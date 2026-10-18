import json, sys, copy, importlib.util
def load(p, n):
    sp = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
old = load('/home/claude/ft-game/scripts/ft_pipeline.py', 'v71'); new = load(sys.argv[1], 'v72')
R = '/home/claude/ft-game/data/'
L0 = json.load(open(R+'ledger.json')); H0 = {(r['ticker'], r['date']): r for r in json.load(open(R+'history.json'))}
# A: GPT's hypothetical row
for m in (old, new):
    h = {}; m.merge_history(h, 'X', [{'date': '2026-10-19', 'open': None, 'high': 110, 'low': 99, 'close': 105, 'volume': 1e6}])
    print('A', m.__name__, 'stored open', h[('X','2026-10-19')]['open'], 'real_open ->', m.real_open(h[('X','2026-10-19')]))
def rerun(m, H, drop_from='2026-10-09'):
    L = [r for r in copy.deepcopy(L0) if not (r['table'] in ('perf','contrib') and r['date'] >= drop_from)]
    m._SERIES.clear(); m.WARN.clear()
    m.update_performance(L, H, 'SPY', '2026-10-16')
    return [(r['date'], r['value_est'], r['day_pct']) for r in L if r['table']=='perf'], [r for r in L if r['table']=='contrib'], list(m.WARN)
# B: complete data -> identical
po, co, _ = rerun(old, H0); pn, cn, _ = rerun(new, H0)
orig = [(r['date'], r['value_est'], r['day_pct']) for r in L0 if r['table']=='perf']
print('B identical to stored:', po == orig, pn == orig, 'contrib rows equal:', [(c['date'],c['name'],c['contrib_pts']) for c in co]==[(c['date'],c['name'],c['contrib_pts']) for c in cn])
# C: Exxon's 14 Oct row missing
H1 = dict(H0); del H1[('XOM','2026-10-14')]
po, _, wo = rerun(old, H1); pn, _, wn = rerun(new, H1)
print('C v7.1 records:', po[-3:], '\n  final value', po[-1][1], 'vs true', orig[-1][1])
print('C v7.2 records up to:', pn[-1], '\n  warn:', [w for w in wn if 'stops' in w])
L = [r for r in copy.deepcopy(L0) if not (r['table'] in ('perf','contrib') and r['date'] >= '2026-10-09')]
new._SERIES.clear(); new.update_performance(L, H1, 'SPY', '2026-10-16'); new._SERIES.clear(); new.update_performance(L, H0, 'SPY', '2026-10-16')
print('C after the row arrives, matches stored:', [(r['date'], r['value_est'], r['day_pct']) for r in L if r['table']=='perf'] == orig)
# D: drift row with no tradable next open settles as n/a
bser = new.series(H0, 'SPY'); d0 = bser[-20]['date']; d1 = bser[-19]['date']
H2 = dict(H0); H2[('XOM', d1)] = dict(H0[('XOM', d1)], open_obs=False)
for m in (old, new):
    L = [m.lrow('drift', date=d0, name='Exxon', ticker='XOM', kind='enter')]
    m._SERIES.clear(); m.resolve_drift(L, H2 if m is new else {k:(dict(v, open=v['close'], high=v['close'], low=v['close'], volume=None) if k==('XOM',d1) else v) for k,v in H0.items()}, 'SPY')
    print('D', m.__name__, L[0]['beat'], L[0]['unit'])
