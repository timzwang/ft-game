import argparse
import contextlib
import datetime as dt
import hashlib
import importlib.util
import io
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description='Read-only reproductions for the independent review of Claude on 19 October 2026.')
parser.add_argument('--repo', type=Path, default=ROOT / 'repo' if (ROOT / 'repo').exists() else ROOT.parents[2])
parser.add_argument('--out', type=Path)
arguments = parser.parse_args()
REPO = arguments.repo.resolve()
sys.path.insert(0, str(REPO / 'tests'))


def load_module(path, name):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


pipeline = load_module(REPO / 'scripts/ft_pipeline.py', 'review_pipeline')
calendar = load_module(REPO / 'tests/test_calendar.py', 'review_calendar')
checker = load_module(REPO / 'scripts/check_data.py', 'review_checker')
results = {}


stored_ledger = json.loads((REPO / 'data/ledger.json').read_text(encoding='utf-8'))
stored_history = json.loads((REPO / 'data/history.json').read_text(encoding='utf-8'))
price_map = {(row['ticker'], row['date']): row for row in stored_history}
positions = [row for row in stored_ledger if row['table'] == 'position']
metadata = {row['name']: row for row in stored_ledger if row['table'] == 'meta'}
performance = sorted((row for row in stored_ledger if row['table'] == 'perf'), key=lambda row: row['date'])
benchmark_days = sorted(row['date'] for row in stored_history if row['ticker'] == 'SPY')


def independent_weights(date):
    selected = {}
    for row in sorted(positions, key=lambda item: item['effective']):
        if date and row['effective'] <= date:
            selected[row['name']] = (row['weight'] or 0, row['ticker'])
    return {name: record for name, record in selected.items() if record[0] > 0}


reconstructed = float(metadata['start_value']['value'])
accounting_rows = []
for stored in performance:
    date = stored['date']
    day_index = benchmark_days.index(date)
    previous = benchmark_days[day_index - 1] if day_index else None
    previous_weights = independent_weights(previous) if previous and previous >= metadata['start_date']['text'] else {}
    current_weights = independent_weights(date)
    daily_points = 0.0
    for name in set(previous_weights) | set(current_weights):
        old_weight, old_ticker = previous_weights.get(name, (0, None))
        new_weight, new_ticker = current_weights.get(name, (0, None))
        ticker = new_ticker or old_ticker
        current = price_map[(ticker, date)]
        earlier = sorted((row for row in stored_history if row['ticker'] == ticker and previous and row['date'] <= previous),
                         key=lambda row: row['date'])
        kept = min(old_weight, new_weight)
        bought = max(new_weight - old_weight, 0)
        sold = max(old_weight - new_weight, 0)
        if kept:
            daily_points += kept * (current['close'] / earlier[-1]['close'] - 1)
        if bought:
            manual_fill = next((row['value'] for row in positions if row['name'] == name and row['effective'] == date
                                and row['value']), None)
            daily_points += bought * (current['close'] / (manual_fill or current['open']) - 1)
        if sold:
            daily_points += sold * (current['open'] / earlier[-1]['close'] - 1)
    reconstructed *= 1 + daily_points / 100
    accounting_rows.append({'date': date, 'stored': stored['value_est'], 'independent': round(reconstructed, 2),
                            'difference_credits': round(round(reconstructed, 2) - stored['value_est'], 2)})
results['independent_accounting'] = accounting_rows


def reset():
    pipeline._SERIES.clear()
    pipeline.INCOMPLETE.clear()
    pipeline.WARN.clear()


def value(ledger, history):
    reset()
    with contextlib.redirect_stdout(io.StringIO()):
        pipeline.update_performance(ledger, history, 'SPY', '2026-11-27')
    return calendar.perf(ledger)['2026-11-27']['value_est']


baseline = value(calendar.london_change_on_26(pipeline), calendar.history())
results['holiday_baseline_value'] = baseline
for mode in ('missing_26_open', 'imputed_26_open'):
    history = calendar.history()
    if mode == 'missing_26_open':
        del history[('UKB', '2026-11-26')]
    else:
        history[('UKB', '2026-11-26')]['open_obs'] = False
    actual = value(calendar.london_change_on_26(pipeline), history)
    results[mode] = {
        'expected': 'stop before 27 Nov until the actual 26 Nov London fill is available',
        'actual_value': actual,
        'correct_value_with_actual_fill': baseline,
        'incomplete': list(pipeline.INCOMPLETE),
        'warnings': list(pipeline.WARN),
        'silent_wrong_fill': actual != baseline and not pipeline.INCOMPLETE,
    }

reset()
ledger = calendar.london_change_on_26(pipeline)
for ticker, weight in (('UKA', 20), ('UKB', 30)):
    ledger.extend(calendar.ledger(pipeline, [('2026-11-27', ticker, weight)])[3:])
actual = value(ledger, calendar.history())
base = calendar.chain([0.0] + calendar.first_days({'USA': 50, 'UKA': 50}))
points = (
    calendar.kept(50, 'USA', '2026-11-25', '2026-11-27')
    + calendar.kept(20, 'UKA', '2026-11-25', '2026-11-27')
    + 20 * (calendar.o('UKA', '2026-11-26') / calendar.c('UKA', '2026-11-25') - 1)
    + 10 * (calendar.o('UKA', '2026-11-27') / calendar.c('UKA', '2026-11-25') - 1)
    + 20 * (calendar.c('UKB', '2026-11-27') / calendar.o('UKB', '2026-11-26') - 1)
    + 10 * (calendar.c('UKB', '2026-11-27') / calendar.o('UKB', '2026-11-27') - 1)
)
expected = round(base * (1 + points / 100), 2)
reset()
changes = [row for row in pipeline.standstill_rows(ledger, calendar.history(), 'SPY', '2026-11-27')
           if row['kind'] == 'change']
results['changes_on_both_26_and_27'] = {
    'actual_value': actual,
    'expected_under_same_no_26_reset_assumption': expected,
    'difference_credits': round(actual - expected, 2),
    'standstill_rows': [{key: row[key] for key in ('effective', 'value', 'text')} for row in changes],
}

results['last_order_parser'] = {}
for label, event in {
    'london_report_27_nov': {'date': '2026-11-27', 'time_uk': '07:00 UK', 'last_order': 'Before 07:00 Thu 26 Nov'},
    'no_cutoff_time': {'date': '2026-10-28', 'time_uk': 'after US close', 'last_order': 'Any time Wed 28 Oct'},
    'after_cutoff': {'date': '2026-10-28', 'time_uk': 'after US close', 'last_order': 'After 07:00 Wed 28 Oct'},
}.items():
    results['last_order_parser'][label] = {'event': event, 'problem': checker.last_order_problem(event, pipeline)}


def write_json(path, data):
    path.write_text(json.dumps(data), encoding='utf-8')


def resync(folder):
    path = folder / 'state/last-sync.md'
    text = path.read_text(encoding='utf-8')
    for name in ('history', 'ledger', 'macro', 'panel', 'stocks'):
        filename = f'data/{name}.json'
        digest = hashlib.sha256((folder / filename).read_bytes()).hexdigest()
        text = re.sub(r'^[0-9a-f]{64}(\s+' + re.escape(filename) + r')$', digest + r'\1', text, flags=re.M)
    path.write_text(text, encoding='utf-8')


with tempfile.TemporaryDirectory() as temporary:
    folder = Path(temporary)
    shutil.copytree(REPO / 'data', folder / 'data')
    shutil.copytree(REPO / 'state', folder / 'state')
    ledger_path = folder / 'data/ledger.json'
    ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
    ledger.append(pipeline.lrow('event', kind='results', stock='AbbVie', date='2026-10-30', time_uk='before US open'))
    for row in ledger:
        if not row['id']:
            row['id'] = 'review-added-abbvie-event'
    write_json(ledger_path, ledger)
    resync(folder)
    now = dt.datetime(2026, 10, 19, 19, 42, 1, tzinfo=dt.timezone.utc)
    report = checker.check(folder, now, False, pipeline)
    results['baseline_with_abbvie_fixed'] = {'failed': report.failed, 'lines': report.lines}

    sync_path = folder / 'state/last-sync.md'
    sync = sync_path.read_text(encoding='utf-8')
    stocks_path = folder / 'data/stocks.json'
    sync_path.write_text('Run: 2026-10-19T18:58:17Z\n' + hashlib.sha256(stocks_path.read_bytes()).hexdigest()
                         + '  data/stocks.json\n', encoding='utf-8')
    report = checker.check(folder, now, False, pipeline)
    results['manifest_only_lists_stocks'] = {'failed': report.failed,
                                             'sync_lines': [line for line in report.lines if ' sync:' in line]}
    sync_path.write_text(sync, encoding='utf-8')

    saved_ledger = ledger_path.read_bytes()
    write_json(ledger_path, [row for row in ledger if row['table'] != 'contrib'])
    resync(folder)
    report = checker.check(folder, now, False, pipeline)
    results['all_contributions_deleted'] = {'failed': report.failed,
                                            'performance_lines': [line for line in report.lines if 'performance:' in line]}
    ledger_path.write_bytes(saved_ledger)

    for row in ledger:
        if row['table'] == 'event' and row['kind'] == 'results' and row['stock'] == 'Coca-Cola':
            row['date'] = '2027-01-15'
    write_json(ledger_path, ledger)
    resync(folder)
    report = checker.check(folder, now, False, pipeline)
    reset()
    results['held_event_on_wrong_date'] = {
        'failed': report.failed,
        'results_lines': [line for line in report.lines if ' results:' in line],
        'ten_session_total': pipeline.results_total(ledger, {name: weight for name, (weight, ticker)
                                                            in pipeline.live_weights(ledger, '9999-12-31').items()},
                                                     '2026-10-16')[10],
    }
    ledger = json.loads(saved_ledger)

    for row in ledger:
        if row['table'] == 'event' and row['kind'] == 'results' and row['stock'] == 'Coca-Cola':
            row['date'] = '2026-10-21'
            row['implied_pct'] = None
            row['text'] = 'Implied move unavailable'
            row['plan'] = ''
            row['last_order'] = 'Before 07:00 Tue 20 Oct'
    write_json(ledger_path, ledger)
    resync(folder)
    report = checker.check(folder, now, False, pipeline)
    results['documented_absence_literal'] = {
        'failed': report.failed,
        'results_lines': [line for line in report.lines if ' results:' in line],
        'source_condition': 'substring only; does not require a reason',
        'code_line': next(index + 1 for index, line in enumerate((REPO / 'scripts/check_data.py').read_text().splitlines())
                          if 'if "implied move unavailable" in note' in line),
    }

    ledger = json.loads(saved_ledger)
    ledger_path.write_bytes(saved_ledger)
    order_day = '2026-10-16'
    order = [{'name': name, 'weight': weight} for name, (weight, ticker) in pipeline.live_weights(ledger, order_day).items()]
    order_path = folder / 'reorder-input.json'
    write_json(order_path, {'order': order, 'effective': order_day, 'entered': order_day,
                           'order_expected': {'pts': 9.99, 'thesis': 'entered after session close', 'invalidation': 'test'}})
    reset()
    with contextlib.redirect_stdout(io.StringIO()):
        pipeline.cmd_reorder({'stocks': str(folder / 'data/stocks.json'), 'ledger': str(ledger_path),
                              'order': str(order_path), 'out': str(folder / 'reordered')})
    reordered = json.loads((folder / 'reordered/ledger.json').read_text(encoding='utf-8'))
    new_expectations = [row for row in reordered if row['table'] == 'expect' and row['effective'] == order_day]
    results['same_day_after_close_expectation'] = {
        'latest_stored_performance_day': max(row['date'] for row in ledger if row['table'] == 'perf'),
        'effective_and_entered': order_day,
        'accepted_forecasts': [row['forecast'] for row in new_expectations],
        'warnings': list(pipeline.WARN),
    }

results['source_pipeline_sha256'] = hashlib.sha256((REPO / 'scripts/ft_pipeline.py').read_bytes()).hexdigest()
if arguments.out:
    arguments.out.write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results, indent=2))
