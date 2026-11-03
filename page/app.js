dash.calc('standing', {
    inputs: ['ledger'],
    title: 'Where the portfolio stands',
    description: 'The latest estimated value and return against the S&P 500, the latest value and rank read from the FT site, the rank needed for the top 2% of players, the gap to the player nearest that line, and the open day-ahead call for the S&P 500.',
    fn: (ledger) => {
      const perf = ledger.filter((r) => r.table === 'perf').sort((a, b) => String(a.date).localeCompare(String(b.date)));
      const rep = ledger.filter((r) => r.table === 'reported').sort((a, b) => (String(a.date) + String(a.time_uk || '')).localeCompare(String(b.date) + String(b.time_uk || '')));
      const p = perf[perf.length - 1] || {};
      const r = rep[rep.length - 1] || {};
      const has = (x) => x !== null && x !== undefined && x !== '';
      const calls = ledger.filter((x) => x.table === 'daycall' && x.name === 'S&P 500').sort((a, b) => String(a.date).localeCompare(String(b.date)));
      const open = calls.filter((x) => !has(x.ret_pct));
      const c = open[open.length - 1] || null;
      const startRow = ledger.find((x) => x.table === 'meta' && x.name === 'start_value');
      const start = startRow && has(startRow.value) ? Number(startRow.value) : 100000;
      const line = rep.filter((x) => has(x.value)).pop() || null;
      return [{
        top2_return: line ? Number(line.value) : null,
        top2_on: line ? line.date : null,
        top2_gap: line && has(p.cum_pct) ? Math.round((Number(line.value) - Number(p.cum_pct)) * 100) / 100 : null,
        chg_abs: has(p.value_est) ? Math.round(Number(p.value_est) - start) : null,
        next_call: c ? (c.kind === 'green' ? 'Green ' : 'Red ') + Number(c.confidence) + '%' : null,
        next_usual: c && has(c.percentile) ? Math.round(Number(c.percentile)) : null,
        next_date: c ? c.date : null,
        sessions: perf.length,
        last_date: p.date || null,
        value_est: has(p.value_est) ? Number(p.value_est) : null,
        cum_pct: has(p.cum_pct) ? Number(p.cum_pct) : null,
        spx_cum_pct: has(p.spx_cum_pct) ? Number(p.spx_cum_pct) : null,
        gap_pts: has(p.cum_pct) && has(p.spx_cum_pct) ? Number(p.cum_pct) - Number(p.spx_cum_pct) : null,
        value_reported: has(r.value_reported) ? Number(r.value_reported) : null,
        reported_on: r.date ? r.date + (r.time_uk ? ' ' + r.time_uk : '') : null,
        rank: has(r.rank) ? Number(r.rank) : null,
        players: has(r.players) ? Number(r.players) : null,
        percentile: has(r.percentile) ? Number(r.percentile) : null,
        target_rank: has(r.players) ? Math.floor(Number(r.players) * 0.02) : null,
      }];
    },
  });

  dash.calc('indexed', {
    inputs: ['ledger'],
    title: 'Portfolio and S&P 500, indexed',
    description: 'Estimated portfolio value and the S&P 500 (through the SPY fund), both set to 100 at the open of the day the portfolio went live, with values read from the FT site on the same scale.',
    fn: (ledger) => {
      const meta = {};
      ledger.filter((r) => r.table === 'meta').forEach((r) => { meta[r.name] = r; });
      const start = meta.start_value ? Number(meta.start_value.value) : 100000;
      const rep = {};
      ledger.filter((r) => r.table === 'reported' && r.value_reported !== null && r.value_reported !== '').forEach((r) => { rep[r.date] = Math.round(Number(r.value_reported) / start * 10000) / 100; });
      const perf = ledger.filter((r) => r.table === 'perf').sort((a, b) => String(a.date).localeCompare(String(b.date)));
      const rows = perf.map((r) => ({date: r.date, portfolio: Math.round((100 + Number(r.cum_pct)) * 100) / 100, sp500: Math.round((100 + Number(r.spx_cum_pct)) * 100) / 100, reported: rep[r.date] === undefined ? null : rep[r.date]}));
      return rows.length ? [{date: 'Start', portfolio: 100, sp500: 100, reported: null}].concat(rows) : [];
    },
  });

  dash.calc('contrib_total', {
    inputs: ['ledger'],
    title: 'Contribution by position',
    description: 'For each stock, the sum over all completed sessions of weight times that day\'s move, in points of the portfolio.',
    fn: (ledger) => {
      const by = {};
      ledger.filter((r) => r.table === 'contrib').forEach((r) => {
        by[r.name] = by[r.name] || {name: r.name, contrib_pts: 0, sessions: 0};
        by[r.name].contrib_pts += Number(r.contrib_pts) || 0;
        by[r.name].sessions += 1;
      });
      return Object.values(by).map((r) => ({name: r.name, contrib_pts: Math.round(r.contrib_pts * 1000) / 1000, sessions: r.sessions})).sort((a, b) => b.contrib_pts - a.contrib_pts);
    },
  });

  dash.calc('conf_bands', {
    inputs: ['ledger'],
    title: 'Confidence hit rate by band',
    description: 'Ratings grouped into three bands, with how many have a closed five-session window and how many of those beat the S&P 500.',
    fn: (ledger) => {
      const conf = ledger.filter((r) => r.table === 'confidence' && r.confidence !== null && r.confidence !== '');
      return [['Below 55', 0, 54.99], ['55 to 59', 55, 59.99], ['60 and above', 60, 100]].map(([band, lo, hi]) => {
        const b = conf.filter((r) => Number(r.confidence) >= lo && Number(r.confidence) <= hi);
        const done = b.filter((r) => r.beat === 'yes' || r.beat === 'no');
        const beat = done.filter((r) => r.beat === 'yes').length;
        return {band, rated: b.length, resolved: done.length, beat, hit_rate: done.length ? Math.round(beat / done.length * 100) : null, avg_rating: b.length ? Math.round(b.reduce((t, r) => t + Number(r.confidence), 0) / b.length) : null};
      });
    },
  });

  dash.calc('results_risk', {
    inputs: ['ledger', 'stocks'],
    title: 'Results risk on holdings',
    description: 'For each holding with results still to come: its weight times the options-implied move, in points of the portfolio.',
    fn: (ledger, stocks) => {
      const w = {};
      stocks.filter((r) => r.group === 'Portfolio').forEach((r) => { w[r.name] = Number(r.weight); });
      // The budget per report: 0.6 points unless the pipeline's results_budget row sets another (pipeline 7.3).
      const rb = ledger.find((r) => r.table === 'meta' && r.name === 'results_budget');
      let rule = {default: 0.6, windows: []};
      try { if (rb && rb.text) rule = Object.assign(rule, JSON.parse(rb.text)); } catch (e) { /* keep 0.6 */ }
      const budgetFor = (d) => (rule.windows || []).reduce((b, x) => (String(d) >= x.from && String(d) <= x.to ? Math.max(b, Number(x.budget)) : b), Number(rule.default) || 0.6);
      return ledger.filter((r) => r.table === 'event' && r.kind === 'results' && w[r.stock] !== undefined)
        .sort((a, b) => String(a.date).localeCompare(String(b.date)))
        .map((r) => ({id: r.id, stock: r.stock, date: r.date, weight: w[r.stock], budget: budgetFor(r.date), implied_pct: r.implied_pct === null || r.implied_pct === '' ? null : Number(r.implied_pct), risk_pts: r.implied_pct === null || r.implied_pct === '' ? null : Math.round(w[r.stock] * Number(r.implied_pct)) / 100}));
    },
  });

  // ---------------------------------------------------------------- state and formatting
  const root = document.querySelector('.sb');
  const PAGES = ['today', 'macro', 'performance', 'risk', 'calendar', 'log'];
  const SEGS = {
    macro: [['call', 'Day call'], ['rates', 'Rates and oil'], ['crypto', 'Crypto'], ['releases', 'Releases']],
    performance: [['overview', 'Overview'], ['ratings', 'Ratings'], ['score', 'Score check']],
    calendar: [['next', '7 days'], ['held', 'Held'], ['results', 'Results'], ['data', 'Data'], ['all', 'All'], ['past', 'Past']],
    log: [['orders', 'Orders'], ['alerts', 'Alerts'], ['analysts', 'Analysts'], ['closed', 'Closed']],
  };
  const S = {page: 'today', size: 's', sel: null, range: 63, busy: true,
    view: {macro: 'call', performance: 'overview', calendar: 'next', log: 'orders'},
    wl: {band: 'all', sort: 'score', dir: -1}, revAll: false};

  const num = (x) => (x === null || x === undefined || x === '' || Number.isNaN(Number(x)) ? null : Number(x));
  const fmt2 = d3.format(',.2f');
  const fmt0 = d3.format(',.0f');
  const fix = (v, d) => (Math.abs(v) + 1e-9).toFixed(d);
  const pct = (v, d) => (v === null || v === undefined ? '—' : (v > 0 ? '+' : v < 0 ? '−' : '') + fix(v, d === undefined ? 2 : d) + '%');
  const pts = (v, d) => (v === null || v === undefined ? '—' : (v > 0 ? '+' : v < 0 ? '−' : '') + fix(v, d === undefined ? 2 : d));
  const bp = (v) => (v === null || v === undefined ? '—' : (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(0) + 'bp');
  const wt = (v) => (v === null || v === undefined ? '—' : (Number.isInteger(v) ? v : v.toFixed(1)) + '%');
  const dir = (v) => (v === null || v === undefined || Math.abs(v) < 0.005 ? 'flat' : v > 0 ? 'up' : 'down');
  const money = (r, v) => (v === null ? '—' : (r.currency === 'USD' ? '$' : '') + fmt2(v) + (r.currency === 'GBX' ? 'p' : ''));
  const asDate = (s) => (s && /^\d{4}-\d{2}-\d{2}/.test(String(s)) ? new Date(String(s).slice(0, 10) + 'T00:00:00Z') : null);
  const dFmt = d3.utcFormat('%a %-d %b');
  const dShort = d3.utcFormat('%-d %b');
  const dateText = (s) => { const d = asDate(s); return d ? dFmt(d) : s ? String(s) : '—'; };
  const shortDate = (s) => { const d = asDate(s); return d ? dShort(d) : s ? String(s) : '—'; };
  const ukParts = () => {
    try {
      const p = {};
      new Intl.DateTimeFormat('en-GB', {timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', weekday: 'short', hour12: false}).formatToParts(new Date()).forEach((x) => { p[x.type] = x.value; });
      return {date: p.year + '-' + p.month + '-' + p.day, time: (p.hour === '24' ? '00' : p.hour) + ':' + p.minute, wd: p.weekday};
    } catch (e) { const s = new Date().toISOString(); return {date: s.slice(0, 10), time: s.slice(11, 16), wd: ''}; }
  };
  const ukNow = () => { const p = ukParts(); return p.date + ' ' + p.time; };
  const today = () => ukParts().date;
  const addDays = (s, n) => { const d = asDate(s); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
  const daysAway = (s) => { const a = asDate(s); const b = asDate(today()); return a && b ? Math.round((a - b) / 86400000) : null; };
  const relDay = (s) => { const n = daysAway(s); return n === null ? '' : n === 0 ? 'today' : n === 1 ? 'tomorrow' : n === -1 ? 'yesterday' : n > 1 ? 'in ' + n + ' days' : -n + ' days ago'; };
  const isWeekday = (s) => { const d = asDate(s).getUTCDay(); return d > 0 && d < 6; };
  // US calendar for the rest of the game (pipeline 7.3): shut on 26 Nov, early close 13:00 New York (18:00 UK) on 27 Nov.
  const US_CLOSED = ['2026-11-26'];
  const isUsSession = (s) => isWeekday(s) && !US_CLOSED.includes(s);
  // UK time from which a US session's daily bar is final: 15 minutes after the close.
  const usFinalUk = (s) => (s === '2026-11-27' ? '18:15' : s >= '2026-10-26' && s <= '2026-10-30' ? '20:15' : '21:15');
  // The last US session that should be complete now: today once its bar is final, else the session before.
  const expectedSession = () => {
    const p = ukParts();
    let d = p.date;
    if (!(isUsSession(d) && p.time >= usFinalUk(d))) { d = addDays(d, -1); while (!isUsSession(d)) d = addDays(d, -1); }
    return d;
  };
  const sessionsBetween = (a, b) => { let n = 0; let d = a; while (d < b) { d = addDays(d, 1); if (isUsSession(d)) n += 1; } return n; };
  const usOpenUk = (s) => (s >= '2026-10-26' && s <= '2026-10-30' ? '13:30' : '14:30');
  const CUTOFF = '08:00';   // order cut-off, UK time: 08:00 UK local time all year, confirmed by the FT on 21 Oct (playbook 6.14, part C)
  const whenKey = (r) => String(r.date) + String(r.time_uk || '');
  const shortTime = (t) => { const m = /\b(\d{1,2}:\d{2})\b/.exec(String(t || '')); if (m) return m[1]; return String(t || '').replace(/\s*\(est\.\)/i, '').replace(/before US open/i, 'Pre-open').replace(/after US close/i, 'After close'); };
  // Has an event dated today already happened? Results stored as text ("after US close") count from the US close.
  const eventPassed = (r) => {
    const p = ukParts();
    if (String(r.date) !== p.date) return String(r.date) < p.date;
    const m = /\b(\d{1,2}):(\d{2})\b/.exec(String(r.time_uk || ''));
    if (m) return p.time >= m[1].padStart(2, '0') + ':' + m[2];
    if (/after US close/i.test(String(r.time_uk || ''))) return p.time >= usFinalUk(p.date);
    if (/before US open/i.test(String(r.time_uk || ''))) return p.time >= usOpenUk(p.date);
    return false;
  };

  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined && text !== null) n.textContent = text; return n; };
  const svgEl = (tag, attrs) => { const n = document.createElementNS('http://www.w3.org/2000/svg', tag); Object.entries(attrs || {}).forEach(([k, v]) => n.setAttribute(k, v)); return n; };
  const btn = (cls, text, fn) => { const b = el('button', cls, text); b.type = 'button'; if (fn) b.addEventListener('click', fn); return b; };
  const st = (text, kind, tip) => { const s = el('span', 'st' + (kind ? ' ' + kind : ''), text); if (tip) { s.dataset.tip = tip; s.tabIndex = 0; } return s; };
  const span = (cls, text) => el('span', cls, text);
  const q = (sel) => root.querySelector(sel);
  const msg = (box, text, failed) => { box.classList.remove('skel'); const m = el('div', 'msg'); if (failed) m.append(el('i')); m.append(span('', failed ? 'Failed to load. The last saved data could not be read.' : text)); box.replaceChildren(m); };
  const bandEl = (t) => { const b = span('band ' + (t || ''), t === 'strong' ? 'Strong' : t === 'middling' ? 'Middling' : t === 'weak' ? 'Weak' : '—'); b.prepend(el('i')); return b; };
  const tierOf = (r) => (['strong', 'middling', 'weak'].includes(r.tier) ? r.tier : '');

  // sentences to bullets; one sentence stays a line
  const ABBR = /^(est|approx|vs|inc|corp|ltd|co|plc|e\.g|i\.e|st|mr|dr|u\.s|no)$/i;
  const sentences = (t) => {
    const words = String(t || '').trim().split(/\s+/).filter(Boolean);
    const out = []; let cur = [];
    words.forEach((w, i) => {
      cur.push(w);
      const nx = words[i + 1];
      if (!nx) return;
      const m = /^(.*?)[.!?]["')]?$/.exec(w);
      if (m && /^["'(]?[A-Z$£]/.test(nx) && !ABBR.test(m[1].replace(/^[("']/, ''))) { out.push(cur.join(' ')); cur = []; }
    });
    if (cur.length) out.push(cur.join(' '));
    return out;
  };
  const bullets = (text, o) => {
    o = o || {};
    const parts = (Array.isArray(text) ? text : sentences(text)).filter(Boolean);
    if (!parts.length) return null;
    if (parts.length === 1) return el('p', o.small ? 'note' : 'note', parts[0]);
    const ul = el('ul', 'bl' + (o.small ? ' s' : ''));
    const max = o.max && parts.length > o.max ? o.max : parts.length;
    parts.forEach((p, i) => { const li = el('li', '', p); if (i >= max) li.hidden = true; ul.append(li); });
    if (max === parts.length) return ul;
    const w = el('div');
    w.style.display = 'flex'; w.style.flexDirection = 'column'; w.style.gap = '0.125rem';
    const label = (parts.length - max) + ' more';
    const m = btn('more', label, () => { const open = m.dataset.open === '1'; Array.from(ul.children).forEach((li, i) => { li.hidden = open && i >= max; }); m.dataset.open = open ? '0' : '1'; m.textContent = open ? label : 'Less'; m.setAttribute('aria-expanded', open ? 'false' : 'true'); });
    m.setAttribute('aria-expanded', 'false');
    w.append(ul, m);
    return w;
  };

  // logos
  let LOGOS = {n: -1, m: new Map()};
  const logos = () => { const d = dash.data('logos'); if (d.status === 'ok' && Array.isArray(d.data) && d.data.length !== LOGOS.n) LOGOS = {n: d.data.length, m: new Map(d.data.map((r) => [r.key, r.src]))}; return LOGOS.m; };
  const logoFor = (ticker, market, name, cls) => {
    const s = el('span', 'logo' + (cls ? ' ' + cls : ''));
    s.setAttribute('aria-hidden', 'true');
    const tk = String(ticker || '');
    const src = tk ? logos().get((market === 'UK' || /\.$/.test(tk) ? 'UK:' : 'US:') + tk) : null;
    if (src && /^data:image\//.test(src)) { const i = el('img'); i.alt = ''; i.src = src; s.append(i); } else s.textContent = (tk || String(name || '?')).replace(/[^A-Za-z]/g, '').slice(0, 2).toUpperCase();
    return s;
  };

  // ---------------------------------------------------------------- derived data, rebuilt when the files change
  let D = null;
  let DKEY = '';
  const derive = (rows, L, H) => {
    const key = rows.length + ':' + L.length + ':' + H.length + ':' + (rows[0] ? rows[0].prices_as_of : '');
    if (D && key === DKEY) return D;
    DKEY = key;
    const byT = new Map();
    H.forEach((r) => { if (!byT.has(r.ticker)) byT.set(r.ticker, []); byT.get(r.ticker).push(r); });
    byT.forEach((a) => a.sort((x, y) => String(x.date).localeCompare(String(y.date))));
    const spy = byT.get('SPY') || [];
    const spyAt = new Map(spy.map((r) => [r.date, Number(r.close)]));
    const relN = (tk, n) => {
      const a = byT.get(tk);
      if (!a || a.length <= n) return null;
      const e = a[a.length - 1]; const b = a[a.length - 1 - n];
      const se = spyAt.get(e.date); const sb = spyAt.get(b.date);
      if (!se || !sb) return null;
      return ((Number(e.close) / Number(b.close)) - (se / sb)) * 100;
    };
    const retN = (tk, n) => { const a = byT.get(tk); if (!a || a.length <= n) return null; return (Number(a[a.length - 1].close) / Number(a[a.length - 1 - n].close) - 1) * 100; };
    const shadow = new Map();
    L.filter((r) => r.table === 'shadow').forEach((r) => { if (!shadow.has(r.name)) shadow.set(r.name, []); shadow.get(r.name).push(r); });
    shadow.forEach((a) => a.sort((x, y) => String(y.date).localeCompare(String(x.date))));
    const t0 = today();
    const events = L.filter((r) => r.table === 'event');
    const nextRes = new Map();
    events.filter((r) => r.kind === 'results' && !eventPassed(r)).sort((a, b) => String(a.date).localeCompare(String(b.date))).forEach((r) => { if (r.stock && !nextRes.has(r.stock)) nextRes.set(r.stock, r); });
    const revBy = new Map();
    L.filter((r) => r.table === 'revision').forEach((r) => { if (!revBy.has(r.stock)) revBy.set(r.stock, []); revBy.get(r.stock).push(r); });
    const stocks = rows.filter((r) => r.group !== 'Cash').map((r) => {
      const sh = shadow.get(r.name) || [];
      const s0 = sh[0] || null;
      const s1 = sh.find((x) => x.date !== (s0 && s0.date)) || null;
      const tk = num(r.trend_price) !== null && r.trend_ticker ? r.trend_ticker : (r.market === 'UK' && byT.has(r.ticker + '-US') ? r.ticker + '-US' : r.ticker);
      const nr = nextRes.get(r.name) || null;
      const rv = (revBy.get(r.name) || []).filter((x) => daysAway(x.date) >= -7);
      return Object.assign({}, r, {
        held: r.group === 'Portfolio',
        rel20: relN(tk, 20), rel5: relN(tk, 5), ret20: retN(tk, 20),
        conv: s0 ? num(s0.confidence) : num(r.confidence),
        dScore: s0 && s1 && num(s0.score) !== null && num(s1.score) !== null ? num(s0.score) - num(s1.score) : null,
        dFrom: s1 ? s1.date : null,
        nextRes: nr, resDays: nr ? daysAway(nr.date) : null, implied: nr ? num(nr.implied_pct) : null,
        rev7: rv.length, histT: tk,
      });
    });
    const latestPerf = L.filter((r) => r.table === 'perf').sort((a, b) => String(a.date).localeCompare(String(b.date)));
    const sold = new Map();
    L.filter((r) => r.table === 'trade' && num(r.to_w) === 0).forEach((r) => { if (!sold.has(r.name) || String(r.effective) > sold.get(r.name)) sold.set(r.name, String(r.effective)); });
    D = {byT, spy, stocks, shadow, events, revBy, perf: latestPerf, relN, retN, sold, listed: new Set(rows.map((r) => r.name))};
    return D;
  };

  // A company's results matter here only while it is held or on the watchlist; the calendar keeps older rows in the ledger.
  const relevantEvent = (r) => r.kind !== 'results' || !r.stock || D.listed.has(r.stock);

  // ---------------------------------------------------------------- charts
  // A line chart with a left value axis, a date axis, an optional reference line and a hover readout.
  const lineChart = (box, rows, series, o) => {
    box.classList.remove('skel');
    box.replaceChildren();
    const W = Math.max(260, box.clientWidth || 600);
    const H = o.height || 190;
    const vals = [];
    rows.forEach((r) => series.concat((o.dots || []).map((k) => ({key: k}))).forEach((s) => { const v = r[s.key]; if (v !== null && v !== undefined && Number.isFinite(v)) vals.push(v); }));
    if (o.ref !== undefined) vals.push(o.ref);
    if (!vals.length) { msg(box, o.empty || 'No data yet.'); return; }
    let lo = Math.min(...vals); let hi = Math.max(...vals);
    if (o.floor !== undefined) lo = Math.min(lo, o.floor);
    const pad = (hi - lo || Math.abs(hi) * 0.02 || 1) * 0.1;
    let dom = [lo - (o.floor === lo ? 0 : pad), hi + pad];
    if (o.invert) dom = [dom[1], dom[0]];
    const y = d3.scaleLinear(dom, [H - 22, 8]).nice(4);
    const ticks = y.ticks(4);
    const tt = ticks.map((t) => o.yfmt(t));
    const m = {l: 8 + Math.max(...tt.map((t) => t.length)) * 6.4, r: o.right || 12, t: 8, b: 22};
    const x = d3.scalePoint(rows.map((r, i) => i), [m.l + 4, W - m.r]);
    const svg = svgEl('svg', {viewBox: '0 0 ' + W + ' ' + H, width: '100%', role: 'img', 'aria-label': o.label});
    ticks.forEach((t, i) => {
      svg.append(svgEl('line', {x1: m.l, x2: W - m.r, y1: y(t), y2: y(t), stroke: 'var(--rule2)', 'stroke-width': 1}));
      const tx = svgEl('text', {x: m.l - 6, y: y(t), dy: '0.32em', 'text-anchor': 'end', class: 'ax'});
      tx.textContent = tt[i];
      svg.append(tx);
    });
    if (o.ref !== undefined) svg.append(svgEl('line', {x1: m.l, x2: W - m.r, y1: y(o.ref), y2: y(o.ref), stroke: 'var(--ink3)', 'stroke-width': 1, 'stroke-dasharray': '3 3'}));
    if (o.refLabel) { const tx = svgEl('text', {x: W - m.r, y: y(o.ref) - 4, 'text-anchor': 'end', class: 'ax'}); tx.textContent = o.refLabel; svg.append(tx); }
    const step = Math.max(1, Math.ceil(rows.length / Math.max(2, Math.floor((W - m.l - m.r) / 70))));
    rows.forEach((r, i) => {
      const last = i === rows.length - 1;
      if (!last && (i % step !== 0 || rows.length - 1 - i < step * 0.8)) return;
      const tx = svgEl('text', {x: x(i), y: H - 6, 'text-anchor': i === 0 ? 'start' : last ? 'end' : 'middle', class: 'ax'});
      tx.textContent = o.xfmt(r);
      svg.append(tx);
    });
    series.forEach((s) => {
      const p = rows.map((r, i) => [i, r[s.key]]).filter((d) => d[1] !== null && d[1] !== undefined && Number.isFinite(d[1]));
      if (s.area && p.length > 1) { const a = svgEl('path', {d: d3.area().x((d) => x(d[0])).y0(y(o.areaBase !== undefined && o.areaBase !== null ? o.areaBase : y.domain()[0])).y1((d) => y(d[1]))(p) || '', 'fill-opacity': 0.1, stroke: 'none'}); a.style.fill = s.color; svg.append(a); }
      const path = svgEl('path', {d: d3.line().curve(d3.curveMonotoneX).x((d) => x(d[0])).y((d) => y(d[1]))(p) || '', fill: 'none', 'stroke-width': s.width || 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'});
      if (s.dash) path.setAttribute('stroke-dasharray', s.dash);
      path.style.stroke = s.color;
      svg.append(path);
      if (p.length) { const c = svgEl('circle', {cx: x(p[p.length - 1][0]), cy: y(p[p.length - 1][1]), r: 3}); c.style.fill = s.color; svg.append(c); }
    });
    (o.dots || []).forEach((k) => rows.forEach((r, i) => { if (r[k] === null || r[k] === undefined) return; svg.append(svgEl('circle', {cx: x(i), cy: y(r[k]), r: 3.5, fill: 'var(--ink)', stroke: 'var(--panel)', 'stroke-width': 1.5})); }));
    const rule = svgEl('line', {y1: m.t, y2: H - m.b, stroke: 'var(--ink3)', 'stroke-width': 1, visibility: 'hidden'});
    svg.append(rule);
    box.append(svg);
    const tip = el('div', 'tip'); tip.hidden = true; box.append(tip);
    const all = series.concat((o.dots || []).map((k) => ({key: k, name: o.dotName || k, color: 'var(--on-pop)'})));
    const move = (ev) => {
      const b = svg.getBoundingClientRect();
      const px = (ev.clientX - b.left) / b.width * W;
      let best = 0;
      rows.forEach((r, i) => { if (Math.abs(x(i) - px) < Math.abs(x(best) - px)) best = i; });
      rule.setAttribute('x1', x(best)); rule.setAttribute('x2', x(best)); rule.setAttribute('visibility', 'visible');
      tip.replaceChildren(el('div', 'h', o.xlong(rows[best])));
      all.forEach((s) => { const v = rows[best][s.key]; if (v === null || v === undefined) return; const d = el('div'); const sw = span('sw'); sw.style.background = s.color; d.append(sw, span('', s.name + ' ' + o.vfmt(v))); tip.append(d); });
      tip.hidden = false;
      const left = x(best) / W * b.width;
      tip.style.left = Math.max(0, Math.min(box.clientWidth - tip.offsetWidth, left + 10 + tip.offsetWidth > box.clientWidth ? left - tip.offsetWidth - 10 : left + 10)) + 'px';
      tip.style.top = '0px';
    };
    const hide = () => { rule.setAttribute('visibility', 'hidden'); tip.hidden = true; };
    svg.addEventListener('pointermove', move);
    svg.addEventListener('pointerdown', move);
    svg.addEventListener('pointerleave', hide);
  };
  const spark = (vals) => {
    const v = vals.filter((x) => Number.isFinite(x));
    if (v.length < 3) return null;
    const lo = Math.min(...v); const hi = Math.max(...v);
    const y = (a) => (hi === lo ? 10 : 18 - (a - lo) / (hi - lo) * 16);
    const svg = svgEl('svg', {class: 'spark', viewBox: '0 0 100 20', preserveAspectRatio: 'none', 'aria-hidden': 'true'});
    svg.append(svgEl('path', {d: v.map((a, i) => (i ? 'L' : 'M') + (i / (v.length - 1) * 100).toFixed(1) + ' ' + y(a).toFixed(1)).join(' ')}));
    return svg;
  };
  const sparkOf = (r) => spark(String(r.spark || '').split('|').map(Number));
  // Horizontal bars: diverging around zero, or from zero with an optional guide line.
  const bars = (box, items, o) => {
    box.classList.remove('skel');
    if (!items.length) { msg(box, o.empty || 'Nothing yet.'); return; }
    const mx = Math.max(o.min || 0, ...items.map((i) => Math.abs(i.value || 0)));
    box.replaceChildren(...items.map((i) => {
      const r = el('div', 'br');
      const l = span('br-l', i.label); if (i.detail) l.append(el('small', '', i.detail));
      const k = el('div', 'br-k'); k.setAttribute('aria-hidden', 'true');
      if (i.value !== null && i.value !== undefined) {
        const f = el('i', o.diverging ? (i.value >= 0 ? 'p' : 'n') : '');
        if (o.diverging) { const w = Math.abs(i.value) / mx * 50; f.style.left = (i.value >= 0 ? 50 : 50 - w) + '%'; f.style.width = w + '%'; } else { f.style.left = '0'; f.style.width = Math.min(100, Math.abs(i.value) / mx * 100) + '%'; }
        k.append(f);
      }
      if (o.diverging) { const z = el('span', 'z'); z.style.left = '50%'; k.append(z); }
      if (o.guide) { const g = el('span', 'g'); g.style.left = Math.min(100, o.guide / mx * 100) + '%'; k.append(g); }
      r.append(l, span('br-v ' + (o.diverging ? dir(i.value) : ''), i.text), k);
      return r;
    }));
  };
  // A plain table: columns are {h, cls, num, tip, cell(row) -> text | Node | [text, cls]}.
  const table = (box, cols, rows, o) => {
    o = o || {};
    box.classList.remove('skel');
    if (!rows.length) { msg(box, o.empty || 'Nothing yet.'); return null; }
    const use = cols.filter((c) => !c.only || c.only.includes(o.size || S.cols || S.size));
    const t = el('table', 't');
    if (o.caption) { const c = el('caption', '', o.caption); c.style.position = 'absolute'; c.style.left = '-9999px'; t.append(c); }
    const hr = el('tr');
    use.forEach((c) => {
      const th = el('th', c.num ? 'num' : '');
      th.scope = 'col';
      if (o.sort && c.key) {
        const b = btn('sort', c.h, () => o.onSort(c.key));
        b.append(sortIcon());
        if (c.tip) b.dataset.tip = c.tip;
        if (o.sort.sort === c.key) th.setAttribute('aria-sort', o.sort.dir > 0 ? 'ascending' : 'descending');
        th.append(b);
      } else { th.textContent = c.h || ''; if (c.tip) { th.append(document.createTextNode(' '), qmark(c.tip)); } }
      hr.append(th);
    });
    const thead = el('thead'); thead.append(hr);
    const tb = el('tbody');
    rows.forEach((r) => {
      if (r && r.__group) { const tr = el('tr', 'grp'); const td = el('td', '', r.__group); td.colSpan = use.length; tr.append(td); tb.append(tr); return; }
      const tr = el('tr', o.rowCls ? o.rowCls(r) || '' : '');
      use.forEach((c) => {
        const td = el('td', (c.num ? 'num ' : '') + (c.cls || ''));
        const v = c.cell(r);
        if (v instanceof Node) td.append(v); else if (Array.isArray(v)) { td.textContent = v[0]; if (v[1]) td.classList.add(v[1]); } else td.textContent = v === null || v === undefined ? '—' : String(v);
        tr.append(td);
      });
      if (o.onRow) {
        tr.classList.add('sel'); tr.tabIndex = 0;
        if (o.label) tr.setAttribute('aria-label', o.label(r));
        tr.addEventListener('click', () => o.onRow(r));
        tr.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); o.onRow(r); } });
      }
      tb.append(tr);
    });
    t.append(thead, tb);
    const w = el('div', 'tw'); w.append(t);
    box.replaceChildren(w);
    return t;
  };
  const sortIcon = () => { const s = svgEl('svg', {viewBox: '0 0 8 8', 'aria-hidden': 'true'}); s.append(svgEl('path', {d: 'M1 2.5 4 5.5 7 2.5', fill: 'none', stroke: 'currentColor', 'stroke-width': 1.5})); return s; };
  const qmark = (tip) => { const s = span('q', '?'); s.dataset.tip = tip; s.tabIndex = 0; s.setAttribute('aria-label', tip); return s; };
  const agItem = (when, what, body, chips) => {
    const li = el('li');
    const at = String(when || '').split(', ');
    const w = el('div', 'ag-w');
    if (at[0]) w.append(el('b', '', at[0]));
    if (at.length > 1) w.append(document.createTextNode(at.slice(1).join(', ')));
    const x = el('div', 'ag-x', what);
    (chips || []).forEach((c) => { if (c) x.append(c); });
    if (body) x.append(typeof body === 'string' ? el('small', '', body) : body);
    li.append(w, x);
    return li;
  };
  const dayGroups = (box, groups, empty) => {
    box.classList.remove('skel');
    if (!groups.length) { const c = el('section', 'pn'); msg(c, empty); box.replaceChildren(c); return; }
    const cards = groups.map((g) => {
      const d = el('section', 'pn dg' + (g.past ? ' past' : ''));
      const h = el('div', 'ph');
      h.append(el('h2', '', g.title));
      if (g.sub) h.append(span('meta', g.sub));
      const b = el('div', 'pb');
      b.append(g.body);
      d.append(h, b);
      return {d, size: 2 + g.body.children.length};
    });
    // Two columns on a wide screen, each card going to the shorter one, so short days leave no holes.
    const n = root.clientWidth >= 1180 ? 2 : 1;
    const cols = Array.from({length: n}, () => ({node: el('div', 'col'), size: 0}));
    cards.forEach((c) => { const t0 = cols.reduce((a, b) => (b.size < a.size ? b : a)); t0.node.append(c.d); t0.size += c.size; });
    box.style.gridTemplateColumns = 'repeat(' + n + ', minmax(0, 1fr))';
    box.replaceChildren(...cols.map((c) => c.node));
  };
  // One line of a list: time, icon, what it is, key figures; tap to read the rest.
  const OPEN = new Set();
  const lineRow = (o) => {
    const w = el('div', 'er');
    const can = !!o.detail;
    const h = can ? btn('er-h', null) : el('div', 'er-h');
    if (o.when !== undefined) { const a = el('div', 'er-w', o.when); if (o.whenSub) a.append(el('small', '', o.whenSub)); h.append(a); }
    if (o.icon) { const i = el('div', 'er-i'); i.append(o.icon); h.append(i); }
    const m = el('div', 'er-t');
    m.append(el('b', '', o.title));
    if (o.note) m.append(el('span', '', o.note));
    h.append(m);
    const s = el('div', 'er-s');
    (o.stats || []).filter(Boolean).forEach((x) => s.append(x));
    h.append(s);
    const c = el('div', 'er-c');
    if (can) c.append(chev('M6 3l5 5-5 5'));
    h.append(c);
    w.append(h);
    if (can) {
      const d = el('div', 'er-d');
      d.append(o.detail);
      const set = (on) => { d.hidden = !on; h.setAttribute('aria-expanded', on ? 'true' : 'false'); };
      set(OPEN.has(o.key));
      h.addEventListener('click', () => { const on = !OPEN.has(o.key); if (on) OPEN.add(o.key); else OPEN.delete(o.key); set(on); });
      w.append(d);
    }
    return w;
  };
  const stat = (label, value, cls, tip) => { const s = el('span', 'stat'); if (label) s.append(el('i', '', label)); s.append(el('b', cls || '', value)); if (tip && tip !== value) { s.dataset.tip = tip; s.tabIndex = 0; } return s; };
  // Figures as logged carry their source in brackets and sometimes a sentence: keep the figure.
  const cleanFig = (x) => String(x || '').replace(/\s*\([^)]*\)/g, '').split(';')[0].trim();
  const lastOrderText = (r) => (r.last_order && r.last_order !== 'Passed' ? String(r.last_order).replace(/^Before 07:00/, 'Before ' + CUTOFF) : '');
  const iconFor = (stock, kind) => {
    const s = stock ? D.stocks.find((x) => x.name === stock) : null;
    if (s) return logoFor(s.ticker, s.market, s.name, 's');
    if (stock) return logoFor('', '', stock, 's');
    const g = el('span', 'glyph');
    const v = svgEl('svg', {viewBox: '0 0 16 16', 'aria-hidden': 'true'});
    v.append(svgEl('path', {d: kind === 'game' ? 'M4 14V2.5M4 3h8l-2 3 2 3H4' : 'M3 13V9M8 13V3M13 13V6'}));
    g.append(v);
    return g;
  };
  const capDay = (s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : '');
  const timeKey = (r) => { const m = /\b(\d{1,2}):(\d{2})\b/.exec(String(r.time_uk || '')); if (m) return m[1].padStart(2, '0') + m[2]; return /all day/i.test(String(r.time_uk || '')) ? '0000' : /before/i.test(String(r.time_uk || '')) ? '1100' : /after/i.test(String(r.time_uk || '')) ? '2105' : '9999'; };
  const segBar = (name) => {
    const box = q('#seg-' + name);
    box.replaceChildren(...SEGS[name].map(([k, t]) => { const b = btn('', t, () => { S.view[name] = k; draw(); }); b.setAttribute('aria-pressed', S.view[name] === k ? 'true' : 'false'); return b; }));
    root.querySelectorAll('#' + name + ' [data-view]').forEach((n) => { n.hidden = n.dataset.view !== S.view[name]; });
  };

  // ---------------------------------------------------------------- header: how fresh the prices are
  const freshness = (rows) => {
    const box = q('#fresh');
    const first = rows[0] || {};
    const sess = D.spy.length ? D.spy[D.spy.length - 1].date : null;
    const kids = [];
    if (first.prices_as_of) {
      kids.push(span('', String(first.prices_as_of).replace(/\s*\(.*\)\s*$/, '')));
      if (!/UK/.test(first.prices_as_of) && sess) {
        const n = sessionsBetween(sess, expectedSession());
        if (n === 1) kids.push(st('1 session behind', 'warn', 'The last completed US session is not in the files yet. The evening review adds it after 21:30 UK.'));
        else if (n > 1) kids.push(st(n + ' sessions behind', 'bad', 'Prices have not been refreshed for ' + n + ' sessions. Treat moves and scores as out of date.'));
      }
    }
    box.replaceChildren(...kids);
  };

  // ---------------------------------------------------------------- where the portfolio stands
  let heroDraw = () => {};
  const strip = (rows, L) => {
    const box = q('#strip');
    const sd = dash.data('standing');
    const s = sd.status === 'ok' && sd.data && sd.data[0] ? sd.data[0] : null;
    const tile = (label, value, cls, unit, tip, flag) => {
      const d = el('div', 'tile');
      const l = el('div', 'tile-l', label);
      if (flag) l.prepend(el('i'));
      if (tip) { d.dataset.tip = tip; d.tabIndex = 0; }
      const v = el('div', 'tile-v ' + (cls || ''), value);
      if (unit) v.append(el('small', '', unit));
      d.append(l, v);
      return d;
    };
    const hero = el('div', 'hero');
    hero.append(el('div', 'hero-l', 'Portfolio'));
    const hv = el('div', 'hero-v');
    const has = s && s.sessions > 0;
    hv.append(el('b', '', has ? fmt0(s.value_est) : '—'));
    if (has) hv.append(el('span', 'pill big ' + dir(s.cum_pct), pct(s.cum_pct)));
    hero.append(hv);
    const lg = el('ul', 'lg');
    [['Portfolio', 'var(--s1)'], ['S&P 500', 'var(--bench)']].forEach(([n, c]) => { const li = el('li'); const sw = span('sw'); sw.style.background = c; li.append(sw, document.createTextNode(n)); lg.append(li); });
    const chart = el('div', 'ch');
    hero.append(lg, chart);
    const perf = D.perf;
    const last = perf[perf.length - 1];
    const lastDay = last ? num(last.day_pct) : null;
    const ranked = s && s.rank !== null;
    const stale = ranked ? sessionsBetween(String(s.reported_on).slice(0, 10), expectedSession()) >= 2 : false;
    const rankLabel = ranked ? 'Rank, ' + shortDate(s.reported_on) : 'Rank';
    const tiles = el('div', 'tiles');
    tiles.append(
      tile('Against S&P 500', has ? pts(s.gap_pts) : '—', has ? dir(s.gap_pts) : '', has ? 'pts' : ''),
      tile(last ? 'Last session, ' + shortDate(last.date) : 'Last session', pct(lastDay), dir(lastDay)),
      tile(rankLabel, ranked ? fmt0(s.rank) : '—', '', ranked && s.percentile !== null ? 'top ' + Math.round(s.percentile) + '%' : '', ranked ? 'Of ' + fmt0(s.players) + ' players. The top 2% is rank ' + fmt0(s.target_rank) + ' or better. Only known when read off the FT site.' : 'Send your rank and the number of players.', stale),
      tile('Gap to top 2%', s && s.top2_gap !== null ? Math.abs(s.top2_gap).toFixed(1) : '—', s && s.top2_gap !== null ? (s.top2_gap > 0 ? 'down' : 'up') : '', s && s.top2_gap !== null ? 'pts' : '', s && s.top2_return !== null ? 'The player nearest the line was at ' + pct(s.top2_return) + ' on ' + shortDate(s.top2_on) + '. Portfolio now ' + pct(s.cum_pct) + ' (estimate).' : 'Needs the return of a player near the line.', stale),
    );
    box.replaceChildren(hero, tiles);
    box.classList.remove('skel');
    const ix = dash.data('indexed');
    const irows = ix.status === 'ok' ? ix.data : [];
    if (irows.length >= 2) lineChart(chart, irows, [{key: 'portfolio', name: 'Portfolio', color: 'var(--s1)', width: 2.25, area: true}, {key: 'sp500', name: 'S&P 500', color: 'var(--bench)', width: 1.5}], {height: S.size === 's' ? 128 : 148, ref: 100, label: 'Portfolio estimate and the S&P 500 since the start, both 100 at the start', yfmt: (t) => t.toFixed(0), vfmt: (x) => x.toFixed(2), xfmt: (r) => (r.date === 'Start' ? 'Start' : shortDate(r.date)), xlong: (r) => (r.date === 'Start' ? 'Start, Fri 9 Oct open' : dateText(r.date)), areaBase: null});
  };

  // ---------------------------------------------------------------- the order
  const orderQueue = (rows, L) => {
    const box = q('#oq');
    const held = rows.filter((r) => r.group === 'Portfolio').sort((a, b) => num(b.weight) - num(a.weight));
    const cashRow = rows.find((r) => r.group === 'Cash');
    const cash = cashRow ? num(cashRow.weight) || 0 : 0;
    const trades = L.filter((r) => r.table === 'trade');
    const E = trades.reduce((m, r) => (String(r.effective) > m ? String(r.effective) : m), '');
    const round = trades.filter((r) => String(r.effective) === E);
    const alert = L.filter((r) => r.table === 'alert' && r.stock === 'Order').sort((a, b) => whenKey(b).localeCompare(whenKey(a)))[0] || null;
    const now = ukNow();
    // An order is live from the review's message until the cut-off on the day it fills.
    const live = !!alert && /^(changed|revised)/i.test(String(alert.text || '')) && E && now < E + ' ' + CUTOFF;
    const first = rows[0] || {};
    const head = el('div', 'ph');
    head.append(el('h2', '', 'Order'));
    const state = el('span', 'oq-state' + (live ? ' go' : ''), live ? 'Enter before ' + CUTOFF + ' UK' : 'Nothing to enter');
    head.append(state);
    const body = el('div', 'pb');
    const pendingFill = !!E && now < E + ' ' + usOpenUk(E);
    const marks = new Map(pendingFill ? round.map((r) => [r.name, r]) : []);
    const grid = el('div', 'oq-grid');
    held.forEach((r) => {
      const m = marks.get(r.name);
      const i = el('div', 'oq-i' + (m && num(m.to_w) > num(m.from_w) ? ' new' : ''));
      i.append(logoFor(r.ticker, r.market, r.name, 's'), span('t', r.ticker), span('w', wt(num(r.weight))));
      grid.append(i);
    });
    if (cash > 0) { const i = el('div', 'oq-i'); i.append(span('t', 'Cash'), span('w', wt(cash))); grid.append(i); }
    if (!held.length) msg(grid, S.busy ? 'Loading' : 'No order has been logged yet.');
    body.append(grid);
    const sells = pendingFill ? round.filter((r) => num(r.to_w) === 0) : [];
    if (sells.length) { const x = el('div', 'oq-sell'); sells.forEach((r) => x.append(span('', 'Sell ' + r.ticker))); body.append(x); }
    const total = held.reduce((t, r) => t + (num(r.weight) || 0), 0) + cash;
    const ok = held.length >= 5 && held.length <= 20 && held.every((r) => num(r.weight) >= 5 && num(r.weight) <= 25) && cash <= 25 && Math.abs(total - 100) < 0.05;
    if (held.length && !ok) body.append(st('Breaks a game rule: check the log', 'bad'));
    const lastLine = el('div', 'oq-last');
    if (live) {
      const mins = Math.round((new Date(E + 'T' + CUTOFF + ':00') - new Date(now.replace(' ', 'T') + ':00')) / 60000);
      lastLine.textContent = 'For ' + (first.order_for || dateText(E)) + (mins > 0 ? ', cut-off in ' + (mins >= 60 ? Math.floor(mins / 60) + 'h ' : '') + (mins % 60) + 'm' : '');
    } else {
      const outs = round.filter((r) => num(r.to_w) === 0).map((r) => r.ticker);
      const ins = round.filter((r) => num(r.from_w) === 0).map((r) => r.ticker);
      lastLine.textContent = (first.order_for ? 'For ' + first.order_for + '. ' : '') + (E ? 'Last changed ' + dateText(E) + (outs.length + ins.length && outs.length + ins.length <= 4 ? ': ' + [outs.length ? outs.join(', ') + ' out' : '', ins.length ? ins.join(', ') + ' in' : ''].filter(Boolean).join(', ') : '') : '');
    }
    body.append(lastLine);
    box.replaceChildren(head, body);
  };

  // ---------------------------------------------------------------- holdings and watchlist
  const soldOn = (r) => (D.sold.get(r.name) && daysAway(D.sold.get(r.name)) >= -10 ? D.sold.get(r.name) : null);
  const statusChip = (r) => {
    if (r.held) return st('Held ' + wt(num(r.weight)));
    const t = String(r.status || '').toLowerCase();
    if (/ready|confirmed/.test(t)) return st(/ready/.test(t) ? 'Ready' : 'Confirmed', 'okay', 'Passes the entry rules; a candidate for the next order.');
    if (/drift: enter/.test(t)) return st('Drift entry', 'okay', 'Passed all six earnings-drift tests.');
    if (/follow|2nd day/.test(t)) return st('Needs 2nd day', 'warn', 'Strong news, but needs a second session closing above its open on heavy volume.');
    const so = soldOn(r);
    if (so) return st('Sold ' + shortDate(so));
    if (/faded/.test(t)) return st('Faded gap', 'warn', 'Gapped up then closed below its open; needs a second strong session.');
    return null;
  };
  const scoreCell = (r) => el('span', 'sc ' + tierOf(r), num(r.score) === null ? '—' : String(num(r.score)));
  const deltaCell = (r) => (r.dScore === null ? span('faint', '—') : r.dScore === 0 ? span('faint', '0') : span('delta ' + (r.dScore > 0 ? 'up' : 'down'), (r.dScore > 0 ? '+' : '−') + Math.abs(r.dScore)));
  const stkCell = (r) => { const w = el('div', 'stk'); const t = el('div', 'stk-t'); t.append(el('b', '', r.ticker), span('', r.name)); w.append(logoFor(r.ticker, r.market, r.name, 's'), t); return w; };
  const rowLabel = (r) => r.name + ', ' + money(r, num(r.price)) + ', ' + pct(num(r.day_pct)) + ' on the day, score ' + num(r.score) + '. Open research.';
  const sortRows = (list, sort, dirn) => {
    const val = {score: (r) => num(r.score), delta: (r) => r.dScore, rel: (r) => r.rel20, day: (r) => num(r.day_pct), res: (r) => (r.resDays === null ? 999 : r.resDays), weight: (r) => num(r.weight), name: (r) => r.name}[sort];
    return list.slice().sort((a, b) => {
      const x = val(a); const y = val(b);
      if (x === null || x === undefined) return 1;
      if (y === null || y === undefined) return -1;
      return (typeof x === 'string' ? x.localeCompare(y) : x - y) * dirn;
    });
  };
  const open = (r) => { S.sel = r.name; draw(); const p = q('#research'); if (S.size !== 'l') root.scrollIntoView({block: 'start'}); if (p) p.focus({preventScroll: S.size === 'l'}); };
  const pxCell = (r) => { const d = el('div', 'px'); d.append(span('', money(r, num(r.price))), el('span', 'pill ' + dir(num(r.day_pct)), pct(num(r.day_pct)))); return d; };
  const sparkCell = (r) => { const d = el('div', 'spk ' + dir(num(r.day_pct))); const s = sparkOf(r); if (s) d.append(s); return d; };
  const idCell = (r, sub) => { const d = el('div', 'id'); const n = el('span', '', sub || r.name); d.append(el('b', '', r.ticker), n); return d; };
  const rowBtn = (cls, r) => { const b = btn('row ' + cls + (S.sel === r.name ? ' on' : ''), null, () => open(r)); b.setAttribute('aria-label', rowLabel(r)); b.append(logoFor(r.ticker, r.market, r.name)); return b; };

  const holdings = () => {
    const box = q('#hold-body');
    const held = sortRows(D.stocks.filter((r) => r.held), 'weight', -1);
    box.classList.remove('skel');
    if (!held.length) { msg(box, S.busy ? 'Loading' : 'No holdings.'); return; }
    const wide = (S.cols || S.size) !== 's' && root.clientWidth >= 720 && !(S.sel && S.size === 'l');
    const wrap = el('div', 'rows one');
    if (wide) {
      const h = el('div', 'row-h hold wide');
      ['', 'Stock', '', 'Price', '', 'Weight', 'Points', 'vs S&P, 20d', 'Score'].forEach((t, i) => h.append(span(i > 2 ? 'r' : '', t)));
      h.children[4].textContent = 'Day';
      wrap.append(h);
    }
    held.forEach((r) => {
      const b = rowBtn('hold' + (wide ? ' wide' : ''), r);
      const cp = num(r.contrib_pts);
      if (wide) {
        const price = span('cell', money(r, num(r.price)));
        b.append(idCell(r), sparkCell(r), price, el('span', 'pill ' + dir(num(r.day_pct)), pct(num(r.day_pct))), span('cell w', wt(num(r.weight))), span('cell ' + dir(cp), cp === null ? (r.live_from ? 'fills ' + shortDate(r.live_from) : '—') : pts(cp)), span('cell ' + dir(r.rel20), pts(r.rel20, 1)), el('span', 'cell'));
        b.lastChild.append(scoreCell(r));
      } else {
        const w = el('div', 'stack');
        w.append(el('b', '', wt(num(r.weight))), span(dir(cp), cp === null ? '—' : pts(cp) + ' pts'));
        b.append(idCell(r), w, pxCell(r));
      }
      wrap.append(b);
    });
    box.replaceChildren(wrap);
  };

  const watchlist = () => {
    const box = q('#watch-body');
    const w = S.wl;
    const fl = q('#watch-fl');
    const seg = el('div', 'seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'Strength');
    [['all', 'All'], ['strong', 'Strong'], ['middling', 'Middling'], ['weak', 'Weak']].forEach(([k, t]) => { const b = btn('', t, () => { S.wl.band = k; draw(); }); b.setAttribute('aria-pressed', w.band === k ? 'true' : 'false'); seg.append(b); });
    const sel = el('select', 'sel'); sel.setAttribute('aria-label', 'Sort by');
    [['score', 'Score'], ['day', 'Today'], ['rel', 'vs S&P, 20 days'], ['delta', 'Score change'], ['res', 'Next results']].forEach(([k, t]) => { const o = el('option', '', t); o.value = k; if (w.sort === k) o.selected = true; sel.append(o); });
    sel.addEventListener('change', () => { S.wl.sort = sel.value; S.wl.dir = sel.value === 'res' ? 1 : -1; draw(); });
    fl.replaceChildren(seg, sel);
    const list = sortRows(D.stocks.filter((r) => !r.held).filter((r) => (w.band === 'all' ? true : tierOf(r) === w.band)), w.sort, w.dir);
    box.classList.remove('skel');
    if (!list.length) { msg(box, S.busy ? 'Loading' : 'No stocks at this strength.'); return; }
    const wrap = el('div', 'rows');
    const cap = S.size === 's' && !S.wlAll ? 10 : list.length;
    list.slice(0, cap).forEach((r) => {
      const b = rowBtn('watch', r);
      const chip = r.nextRes && r.resDays !== null && r.resDays <= 5 ? 'Results ' + (r.resDays === 0 ? 'today' : r.resDays === 1 ? 'tomorrow' : shortDate(r.nextRes.date)) : null;
      const c = statusChip(r);
      const id = el('div', 'id');
      id.append(el('b', '', r.ticker));
      const sub = el('span', '', r.name);
      if (chip || c) { sub.replaceChildren(el('span', 'tag', chip || c.textContent)); }
      id.append(sub);
      b.append(id, sparkCell(r), scoreCell(r), pxCell(r));
      wrap.append(b);
    });
    box.replaceChildren(wrap);
    if (S.size === 's' && list.length > 10) { const m = btn('more', S.wlAll ? 'Show fewer' : 'Show all ' + list.length, () => { S.wlAll = !S.wlAll; draw(); }); m.style.padding = '0.5rem 1.125rem 0.25rem'; box.append(m); }
  };

  // ---------------------------------------------------------------- right rail
  const context = (rows, L) => {
    const box = q('#ctx-body');
    const by = {};
    L.filter((r) => r.table === 'macro').forEach((r) => { by[r.ticker] = r; });
    const sess = D.spy.length ? D.spy[D.spy.length - 1].date : null;
    const g = el('div', 'kv');
    let n = 0;
    const add = (name, value, chg, cc, date) => {
      const stale = sess && date && date < sess;
      const f = n === 0 ? ' fst' : ''; n += 1;
      const nm = span(f.trim(), name);
      g.append(nm, span('num b' + f + (stale ? ' faint' : ''), value), span('num' + f + ' ' + (cc || ''), chg));
    };
    if (D.spy.length > 1) { const a = D.spy[D.spy.length - 1]; const b = D.spy[D.spy.length - 2]; const c = (a.close / b.close - 1) * 100; add('S&P 500', '$' + fmt2(Number(a.close)), pct(c), dir(c), a.date); }
    [['us10y', 'US 10-year'], ['us2y', 'US 2-year'], ['uk10y', 'UK 10-year'], ['brent', 'Brent'], ['btc', 'Bitcoin']].forEach(([k, nm]) => {
      const r = by[k]; if (!r || num(r.value) === null) return;
      const v = num(r.value); const c = num(r.chg_1d);
      add(nm, r.kind === 'yield' ? v.toFixed(2) + '%' : '$' + (v >= 1000 ? fmt0(v) : fmt2(v)), r.kind === 'yield' ? bp(c) : pct(c, 1), r.kind === 'yield' ? 'mut' : dir(c), r.date);
    });
    box.replaceChildren(g);
  };
  const rail = (L) => {
    const heldNames = new Set(D.stocks.filter((r) => r.held).map((r) => r.name));
    const ev = L.filter((r) => r.table === 'event' && !eventPassed(r) && relevantEvent(r)).sort((a, b) => String(a.date).localeCompare(String(b.date))).slice(0, 6);
    q('#next-list').replaceChildren(...(ev.length ? ev.map((r) => agItem(shortDate(r.date) + (shortTime(r.time_uk) ? ', ' + shortTime(r.time_uk) : ''), r.name, null, [heldNames.has(r.stock) ? st('Held') : null, num(r.implied_pct) !== null ? span('mut', '±' + num(r.implied_pct) + '%') : null])) : [agItem('', 'No dated events ahead.')]));
    // Today's alerts rail: what bears on the holdings, not every mover on the list.
    const al = L.filter((r) => r.table === 'alert' && r.stock !== 'Order' && r.stock !== 'Watchlist' && (heldNames.has(r.stock) || ['Portfolio', 'Market', 'System'].includes(r.stock))).sort((a, b) => whenKey(b).localeCompare(whenKey(a)));
    const top = al.slice(0, 4);
    q('#alerts-list').replaceChildren(...(top.length ? top.map((r) => agItem(shortDate(r.date) + (r.time_uk ? ', ' + String(r.time_uk).replace(/\s*UK$/, '') : ''), r.stock || 'Market', el('small', '', String(r.text || '')))) : [agItem('', 'No alerts yet.')]));
  };

  // ---------------------------------------------------------------- research pane for one stock
  const chev = (d) => { const s = svgEl('svg', {viewBox: '0 0 16 16', 'aria-hidden': 'true'}); s.append(svgEl('path', {d})); return s; };
  const sec = (title, sub, ...kids) => { const s = el('section', 'rs-sec'); const h = el('h3', '', title); if (sub) h.append(span('', sub)); s.append(h, ...kids.filter(Boolean)); return s; };
  const fact = (k, v, cls, tip) => { const d = el('div'); const dt = el('dt', '', k); if (tip) { dt.append(document.createTextNode(' '), qmark(tip)); } d.append(dt, el('dd', cls || '', v)); return d; };
  const median = (a) => { const v = a.filter((x) => x !== null && x !== undefined && Number.isFinite(x)).sort((x, y) => x - y); if (!v.length) return null; const m = Math.floor(v.length / 2); return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2; };

  // Rules-based reading of the stored figures: what supports the case and what argues against it.
  const evidence = (r) => {
    const fo = []; const ag = [];
    const v50 = num(r.vs_50d_pct); const v200 = num(r.vs_200d_pct); const rsi = num(r.rsi); const up = num(r.upside_pct);
    if (tierOf(r) === 'strong') fo.push('Score ' + num(r.score) + ', strong'); else if (tierOf(r) === 'weak') ag.push('Score ' + num(r.score) + ', weak');
    if (v50 !== null && v200 !== null) { if (v50 > 0 && v200 > 0) fo.push('Above its 50-day (' + pct(v50, 1) + ') and 200-day (' + pct(v200, 1) + ') averages'); else if (v50 < 0) ag.push('Below its 50-day average (' + pct(v50, 1) + ')'); }
    if (r.ema_stack === 'up') fo.push('Exponential averages stacked upwards'); else if (r.ema_stack === 'down') ag.push('Exponential averages stacked downwards');
    if (r.rel20 !== null) (r.rel20 >= 0 ? fo : ag).push((r.rel20 >= 0 ? 'Beat' : 'Lagged') + ' the S&P 500 by ' + Math.abs(r.rel20).toFixed(1) + ' points over 20 sessions');
    if (rsi !== null && rsi >= 70) ag.push('RSI ' + rsi.toFixed(0) + ': overbought');
    if (num(r.catalyst_pts) !== null && r.catalyst_note && (num(r.catalyst_pts) >= 11 || num(r.catalyst_pts) <= 5)) (num(r.catalyst_pts) <= 5 ? ag : fo).push('Catalyst (' + num(r.catalyst_pts) + '/20): ' + r.catalyst_note);
    if (num(r.revisions_pts) !== null && r.revisions_note && (num(r.revisions_pts) >= 11 || num(r.revisions_pts) <= 5)) (num(r.revisions_pts) <= 5 ? ag : fo).push('Analysts (' + num(r.revisions_pts) + '/20): ' + r.revisions_note);
    if (up !== null) { if (up >= 10) fo.push('Consensus target ' + money(r, num(r.target)) + ', ' + pct(up, 0) + ' above the price'); else if (up < 0) ag.push('Price is above the consensus target (' + money(r, num(r.target)) + ')'); }
    if (r.nextRes && r.resDays !== null && r.resDays <= 10) { const w = r.held ? num(r.weight) : null; ag.push('Results ' + dateText(r.nextRes.date) + (r.implied !== null ? ': options imply ±' + r.implied + '%' + (w ? ', ' + (w * r.implied / 100).toFixed(2) + ' points at ' + wt(w) : '') : '')); }
    String(r.flags || '').split(';').map((x) => x.trim()).filter(Boolean).forEach((f) => { if (/below|downtrend|extended|overbought|faded|death|heavy-volume|bitcoin/i.test(f)) ag.push('Flag: ' + f); });
    if (r.crypto_link === 'yes') ag.push('Moves with Bitcoin: bought only while Bitcoin\'s trend is up, 10% at most');
    return {fo, ag};
  };

  const research = (L, rows) => {
    const pane = q('#research');
    const r = S.sel ? D.stocks.find((x) => x.name === S.sel) : null;
    const grid = q('#tgrid');
    if (!r) { pane.hidden = true; pane.replaceChildren(); grid.classList.remove('open'); root.dataset.focus = '0'; q('#rail').hidden = false; return; }
    pane.hidden = false;
    pane.tabIndex = -1;
    grid.classList.toggle('open', S.size === 'l');
    q('#rail').hidden = S.size === 'l';
    root.dataset.focus = S.size === 'l' ? '0' : '1';
    const list = D.stocks.map((x) => x.name);
    const at = list.indexOf(r.name);
    const kids = [];
    // bar
    const bar = el('div', 'rs-bar');
    const close = btn('btn', null, () => { const was = S.sel; S.sel = null; draw(); const n = Array.from(root.querySelectorAll('tr.sel, .row')).find((x) => (x.getAttribute('aria-label') || '').startsWith(was + ',')); if (n) n.focus(); });
    close.append(chev('M10 3 5 8l5 5'), document.createTextNode(S.size === 'l' ? 'Close' : 'Back'));
    const nav = el('div'); nav.style.display = 'flex'; nav.style.gap = '0.375rem';
    [['Previous stock', 'M10 3 5 8l5 5', at - 1], ['Next stock', 'M6 3l5 5-5 5', at + 1]].forEach(([lab, d, to]) => { const b = btn('btn', null, () => { S.sel = list[to]; draw(); }); b.setAttribute('aria-label', lab); b.append(chev(d)); if (to < 0 || to >= list.length) b.disabled = true; nav.append(b); });
    bar.append(close, nav);
    kids.push(bar);
    // header
    const h = el('div', 'rs-h');
    const id = el('div'); id.style.minWidth = '0';
    id.append(el('h2', '', r.ticker), el('div', 'sub', r.name));
    const px = el('div', 'rs-px'); px.append(el('b', '', money(r, num(r.price))), el('span', 'pill ' + dir(num(r.day_pct)), pct(num(r.day_pct))));
    h.append(logoFor(r.ticker, r.market, r.name, 'l'), id, px);
    kids.push(h);
    const tags = el('div', 'rs-tags');
    const chip0 = statusChip(r);
    if (chip0) tags.append(chip0);
    tags.append(scoreCell(r), bandEl(tierOf(r)));
    if (r.theme) tags.append(st(r.theme));
    if (r.conv !== null) tags.append(st('Conviction ' + r.conv, '', 'Confidence anchor from the latest nightly rating. Not calibrated: a ranking, not a chance of beating the S&P 500.'));
    kids.push(tags);
    // thesis and evidence
    const ev = evidence(r);
    const evb = el('div', 'ev');
    const col = (title, color, items, empty) => { const d = el('div'); const h4 = el('h4', '', title); const i = el('i'); i.style.background = color; h4.prepend(i); d.append(h4, items.length ? bullets(items, {small: true}) : el('p', 'note', empty)); return d; };
    evb.append(col('Supports the case', 'var(--up)', ev.fo, 'Nothing in the stored figures.'), col('Argues against', 'var(--down)', ev.ag, 'Nothing in the stored figures.'));
    kids.push(sec(r.held ? 'Why it is held' : 'Note', '', bullets(r.note) || el('p', 'note', 'No note logged.')));
    kids.push(sec('Evidence', '', evb));
    // relative performance chart
    const hist = D.byT.get(r.histT) || D.byT.get(r.ticker) || [];
    const spyAt = new Map(D.spy.map((x) => [x.date, Number(x.close)]));
    const spans = [[21, '1M'], [63, '3M'], [126, '6M'], [252, '1Y']].filter((o) => hist.length > o[0]);
    const pick = spans.filter((o) => o[0] <= S.range).pop() || spans[spans.length - 1] || null;
    let after = () => {};
    if (pick) {
      const win = hist.slice(-pick[0] - 1).filter((x) => spyAt.has(x.date));
      const b0 = Number(win[0].close); const s0 = spyAt.get(win[0].date);
      const cr = win.map((x) => ({date: x.date, stock: Number(x.close) / b0 * 100, spx: spyAt.get(x.date) / s0 * 100}));
      const head = el('div'); head.style.display = 'flex'; head.style.flexWrap = 'wrap'; head.style.justifyContent = 'space-between'; head.style.gap = '0.375rem';
      const lg = el('ul', 'lg'); [[r.ticker + (r.histT !== r.ticker ? ' (US line)' : ''), 'var(--s1)'], ['S&P 500', 'var(--bench)']].forEach(([n, c]) => { const li = el('li'); const sw = span('sw'); sw.style.background = c; li.append(sw, document.createTextNode(n)); lg.append(li); });
      const seg = el('div', 'seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'Chart window');
      spans.forEach((o) => { const b = btn('', o[1], () => { S.range = o[0]; draw(); }); b.setAttribute('aria-pressed', o[0] === pick[0] ? 'true' : 'false'); seg.append(b); });
      head.append(lg, seg);
      const box = el('div', 'ch');
      const last = cr[cr.length - 1];
            kids.push(sec('Against the S&P 500', pct(last.stock - 100, 1) + ' and ' + pct(last.spx - 100, 1), head, box));
      after = () => lineChart(box, cr, [{key: 'stock', name: r.ticker, color: 'var(--s1)'}, {key: 'spx', name: 'S&P 500', color: 'var(--bench)', width: 1.25}], {height: S.size === 's' ? 170 : 190, ref: 100, label: r.name + ' against the S&P 500, both set to 100 at the start of the window', yfmt: (t) => t.toFixed(0), vfmt: (v) => v.toFixed(1), xfmt: (x) => shortDate(x.date), xlong: (x) => dateText(x.date)});
    }
    // catalysts
    const t0 = today();
    const evs = D.events.filter((x) => x.stock === r.name);
    const tl = [];
    evs.forEach((x) => tl.push({date: x.date, what: x.name, body: [x.implied_pct ? 'Options imply ±' + x.implied_pct + '%' : '', lastOrderText(x) ? 'Last order: ' + lastOrderText(x) : '', x.plan ? 'Plan: ' + x.plan : ''].filter(Boolean).join('. '), kind: 'Event'}));
    (D.revBy.get(r.name) || []).forEach((x) => tl.push({date: x.date, what: x.bank + ': ' + x.action, body: x.text, kind: 'Analyst'}));
    L.filter((x) => x.table === 'trade' && x.name === r.name).forEach((x) => tl.push({date: x.effective, what: 'Order: ' + wt(num(x.from_w)) + ' to ' + wt(num(x.to_w)), body: '', kind: 'Order'}));
    L.filter((x) => x.table === 'alert' && x.stock === r.name).forEach((x) => tl.push({date: x.date, what: 'Alert, ' + (x.time_uk || ''), body: x.text, kind: 'Alert'}));
    const ahead = tl.filter((x) => String(x.date) >= t0).sort((a, b) => String(a.date).localeCompare(String(b.date)));
    const behind = tl.filter((x) => String(x.date) < t0).sort((a, b) => String(b.date).localeCompare(String(a.date))).slice(0, 6);
    const ul = el('ul', 'ag');
    ahead.concat(behind).forEach((x) => ul.append(agItem(shortDate(x.date) + ', ' + (String(x.date) >= t0 ? relDay(x.date) : x.kind), x.what, x.body ? bullets(x.body, {small: true, max: 1}) : null)));
    kids.push(sec('Timeline', '', tl.length ? ul : el('p', 'note', 'No events, analyst changes or alerts logged for this stock.')));
    // technicals
    const facts = el('dl', 'facts');
    const rsi = num(r.rsi);
    facts.append(
      fact('vs 50-day', pct(num(r.vs_50d_pct), 1), dir(num(r.vs_50d_pct))), fact('vs 200-day', pct(num(r.vs_200d_pct), 1), dir(num(r.vs_200d_pct))), fact('RSI (14)', rsi === null ? '—' : rsi.toFixed(0) + (rsi >= 70 ? ', overbought' : rsi <= 30 ? ', oversold' : '')),
      fact('5 sessions', pct(num(r.five_day_pct), 1), dir(num(r.five_day_pct))), fact('Gap at open', pct(num(r.gap_pct)), dir(num(r.gap_pct)), 'Previous close to open. Orders fill at the open, so the gap cannot be captured.'), fact('Open to close', pct(num(r.from_open_pct)), dir(num(r.from_open_pct))),
      fact('Averages', r.ema_stack === 'up' ? 'Stacked up' : r.ema_stack === 'down' ? 'Stacked down' : r.ema_stack ? 'Mixed' : '—'), fact('Cross', r.cross ? String(r.cross).replace(/ on (\d{4}-\d{2}-\d{2})/, (a, d0) => ', ' + shortDate(d0)) : 'None'), fact('Target', num(r.target) === null ? '—' : money(r, num(r.target))),
    );
    const lo = num(r.week52_low); const hi = num(r.week52_high); const p0 = num(r.price);
    let range = null;
    if (lo !== null && hi !== null && p0 !== null && hi > lo) {
      range = el('div', 'range');
      const t = el('div', 'range-t'); t.append(span('', money(r, lo)), span('', '52 weeks, ' + pct(num(r.off_high_pct), 1) + ' from the high'), span('', money(r, hi)));
      const k = el('div', 'range-k'); k.setAttribute('aria-hidden', 'true'); const d = el('i'); d.style.left = Math.max(0, Math.min(100, (p0 - lo) / (hi - lo) * 100)) + '%'; k.append(d);
      range.append(t, k);
    }
    const sc = el('div', 'bars');
    bars(sc, [['Trend', num(r.trend_pts), 40], ['Recent behaviour', num(r.short_pts), 20], ['Catalyst', num(r.catalyst_pts), 20], ['Analyst changes', num(r.revisions_pts), 20]].map(([l, v, m]) => ({label: l, value: v === null ? null : v / m * 100, text: (v === null ? '—' : v) + ' / ' + m})), {min: 100});
    kids.push(sec('Technicals', '', facts, range));
    kids.push(sec('Score ' + (num(r.score) === null ? '—' : num(r.score)) + ' of 100', '', sc));
    // risk
    const rk = el('dl', 'facts');
    const riskRow = L.find((x) => x.table === 'risk' && x.name === r.name);
    rk.append(
      fact('Daily range', num(r.atr_pct) === null ? '—' : num(r.atr_pct).toFixed(1) + '%', '', 'Average true range: a typical day\'s move.'),
      fact('Weight', r.held ? wt(num(r.weight)) : 'Not held'), fact('Share of risk', riskRow && num(riskRow.risk_share_pct) !== null ? num(riskRow.risk_share_pct).toFixed(0) + '%' : '—'),
      fact('Per 1% in Bitcoin', num(r.btc_beta) === null ? '—' : pct(num(r.btc_beta), 2), '', 'Move that has gone with a 1% move in Bitcoin over 120 sessions.'), fact('Results', r.nextRes ? shortDate(r.nextRes.date) + (r.implied !== null ? ', ±' + r.implied + '%' : '') : '—'),
    );
    const pairs = L.filter((x) => x.table === 'corr' && String(x.name).split(' / ').includes(r.name)).sort((a, b) => num(b.value) - num(a.value));
    kids.push(sec('Risk', '', rk, pairs.length ? bullets(pairs.map((x) => 'Correlation with ' + String(x.name).split(' / ').find((n) => n !== r.name) + ': ' + num(x.value).toFixed(2) + (num(x.value) > 0.85 ? ', moves in step' : '')), {small: true}) : null));
    // comparison with holdings
    const held = D.stocks.filter((x) => x.held && x.name !== r.name);
    if (held.length) {
      const m = (f) => median(held.map(f));
      const rowsC = [
        ['Score', num(r.score), m((x) => num(x.score)), (v) => (v === null ? '—' : v.toFixed(0))],
        ['vs S&P 500, 20d', r.rel20, m((x) => x.rel20), (v) => pts(v, 1)],
        ['5 sessions', num(r.five_day_pct), m((x) => num(x.five_day_pct)), (v) => pct(v, 1)],
        ['vs 50-day average', num(r.vs_50d_pct), m((x) => num(x.vs_50d_pct)), (v) => pct(v, 1)],
        ['RSI', num(r.rsi), m((x) => num(x.rsi)), (v) => (v === null ? '—' : v.toFixed(0))],
        ['Daily range', num(r.atr_pct), m((x) => num(x.atr_pct)), (v) => (v === null ? '—' : v.toFixed(1) + '%')],
        ['Conviction', r.conv, m((x) => x.conv), (v) => (v === null ? '—' : v.toFixed(0))],
      ];
      const tb = el('div');
      table(tb, [{h: 'Measure', cell: (x) => x[0]}, {h: r.ticker, num: true, cls: 'b', cell: (x) => x[3](x[1])}, {h: 'Median', num: true, cell: (x) => x[3](x[2])}], rowsC, {size: 'l'});
      const s2 = sec('Against the holdings', '', tb);
      s2.style.paddingLeft = '0'; s2.style.paddingRight = '0';
      s2.firstChild.style.padding = '0 1.125rem';
      kids.push(s2);
    }
    if (r.link) { const a = el('a', 'btn', 'Open live quote'); a.href = r.link; a.target = '_blank'; a.rel = 'noopener'; const s3 = el('section', 'rs-sec'); a.style.alignSelf = 'flex-start'; s3.append(a); kids.push(s3); }
    pane.replaceChildren(...kids);
    after();
  };

  // ---------------------------------------------------------------- macro
  const calBanner = (box, settled, what) => {
    box.replaceChildren();
    const b = el('b', '', 'Not calibrated. ');
    // 19 Oct evening: the banner no longer hides itself at CALIB_TARGET. A count of ratings is not evidence: ratings
    // made on the same few dates share one market move. It stays until Tim agrees the ratings may be read as probabilities.
    box.append(b, document.createTextNode(settled + ' settled ' + what + '. A ranking, not a measured probability.'));
    box.hidden = false;
  };
  const drawMacro = (L) => {
    const M = L.filter((r) => r.table === 'macro');
    const by = {}; M.forEach((r) => { by[r.ticker] = r; });
        const calls = L.filter((r) => r.table === 'daycall').sort((a, b) => String(a.date).localeCompare(String(b.date)));
    const hd = dash.data('history');
    const H = hd.status === 'ok' ? hd.data : [];
    const v = S.view.macro;
    if (v === 'call') {
      const open = calls.filter((r) => num(r.ret_pct) === null);
      const target = open.length ? open[open.length - 1].date : null;
      const now = open.filter((r) => r.date === target);
      const spx = now.find((r) => r.name === 'S&P 500') || null;
      const done = calls.filter((r) => r.beat === 'yes' || r.beat === 'no');
      calBanner(q('#call-cal'), done.filter((r) => r.name === 'S&P 500').length, 'calls');
      q('#call-for').textContent = target ? 'for ' + dateText(target) : '';
      const cards = q('#call-cards');
      if (!now.length) msg(cards, 'No open call. Each evening review makes one.');
      else cards.replaceChildren(...['S&P 500', 'Portfolio'].map((nm) => {
        const r = now.find((x) => x.name === nm);
        const c = el('div');
        c.append(el('div', 'note', nm));
        if (!r) { c.append(el('div', 'call-n flat', '—'), el('p', 'note', 'No figure: under 70% of the weight has a year of stored prices.')); return c; }
        const p = num(r.confidence); const u = num(r.percentile);
        const n = el('div', 'call-n ' + (r.kind === 'green' ? 'up' : 'down'), (r.kind === 'green' ? 'Up ' : 'Down ') + p + '%');
        n.append(el('small', 'mut', 'usual ' + Math.round(u) + '%'));
        const mt = el('div', 'meter'); mt.setAttribute('aria-hidden', 'true'); const f = el('i'); f.style.width = p + '%'; const mk = el('b'); mk.style.left = u + '%'; mt.append(f, mk);
        const adj = (num(r.adj_eve) || 0) + (num(r.adj_morn) || 0);
        c.append(n, mt, bullets([Math.abs(p - u) < 3 ? 'Within 3 points of the usual rate: no real edge' : Math.abs(p - u).toFixed(0) + ' points ' + (p > u ? 'above' : 'below') + ' the usual rate', 'Model ' + num(r.score).toFixed(0) + '%' + (adj ? ', reviewer ' + (adj > 0 ? '+' : '') + adj : ', no reviewer adjustment'), r.action ? String(r.action).charAt(0).toUpperCase() + String(r.action).slice(1) : ''], {small: true}));
        return c;
      }));
      q('#call-why').textContent = spx && spx.lesson ? spx.lesson : '';
      q('#case-bull').replaceChildren(spx && spx.text ? bullets(spx.text) : el('p', 'note', 'No case written.'));
      q('#case-bear').replaceChildren(spx && spx.plan ? bullets(spx.plan) : el('p', 'note', 'No case written.'));
      table(q('#analog'), [
        {h: 'After days when', cls: 'wrap', cell: (r) => String(r.name).replace(/^After days when /, '')},
        {h: 'For', only: ['m', 'l'], cell: (r) => r.stock},
        {h: 'Days', num: true, cell: (r) => num(r.days)},
        {h: 'Rose next day', num: true, cls: 'b', cell: (r) => (num(r.percentile) === null ? '—' : num(r.percentile) + '%')},
        {h: 'Average', num: true, cell: (r) => [pct(num(r.value)), dir(num(r.value))]},
        {h: 'Leans', only: ['m', 'l'], cell: (r) => (r.kind === 'bull' ? 'Up' : r.kind === 'bear' ? 'Down' : 'Neither')},
      ], L.filter((r) => r.table === 'analog').sort((a, b) => String(b.date).localeCompare(String(a.date))).filter((r, i, a) => r.date === a[0].date), {empty: 'No evidence stored yet.'});
      const sd = done.filter((r) => r.name === 'S&P 500');
      q('#call-sum').textContent = sd.length ? 'S&P 500 ' + sd.filter((r) => r.beat === 'yes').length + ' of ' + sd.length + ' right; always up ' + sd.filter((r) => num(r.ret_pct) > 0).length : '';
      table(q('#call-rec'), [
        {h: 'Session', cell: (r) => shortDate(r.date)},
        {h: 'For', cell: (r) => r.name},
        {h: 'Call', cell: (r) => [(r.kind === 'green' ? 'Up ' : 'Down ') + num(r.confidence) + '%', r.kind === 'green' ? 'up' : 'down']},
        {h: 'Outcome', num: true, cell: (r) => [pct(num(r.ret_pct)), dir(num(r.ret_pct))]},
        {h: 'Right?', cell: (r) => st(r.beat === 'yes' ? 'Right' : 'Wrong', r.beat === 'yes' ? 'okay' : 'bad')},
      ], done.slice().reverse(), {empty: 'The first call settles after the next session.'});
    }
    if (v === 'rates') {
      const bd = by.backdrop;
      const bdb = q('#backdrop'); bdb.replaceChildren(); if (bd) bdb.append(document.createTextNode('Backdrop '), el('b', '', String(bd.action || '—')));
      const series = M.filter((r) => ['yield', 'commodity', 'spread'].includes(r.kind));
      const sess = D.spy.length ? D.spy[D.spy.length - 1].date : null;
      const val = (r, x) => (x === null ? '—' : r.kind === 'yield' ? x.toFixed(2) + '%' : r.kind === 'spread' ? x.toFixed(0) + 'bp' : '$' + fmt2(x));
      const ch = (r, f) => { const x = num(r[f]); return r.unit === 'bp' ? bp(x) : [pct(x, 1), dir(x)]; };
      const rateCols = (first) => [
        {h: first, cell: (r) => String(r.name).replace(/, \$.*$/, '').replace(/ 10-year( gilt)? yield$/, ' 10-year').replace(/ yield$/, '')},
        {h: 'Last', num: true, cls: 'b', cell: (r) => [val(r, num(r.value)) + (sess && r.date < sess ? ', ' + shortDate(r.date) : ''), sess && r.date < sess ? 'faint' : '']},
        {h: '1 day', num: true, cell: (r) => ch(r, 'chg_1d')},
        {h: '5 days', num: true, cell: (r) => ch(r, 'chg_5d')},
      ];
      table(q('#rates'), rateCols('Bond'), series.filter((r) => r.kind === 'yield'), {empty: 'No readings stored yet.'});
      table(q('#rates2'), rateCols('Series'), series.filter((r) => r.kind !== 'yield'), {empty: 'No readings stored yet.'});
      const md = dash.data('macro');
      const mrows = md.status === 'ok' ? md.data : [];
      const byDate = {};
      mrows.forEach((r) => { if (['us10y', 'us2y', 'uk10y'].includes(r.series)) { byDate[r.date] = byDate[r.date] || {date: r.date, us10y: null, us2y: null, uk10y: null}; byDate[r.date][r.series] = Number(r.value); } });
      const yr = Object.values(byDate).sort((a, b) => String(a.date).localeCompare(String(b.date))).slice(-252);
      const ys = [{key: 'us10y', name: 'US 10-year', color: 'var(--s1)'}, {key: 'us2y', name: 'US 2-year', color: 'var(--s2)', width: 1.25}, {key: 'uk10y', name: 'UK 10-year', color: 'var(--s3)', width: 1.25}];
      q('#lg-y').replaceChildren(...ys.map((s) => { const li = el('li'); const sw = span('sw'); sw.style.background = s.color; li.append(sw, document.createTextNode(s.name)); return li; }));
      if (md.status === 'error') msg(q('#ch-yields'), '', true); else lineChart(q('#ch-yields'), yr, ys, {height: 200, label: 'Government bond yields over the past year', yfmt: (t) => t.toFixed(1) + '%', vfmt: (x) => x.toFixed(2) + '%', xfmt: (r) => shortDate(r.date), xlong: (r) => dateText(r.date), empty: 'Appears once yields are stored.'});
      const oil = H.filter((r) => r.ticker === 'OIL').sort((a, b) => String(a.date).localeCompare(String(b.date))).slice(-252);
      if (oil.length > 4) { const b0 = Number(oil[0].close); lineChart(q('#ch-oil'), oil.map((r) => ({date: r.date, v: Number(r.close) / b0 * 100})), [{key: 'v', name: 'Brent index', color: 'var(--s1)'}], {height: 200, ref: 100, label: 'Brent oil return index over the past year', yfmt: (t) => t.toFixed(0), vfmt: (x) => x.toFixed(1), xfmt: (r) => shortDate(r.date), xlong: (r) => dateText(r.date)}); } else msg(q('#ch-oil'), hd.status === 'error' ? '' : 'Appears once oil prices are stored.', hd.status === 'error');
      const sens = M.filter((r) => r.kind === 'sensitivity');
      const drivers = [];
      sens.forEach((r) => { const k = String(r.name).split('gone with ')[1] || r.name; if (!drivers.includes(k)) drivers.push(k); });
      const pick = (k, w) => sens.find((r) => String(r.name).startsWith(w + ':') && String(r.name).endsWith(k));
      table(q('#sens'), [
        {h: 'With', cell: (k) => k.charAt(0).toUpperCase() + k.slice(1)},
        {h: 'Portfolio', num: true, cls: 'b', cell: (k) => { const r = pick(k, 'Portfolio'); return r ? [pct(num(r.value)), dir(num(r.value))] : '—'; }},
        {h: 'S&P 500', num: true, cell: (k) => { const r = pick(k, 'S&P 500'); return r ? [pct(num(r.value)), dir(num(r.value))] : '—'; }},
      ], drivers, {empty: 'Needs 30 sessions of prices for most of the portfolio.'});
    }
    if (v === 'crypto') {
      const coins = M.filter((r) => r.kind === 'crypto');
      table(q('#coins'), [
        {h: 'Coin', cell: (r) => String(r.name).replace(/, \$.*$/, '')},
        {h: 'Price', num: true, cls: 'b', cell: (r) => { const x = num(r.value); return x === null ? '—' : '$' + (x >= 1000 ? fmt0(x) : x >= 10 ? fmt2(x) : x.toFixed(4)); }},
        {h: '1 day', num: true, cell: (r) => [pct(num(r.chg_1d), 1), dir(num(r.chg_1d))]},
        {h: '5 days', num: true, cell: (r) => [pct(num(r.chg_5d), 1), dir(num(r.chg_5d))]},
        {h: '20 days', num: true, cell: (r) => [pct(num(r.chg_20d), 1), dir(num(r.chg_20d))]},
      ], coins, {empty: 'No coin prices stored yet.'});
      q('#coin-read').replaceChildren(bullets(M.filter((r) => r.kind === 'crypto-trend').map((r) => String(r.name) + ': ' + String(r.action || '—') + '. ' + String(r.text || '').split(';')[0]).concat(['Orders fill at the open, so an overnight move in Bitcoin is already in the fill price. The trend is what counts.']), {small: true}) || el('p', 'note', ''));
      const ib = H.filter((r) => r.ticker === 'IBIT').sort((a, b) => String(a.date).localeCompare(String(b.date))).slice(-252);
      if (ib.length > 4) { const b0 = Number(ib[0].close); lineChart(q('#ch-btc'), ib.map((r) => ({date: r.date, v: Number(r.close) / b0 * 100})), [{key: 'v', name: 'Bitcoin index', color: 'var(--s2)'}], {height: 200, ref: 100, label: 'Bitcoin return index over the past year', yfmt: (t) => t.toFixed(0), vfmt: (x) => x.toFixed(1), xfmt: (r) => shortDate(r.date), xlong: (r) => dateText(r.date)}); } else msg(q('#ch-btc'), 'Appears once the Bitcoin fund\'s prices are stored.');
      const links = D.stocks.filter((r) => num(r.btc_beta) !== null && num(r.btc_corr) !== null).sort((a, b) => (b.crypto_link === 'yes') - (a.crypto_link === 'yes') || num(b.btc_corr) - num(a.btc_corr)).slice(0, 10);
      table(q('#btc-links'), [
        {h: 'Stock', cell: stkCell},
        {h: 'Status', cell: (r) => (r.held ? st('Held ' + wt(num(r.weight))) : r.crypto_link === 'yes' ? st('Linked', 'warn', 'Correlation of 0.5 or more with Bitcoin, or a crypto business.') : '')},
        {h: 'Per 1% in Bitcoin', num: true, cls: 'b', cell: (r) => [pct(num(r.btc_beta), 2), dir(num(r.btc_beta))]},
        {h: 'Correlation', num: true, cell: (r) => num(r.btc_corr).toFixed(2)},
        {h: 'Net of market', num: true, only: ['m', 'l'], cell: (r) => pct(num(r.btc_net), 2)},
      ], links, {onRow: (r) => { S.page = 'today'; show('today', true); open(r); }, label: (r) => r.name + ', open research'});
    }
    if (v === 'releases') {
      const t0 = today();
      const rel = L.filter((r) => r.table === 'event' && r.kind === 'macro' && (r.forecast || r.actual || r.previous || String(r.date) < t0)).sort((a, b) => String(b.date).localeCompare(String(a.date)));
      const fig = (x, full) => { const c = cleanFig(x); if (!c) return '—'; const s = span('', c); if (full && full !== c) { s.dataset.tip = full; s.tabIndex = 0; } return s; };
      table(q('#releases'), [
        {h: 'When', cls: 'nowrap', cell: (r) => shortDate(r.date)},
        {h: 'Release', cls: 'wrap b', cell: (r) => r.name},
        {h: 'Forecast', cls: 'wrap', only: ['m', 'l'], cell: (r) => fig(r.forecast, r.forecast)},
        {h: 'Previous', cls: 'wrap', only: ['l'], cell: (r) => fig(r.previous, r.previous)},
        {h: 'Actual', cls: 'wrap', cell: (r) => (r.actual ? fig(r.actual, r.actual + (r.surprise ? ' (' + r.surprise + ')' : '')) : String(r.date) >= t0 ? st('Due') : '—')},
        {h: 'S&P 500', num: true, only: ['m', 'l'], cell: (r) => [pct(num(r.spx_ret_pct)), dir(num(r.spx_ret_pct))]},
        {h: 'US 10y', num: true, only: ['l'], cell: (r) => bp(num(r.chg_1d))},
      ], rel, {empty: 'No releases stored yet.'});
    }
  };

  // ---------------------------------------------------------------- performance
  const drawPerformance = (L) => {
    const v = S.view.performance;
    if (v === 'overview') {
      const ix = dash.data('indexed');
      const rows = ix.status === 'ok' ? ix.data : [];
      if (ix.status === 'error') msg(q('#ch-value'), '', true);
      else if (rows.length < 2) msg(q('#ch-value'), 'Starts after the first completed session.');
      else lineChart(q('#ch-value'), rows, [{key: 'portfolio', name: 'Portfolio', color: 'var(--s1)'}, {key: 'sp500', name: 'S&P 500', color: 'var(--bench)', width: 1.25}], {height: 230, ref: 100, dots: ['reported'], dotName: 'FT site', label: 'Portfolio estimate and the S&P 500 since the start, both 100 at the start', yfmt: (t) => t.toFixed(1), vfmt: (x) => x.toFixed(2), xfmt: (r) => (r.date === 'Start' ? 'Start' : shortDate(r.date)), xlong: (r) => (r.date === 'Start' ? 'Start, Fri 9 Oct open' : dateText(r.date))});
      let peak = -Infinity;
      const dd = rows.map((r) => { peak = Math.max(peak, r.portfolio); return {date: r.date, dd: (r.portfolio / peak - 1) * 100}; });
      if (rows.length < 2) msg(q('#ch-dd'), 'Starts after the first completed session.');
      else lineChart(q('#ch-dd'), dd, [{key: 'dd', name: 'Drawdown', color: 'var(--down)', area: true}], {height: 170, ref: 0, areaBase: 0, label: 'Drawdown of the estimated portfolio value from its running peak', yfmt: (t) => t.toFixed(1) + '%', vfmt: (x) => pct(x), xfmt: (r) => (r.date === 'Start' ? 'Start' : shortDate(r.date)), xlong: (r) => (r.date === 'Start' ? 'Start' : dateText(r.date))});
      const rep = L.filter((r) => r.table === 'reported' && num(r.percentile) !== null).sort((a, b) => whenKey(a).localeCompare(whenKey(b)));
      if (rep.length < 2) msg(q('#ch-rank'), 'Needs two ranks read off the FT site.');
      else lineChart(q('#ch-rank'), rep.map((r) => ({date: r.date, t: r.time_uk, p: num(r.percentile), rank: num(r.rank), players: num(r.players)})), [{key: 'p', name: 'Top', color: 'var(--s1)'}], {height: 170, ref: 2, refLabel: 'Target: top 2%', floor: 0, invert: true, label: 'Leaderboard position as a percentage of players over time', yfmt: (t) => t.toFixed(0) + '%', vfmt: (x) => x.toFixed(1) + '%', xfmt: (r) => shortDate(r.date), xlong: (r) => dateText(r.date) + ' ' + (r.t || '') + ': rank ' + fmt0(r.rank) + ' of ' + fmt0(r.players)});
      const ct = dash.data('contrib_total');
      bars(q('#contrib'), (ct.status === 'ok' ? ct.data : []).map((r) => ({label: r.name, detail: r.sessions + (r.sessions === 1 ? ' session' : ' sessions'), value: r.contrib_pts, text: pts(r.contrib_pts)})), {diverging: true, min: 0.1, empty: 'Appears after the first completed session.'});
      const pos = L.filter((r) => r.table === 'position');
      const theme = new Map(D.stocks.map((s) => [s.name, s.theme]));
      L.filter((r) => r.table === 'risk' && r.theme).forEach((r) => { if (!theme.has(r.name)) theme.set(r.name, r.theme); });
      const effs = Array.from(new Set(pos.map((r) => r.effective))).sort();
      const state = new Map(); const snaps = [];
      effs.forEach((e) => { pos.filter((r) => r.effective === e).forEach((r) => state.set(r.name, num(r.weight))); const t = {}; state.forEach((w, n) => { if (w > 0) { const k = theme.get(n) || 'Other'; t[k] = (t[k] || 0) + w; } }); snaps.push({e, t}); });
      const themes = Array.from(new Set(snaps.flatMap((s) => Object.keys(s.t)))).sort((a, b) => (snaps[snaps.length - 1].t[b] || 0) - (snaps[snaps.length - 1].t[a] || 0));
      const lastSnaps = snaps.slice(-(S.size === 's' ? 3 : 5));
      table(q('#expo'), [{h: 'Theme', cell: (t) => t}].concat(lastSnaps.map((s, i) => ({h: shortDate(s.e), num: true, cls: i === lastSnaps.length - 1 ? 'b' : '', cell: (t) => (s.t[t] ? wt(s.t[t]) : '—')}))), themes, {empty: 'No positions logged yet.'});
      table(q('#daily'), [
        {h: 'Session', cell: (r) => dateText(r.date)},
        {h: 'Day', num: true, cls: 'b', cell: (r) => [pct(num(r.day_pct)), dir(num(r.day_pct))]},
        {h: 'Value', num: true, cell: (r) => fmt0(num(r.value_est))},
        {h: 'Since start', num: true, cell: (r) => [pct(num(r.cum_pct)), dir(num(r.cum_pct))]},
        {h: 'S&P 500', num: true, cell: (r) => [pct(num(r.spx_cum_pct)), dir(num(r.spx_cum_pct))]},
        {h: 'Ahead', num: true, only: ['m', 'l'], cell: (r) => { const g = num(r.cum_pct) - num(r.spx_cum_pct); return [pts(g) + ' pts', dir(g)]; }},
      ], L.filter((r) => r.table === 'perf').sort((a, b) => String(b.date).localeCompare(String(a.date))), {empty: 'The first row appears after the first completed session.'});
    }
    if (v === 'ratings') {
      const conf = L.filter((r) => r.table === 'confidence').sort((a, b) => String(b.effective).localeCompare(String(a.effective)) || num(b.confidence) - num(a.confidence));
      const settled = conf.filter((r) => r.beat === 'yes' || r.beat === 'no').length;
      calBanner(q('#rate-cal'), settled, 'ratings');
      const cb = dash.data('conf_bands');
      table(q('#bands'), [
        {h: 'Rating', cls: 'b', cell: (r) => r.band}, {h: 'Rated', num: true, cell: (r) => r.rated}, {h: 'Settled', num: true, cell: (r) => r.resolved},
        {h: 'Beat', num: true, cell: (r) => (r.resolved ? r.beat : '—')}, {h: 'Hit rate', num: true, cls: 'b', cell: (r) => (r.hit_rate === null ? '—' : r.hit_rate + '%')},
      ], cb.status === 'ok' ? cb.data : []);
      q('#conf-meta').textContent = conf.length + ' ratings, ' + (conf.length - settled) + ' still open';
      table(q('#conf'), [
        {h: 'Stock', cell: (r) => { const s = D.stocks.find((x) => x.name === r.name) || {}; const w = el('div', 'stk'); w.append(logoFor(r.ticker, s.market, r.name, 's'), span('', r.name)); return w; }},
        {h: 'Rating', num: true, cls: 'b', cell: (r) => num(r.confidence)},
        {h: 'Score', num: true, only: ['m', 'l'], cell: (r) => num(r.score)},
        {h: 'Window', cls: 'nowrap', cell: (r) => (r.window_end ? shortDate(r.effective) + ' to ' + shortDate(r.window_end) : 'from ' + shortDate(r.effective))},
        {h: 'Return', num: true, only: ['l'], cell: (r) => [pct(num(r.ret_pct)), dir(num(r.ret_pct))]},
        {h: 'S&P 500', num: true, only: ['l'], cell: (r) => [pct(num(r.spx_ret_pct)), dir(num(r.spx_ret_pct))]},
        {h: 'Beat it?', cell: (r) => (r.beat === 'yes' ? st('Yes', 'okay') : r.beat === 'no' ? st('No', 'bad') : st('Open'))},
      ], conf, {empty: 'No ratings logged yet.'});
    }
    if (v === 'score') {
      const cal = L.filter((r) => r.table === 'calib');
      const live = cal.filter((r) => r.kind === 'live');
      const settled = live.reduce((t, r) => t + (num(r.days) || 0), 0);
      calBanner(q('#calib-cal'), settled, 'shadow ratings');
      const cols = (first, n) => [{h: first, cls: 'b', cell: (r) => r.name}, {h: n, num: true, cell: (r) => num(r.days) || 0}, {h: 'Beat index', num: true, cell: (r) => (num(r.percentile) === null ? '—' : num(r.percentile) + '%')}, {h: 'Avg gap', num: true, cell: (r) => [pts(num(r.value)), dir(num(r.value))]}];
      table(q('#calib-live'), cols('Score band', 'Settled'), live, {empty: 'The first ratings settle five sessions after they are made.'});
      const back = cal.filter((r) => r.kind === 'backtest');
      table(q('#calib-back'), cols('Price-only points', 'Stock-days'), back, {empty: 'Needs stocks with a year of stored prices.'});
      const sum = cal.find((r) => r.kind === 'backtest-summary');
      const cover = back.map((r) => r.text).filter(Boolean)[0] || '';
      q('#calib-sum').replaceChildren(bullets([cover ? cover.charAt(0).toUpperCase() + cover.slice(1) : ''].concat(sum ? sentences(sum.text).flatMap((x) => x.split(/;\s+/)) : []).map((x) => x.replace(/\.$/, '')), {small: true}) || el('p', 'note', ''));
    }
  };

  // ---------------------------------------------------------------- risk
  const drawRisk = (L) => {
    const th = L.filter((r) => r.table === 'theme').filter((r) => num(r.weight) > 0).sort((a, b) => num(b.weight) - num(a.weight));
    bars(q('#themes'), th.map((r) => ({label: r.name, value: num(r.weight), text: wt(num(r.weight))})), {min: 100, empty: 'No holdings.'});
    const sc = L.filter((r) => r.table === 'scenario').sort((a, b) => num(a.impact_pct) - num(b.impact_pct));
    bars(q('#scen'), sc.map((r) => ({label: r.name, value: num(r.impact_pct), text: pts(num(r.impact_pct))})), {diverging: true, min: 1, empty: 'No scenarios stored.'});
    const risk = L.filter((r) => r.table === 'risk').sort((a, b) => (num(b.risk_share_pct) ?? -99) - (num(a.risk_share_pct) ?? -99));
    const top = Math.max(1, ...risk.map((r) => Math.max(num(r.weight) || 0, num(r.risk_share_pct) || 0)));
    table(q('#riskshare'), [
      {h: 'Stock', cell: (r) => r.name},
      {h: 'Weight', num: true, cell: (r) => wt(num(r.weight))},
      {h: 'Risk', num: true, cls: 'b', cell: (r) => { const s = num(r.risk_share_pct); const w = num(r.weight); return [s === null ? '—' : s.toFixed(0) + '%', s !== null && s > w * 1.5 ? 'down' : '']; }},
      {h: '', cell: (r) => { const d = el('div', 'duo' + (num(r.risk_share_pct) > num(r.weight) * 1.5 ? ' hot' : '')); d.style.minWidth = '4rem'; const a = el('i'); a.style.width = num(r.weight) / top * 100 + '%'; const b = el('i'); b.style.width = (num(r.risk_share_pct) || 0) / top * 100 + '%'; d.append(a, b); return d; }},
      {h: 'Typical day', num: true, only: ['m', 'l'], cell: (r) => (num(r.vol_pct) === null ? '—' : num(r.vol_pct).toFixed(2) + '%')},
    ], risk, {empty: 'Needs 15 sessions of prices for every holding.'});
    table(q('#corr'), [{h: 'Pair', cell: (r) => r.name}, {h: 'Correlation', num: true, cls: 'b', cell: (r) => num(r.value).toFixed(2)}, {h: '', cell: (r) => (num(r.value) > 0.85 ? st('In step', 'warn', 'Above 0.85: the pair behaves like one position.') : '')}], L.filter((r) => r.table === 'corr').sort((a, b) => num(b.value) - num(a.value)), {empty: 'Needs 15 sessions of prices.'});
    const rr = dash.data('results_risk');
    const t0 = today();
    table(q('#rrisk'), [
      {h: 'Stock', cell: (r) => r.stock}, {h: 'Results', cell: (r) => shortDate(r.date)}, {h: 'Weight', num: true, only: ['m', 'l'], cell: (r) => wt(r.weight)},
      {h: 'Expected move', num: true, cell: (r) => (r.implied_pct === null ? 'Not priced yet' : '±' + r.implied_pct + '%')},
      {h: 'At risk', num: true, cls: 'b', tip: 'Weight × options-implied move. The results budget is suspended under the endgame stance: this is information.', cell: (r) => (r.risk_pts === null ? '—' : r.risk_pts.toFixed(2) + ' pts')},
    ], (rr.status === 'ok' ? rr.data : []).filter((r) => String(r.date) >= t0), {empty: 'No holding has results ahead.'});
  };

  // ---------------------------------------------------------------- calendar
  const drawCalendar = (L) => {
    const t0 = today();
    const v = S.view.calendar;
    const heldN = new Set(D.stocks.filter((r) => r.held).map((r) => r.name));
    const past = v === 'past';
    const ev = L.filter((r) => r.table === 'event').filter((r) => (past ? eventPassed(r) : !eventPassed(r) && relevantEvent(r) && (v !== 'next' || daysAway(r.date) <= 7)))
      .filter((r) => (v === 'held' ? heldN.has(r.stock) : v === 'results' ? r.kind === 'results' : v === 'data' ? r.kind === 'macro' : true))
      .sort((a, b) => (past ? -1 : 1) * String(a.date).localeCompare(String(b.date)) || timeKey(a).localeCompare(timeKey(b)));
    const groups = [];
    ev.forEach((r) => {
      let g = groups[groups.length - 1];
      if (!g || g.date !== r.date) { g = {date: r.date, title: dateText(r.date), sub: capDay(relDay(r.date)), past, body: el('div', 'ers')}; groups.push(g); }
      const lines = [lastOrderText(r) && !past ? 'Last order: ' + lastOrderText(r) : '', r.plan ? 'Plan: ' + r.plan : ''].concat(sentences(r.text)).filter(Boolean);
      const macro = r.kind === 'macro';
      const actual = cleanFig(r.actual);
      g.body.append(lineRow({
        key: 'ev:' + r.id, when: capDay(shortTime(r.time_uk)), whenSub: !past && r.kind === 'results' && r.confirmed !== 'yes' ? 'est.' : '', icon: iconFor(r.stock, r.kind), title: r.name,
        stats: [heldN.has(r.stock) ? st('Held') : null, num(r.implied_pct) !== null ? stat('', '±' + num(r.implied_pct) + '%', '', 'Options-implied move on results day') : null, macro && cleanFig(r.forecast) && !actual ? stat('Forecast', cleanFig(r.forecast), '', r.forecast) : null, macro && actual ? stat('Actual', actual, '', r.actual) : null],
        detail: lines.length ? bullets(lines, {small: true}) : null,
      }));
    });
    dayGroups(q('#events'), groups, past ? 'No past events.' : 'Nothing dated in this view.');
  };

  // ---------------------------------------------------------------- log
  const drawLog = (L) => {
    const v = S.view.log;
    const titled = (x) => x.charAt(0).toUpperCase() + x.slice(1);
    if (v === 'orders') {
      const tr = L.filter((r) => r.table === 'trade').sort((a, b) => String(b.effective).localeCompare(String(a.effective)) || num(b.to_w) - num(a.to_w));
      const groups = [];
      tr.forEach((r) => { let g = groups.find((x) => x.date === r.effective); if (!g) { g = {date: r.effective, title: 'Open of ' + dateText(r.effective), sub: capDay(relDay(r.effective)), rows: [], texts: []}; groups.push(g); } g.rows.push(r); if (r.text && !g.texts.includes(r.text)) g.texts.push(r.text); });
      groups.forEach((g) => {
        const b = el('div', 'ers');
        g.rows.forEach((r) => {
          const a = num(r.from_w) === 0 ? ['Buy', 'okay'] : num(r.to_w) === 0 ? ['Sell', 'bad'] : num(r.to_w) > num(r.from_w) ? ['Add', 'okay'] : ['Trim', 'bad'];
          const row = el('div', 'or');
          const s = D.stocks.find((x) => x.name === r.name);
          row.append(logoFor(r.ticker || (s && s.ticker), s && s.market, r.name, 's'), span('or-n', r.name), st(a[0], a[1]), span('or-w mut', wt(num(r.from_w))), span('or-w b', wt(num(r.to_w))));
          b.append(row);
        });
        g.texts.forEach((x) => { const bl = bullets(sentences(x).flatMap((s) => s.split(/;\s+/)).map((s) => titled(s)), {small: true, max: 2}); if (bl) { const n = el('div', 'or-why'); n.append(bl); b.append(n); } });
        g.body = b;
      });
      dayGroups(q('#log-orders'), groups, 'No order changes yet.');
    }
    if (v === 'alerts') {
      const al = L.filter((r) => r.table === 'alert').sort((a, b) => whenKey(b).localeCompare(whenKey(a))).slice(0, 80);
      const groups = [];
      al.forEach((r, i) => {
        let g = groups[groups.length - 1];
        if (!g || g.date !== r.date) { g = {date: r.date, title: dateText(r.date), sub: capDay(relDay(r.date)), body: el('div', 'ers')}; groups.push(g); }
        const parts = sentences(r.text);
        g.body.append(lineRow({key: 'al:' + r.date + i, when: String(r.time_uk || '').replace(/\s*UK$/, ''), icon: iconFor(['Portfolio', 'Market', 'System', 'Order', 'Watchlist'].includes(r.stock) ? '' : r.stock, 'macro'), title: r.stock || 'Market', note: parts[0] || '', detail: parts.length > 1 ? bullets(parts.slice(1), {small: true}) : null}));
      });
      dayGroups(q('#log-alerts'), groups, 'No alerts yet.');
    }
    if (v === 'analysts') {
      const all = L.filter((r) => r.table === 'revision').sort((a, b) => String(b.date).localeCompare(String(a.date)) || String(a.stock).localeCompare(String(b.stock)));
      const cap = S.size === 's' ? 12 : 30;
      const rev = S.revAll ? all : all.slice(0, cap);
      const groups = [];
      rev.forEach((r) => {
        let g = groups[groups.length - 1];
        if (!g || g.date !== r.date) { g = {date: r.date, title: dateText(r.date), sub: capDay(relDay(r.date)), body: el('div', 'ers')}; groups.push(g); }
        const act = String(r.action || '');
        const kind = /upgrade|raised|initiat/i.test(act) ? 'okay' : /downgrade|cut|lowered/i.test(act) ? 'bad' : '';
        g.body.append(lineRow({icon: iconFor(r.stock), title: r.stock, note: [r.bank, cleanFig(r.text)].filter(Boolean).join(': '), stats: [st(titled(act), kind)]}));
      });
      const box = q('#log-rev');
      dayGroups(box, groups, 'No analyst changes logged yet.');
      if (all.length > cap) { const m = btn('more', S.revAll ? 'Show the latest ' + cap : 'Show all ' + all.length, () => { S.revAll = !S.revAll; draw(); }); m.style.gridColumn = '1 / -1'; box.append(m); }
    }
    if (v === 'closed') {
      const box = q('#log-closed');
      const rows = L.filter((r) => r.table === 'postmortem').sort((a, b) => String(b.date).localeCompare(String(a.date)));
      const wrap = el('div', 'ers');
      rows.forEach((r) => {
        const lesson = r.lesson || r.text || '';
        wrap.append(lineRow({key: 'pm:' + r.id, icon: iconFor(r.name), title: r.name, note: shortDate(r.effective) + ' to ' + shortDate(r.date), stats: [stat('Return', pct(num(r.ret_pct)), dir(num(r.ret_pct))), stat('Points', pts(num(r.contrib_pts)), dir(num(r.contrib_pts)))], detail: lesson ? bullets(sentences(lesson), {small: true}) : null}));
      });
      if (!rows.length) msg(box, 'Nothing has been sold yet.'); else box.replaceChildren(wrap);
    }
  };

  // ---------------------------------------------------------------- details on hover, focus or tap
  // One layer on the page root: a panel's glass makes its own stacking layer, so a tooltip inside a panel falls behind the next one.
  const pop = el('div', 'pop'); pop.hidden = true; pop.setAttribute('role', 'tooltip'); root.append(pop);
  let popFor = null;
  const hideTip = () => { pop.hidden = true; popFor = null; };
  const showTip = (t) => {
    popFor = t;
    pop.textContent = t.dataset.tip;
    pop.hidden = false;
    const b = t.getBoundingClientRect(); const w = pop.offsetWidth; const h = pop.offsetHeight;
    const vw = document.documentElement.clientWidth; const vh = window.innerHeight;
    pop.style.left = Math.max(8, Math.min(vw - w - 8, b.left)) + 'px';
    pop.style.top = (b.bottom + h + 12 > vh && b.top > h + 12 ? b.top - h - 6 : b.bottom + 6) + 'px';
  };
  root.addEventListener('pointerover', (e) => { if (e.pointerType === 'touch') return; const t = e.target.closest('[data-tip]'); if (t) showTip(t); else if (popFor) hideTip(); });
  root.addEventListener('pointerleave', hideTip);
  root.addEventListener('focusin', (e) => { const t = e.target.closest('[data-tip]'); if (t && e.target.matches(':focus-visible')) showTip(t); });
  root.addEventListener('focusout', hideTip);
  root.addEventListener('click', (e) => { const t = e.target.closest('[data-tip]'); if (t) { if (popFor === t && e.pointerType !== 'mouse') hideTip(); else showTip(t); } else hideTip(); });
  window.addEventListener('scroll', hideTip, {passive: true, capture: true});

  // ---------------------------------------------------------------- theme and main loop
  const probe = el('span');
  probe.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden;color:var(--color-bg)';
  probe.setAttribute('aria-hidden', 'true');
  root.append(probe);
  const setTheme = () => {
    let dark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)').matches : false;
    try {
      if (getComputedStyle(root).getPropertyValue('--color-bg').trim()) {
        const c = document.createElement('canvas'); c.width = 1; c.height = 1;
        const g = c.getContext('2d'); g.fillStyle = getComputedStyle(probe).color; g.fillRect(0, 0, 1, 1);
        const p = g.getImageData(0, 0, 1, 1).data;
        dark = (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255 < 0.42;
      }
    } catch (e) { /* keep the system setting */ }
    const name = dark ? 'dark' : 'light';
    if (root.dataset.theme !== name) root.dataset.theme = name;
  };
  if (window.matchMedia) { const mq = window.matchMedia('(prefers-color-scheme: dark)'); if (mq.addEventListener) mq.addEventListener('change', setTheme); }
  if (window.MutationObserver) { const mo = new MutationObserver(setTheme); [document.documentElement, document.body].forEach((n) => { if (n) mo.observe(n, {attributes: true, attributeFilter: ['class', 'style', 'data-theme', 'data-mode', 'data-color-scheme']}); }); }

  const draw = () => {
    hideTip();
    setTheme();
    S.size = root.clientWidth >= 1240 ? 'l' : root.clientWidth >= 760 ? 'm' : 's';
    root.dataset.w = S.size;
    S.cols = S.size === 'l' && S.sel && S.page === 'today' ? 'm' : S.size;
    root.dataset.c = S.cols;
    const s = dash.data('stocks');
    const lg = dash.data('ledger');
    const hd = dash.data('history');
    logos();
    S.busy = s.status === 'loading' || lg.status === 'loading';
    const rows = s.status === 'ok' ? s.data : [];
    const L = lg.status === 'ok' ? lg.data : [];
    derive(rows, L, hd.status === 'ok' ? hd.data : []);
    freshness(rows);
    if (S.page !== 'today') root.dataset.focus = '0';
    if (SEGS[S.page]) segBar(S.page);
    if (s.status === 'error' || lg.status === 'error') { ['#hold-body', '#watch-body'].forEach((x) => msg(q(x), '', true)); }
    if (S.page === 'today') {
      strip(rows, L);
      orderQueue(rows, L);
      if (s.status === 'ok') { holdings(); watchlist(); context(rows, L); rail(L); research(L, rows); }
    }
    if (S.page === 'macro') drawMacro(L);
    if (S.page === 'performance') drawPerformance(L);
    if (S.page === 'risk') drawRisk(L);
    if (S.page === 'calendar') drawCalendar(L);
    if (S.page === 'log') drawLog(L);
  };
  // The selected tab sits under a sliding lens.
  const placeLens = () => {
    const a = root.querySelector('.tab[aria-selected="true"]');
    const l = q('#lens');
    if (!a || !l) return;
    l.style.width = a.offsetWidth + 'px';
    l.style.transform = 'translateX(' + a.offsetLeft + 'px)';
  };
  const show = (name, link) => {
    S.page = PAGES.includes(name) ? name : 'today';
    PAGES.forEach((p) => { q('#' + p).hidden = p !== S.page; });
    root.querySelectorAll('.tab').forEach((b) => b.setAttribute('aria-selected', b.dataset.tab === S.page ? 'true' : 'false'));
    if (link) dash.setLink(S.page);
    draw();
    placeLens();
  };
  root.querySelectorAll('.tab').forEach((b) => b.addEventListener('click', () => show(b.dataset.tab, true)));
  root.querySelector('.tabs').addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const i = PAGES.indexOf(S.page) + (e.key === 'ArrowRight' ? 1 : -1);
    const nx = PAGES[(i + PAGES.length) % PAGES.length];
    show(nx, true);
    root.querySelector('.tab[data-tab="' + nx + '"]').focus();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && S.sel) { S.sel = null; draw(); } });
  let rt = null; let lw = root.clientWidth;
  window.addEventListener('resize', () => { if (root.clientWidth === lw) return; lw = root.clientWidth; clearTimeout(rt); rt = setTimeout(() => { draw(); placeLens(); }, 150); });
  dash.onData(draw);
  const named = location.hash.slice(1);
  if (PAGES.includes(named) && named !== 'today') show(named, false);
  placeLens();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeLens);
