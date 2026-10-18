import json, math, statistics as st
H=json.load(open('history.json'))
P={}
for r in H: P.setdefault(r['ticker'],{})[r['date']]=r
W={'KO':20,'XOM':15,'CVX':15,'SHEL':15,'MSFT':15,'LLY':15,'PLTR':5}
def rets(t):
    d=sorted(P[t]); out={}
    for a,b in zip(d,d[1:]): out[b]=P[t][b]['close']/P[t][a]['close']-1
    return out
R={t:rets(t) for t in list(W)+['SPY','OIL']}
common=sorted(set.intersection(*[set(R[t]) for t in list(W)+['SPY']]))
print('common sessions', len(common), common[0], common[-1])
# data quality: close-only rows inside window
for t in W:
    co=[d for d in common[-120:] if P[t][d]['volume'] is None]
    print(t,'close-only rows in last 120:',len(co))
for N in (40,60,120,len(common)):
    ds=common[-N:]
    m={t:[R[t][d] for d in ds] for t in list(W)+['SPY']}
    port=[sum(W[t]/100*m[t][i] for t in W) for i in range(len(ds))]
    def cov(a,b):
        ma,mb=st.mean(a),st.mean(b); return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(len(a)-1)
    vp=math.sqrt(cov(port,port)); vs=math.sqrt(cov(m['SPY'],m['SPY']))
    beta=cov(port,m['SPY'])/cov(m['SPY'],m['SPY'])
    te=math.sqrt(cov([p-s for p,s in zip(port,m['SPY'])],[p-s for p,s in zip(port,m['SPY'])]))
    var=cov(port,port)
    shares={t:W[t]/100*cov(m[t],port)/var*100 for t in W}
    en=sum(shares[t] for t in ('XOM','CVX','SHEL'))
    # worst 5-day non-overlapping
    p5=[sum(port[i:i+5]) for i in range(0,len(port)-4,5)]
    print(f"\nN={N} ({ds[0]}..{ds[-1]}): port daily vol {vp*100:.2f}% (ann {vp*math.sqrt(252)*100:.1f}%), SPY {vs*100:.2f}%, beta {beta:.2f}, tracking error daily {te*100:.2f}% (5-day ~{te*math.sqrt(5)*100:.2f}%)")
    print('  risk shares', {t:round(v,1) for t,v in shares.items()}, 'energy', round(en,1))
    print('  worst non-overlapping 5-session sum', round(min(p5)*100,2), 'best', round(max(p5)*100,2))
    if N==60 or N==120:
        print('  corr XOM/CVX %.2f XOM/SHEL %.2f CVX/SHEL %.2f KO/SPY %.2f'%(
            cov(m['XOM'],m['CVX'])/math.sqrt(cov(m['XOM'],m['XOM'])*cov(m['CVX'],m['CVX'])),
            cov(m['XOM'],m['SHEL'])/math.sqrt(cov(m['XOM'],m['XOM'])*cov(m['SHEL'],m['SHEL'])),
            cov(m['CVX'],m['SHEL'])/math.sqrt(cov(m['CVX'],m['CVX'])*cov(m['SHEL'],m['SHEL'])),
            cov(m['KO'],m['SPY'])/math.sqrt(cov(m['KO'],m['KO'])*cov(m['SPY'],m['SPY']))))
        # oil beta
        oc=[d for d in ds if d in R['OIL']]
        po=[sum(W[t]/100*R[t][d] for t in W) for d in oc]; o=[R['OIL'][d] for d in oc]
        print('  oil beta (portfolio on OIL daily) %.3f over %d sessions; corr %.2f'%(cov(po,o)/cov(o,o),len(oc),cov(po,o)/math.sqrt(cov(po,po)*cov(o,o))))
# Contribution by stock over the game from ledger contrib rows
L=json.load(open('ledger.json'))
c={}
for r in L:
    if r['table']=='contrib': c[r['name']]=c.get(r['name'],0)+(r['contrib_pts'] or 0)
print('\nsum of daily contributions (pts, uncompounded):',{k:round(v,3) for k,v in sorted(c.items(),key=lambda x:-x[1])}, 'total',round(sum(c.values()),3))
ev=[r for r in L if r['table']=='event' and r.get('kind')=='results']
for r in sorted(ev,key=lambda r:r['date']):
    print('EVENT',r['date'],r.get('time_uk'),r.get('stock'),r.get('confirmed'),r.get('implied_pct'),r.get('last_order'))
