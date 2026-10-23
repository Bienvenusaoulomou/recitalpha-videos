import sys, numpy as np, soundfile as sf
mod = sys.argv[1]; sys.argv=[sys.argv[0]]
R = __import__(mod); E = R.E
SR=24000; ROOT=R.ROOT
v,_=sf.read(f'{ROOT}/voice.wav'); v=v.astype(np.float32); v*=0.89/np.abs(v).max()
n=int(E.TOTAL*SR)+SR; out=np.zeros(n,np.float32); out[:len(v)]+=v
rng=np.random.default_rng(1)
def add(sig,t):
    i=int(t*SR)
    if i<0: return
    j=min(n,i+len(sig)); out[i:j]+=sig[:j-i]
def whoosh(d=0.55,g=0.10):
    m=int(d*SR); x=rng.normal(0,1,m).astype(np.float32); y=np.zeros(m,np.float32); a=0.0
    for k in range(m):
        cf=0.02+0.25*np.sin(np.pi*k/m); a+=cf*(x[k]-a); y[k]=a
    return y*np.sin(np.pi*np.linspace(0,1,m))**2*g/np.abs(y).max()
def impact(g=0.35):
    m=int(0.7*SR); t=np.arange(m)/SR
    s=np.sin(2*np.pi*(48+30*np.exp(-t*20))*t)*np.exp(-t*6)+rng.normal(0,1,m)*np.exp(-t*40)*0.25
    return (s*g).astype(np.float32)
def clink(g=0.06):
    m=int(0.35*SR); t=np.arange(m)/SR
    return ((np.sin(2*np.pi*2630*t)+0.6*np.sin(2*np.pi*3910*t))*np.exp(-t*18)*g).astype(np.float32)
Wh=whoosh()
for s in E.SCENES[1:]: add(Wh,s['start']-0.3)
for sid,w,off,g in R.IMPACTS: add(impact(g), E.SCN[sid]['start']+E.wt(sid,w)+off)
for sid,w,off in getattr(R,'CLINKS',[]):
    for k in range(6): add(clink(0.05), E.SCN[sid]['start']+E.wt(sid,w)+off+k*0.09)
t=np.arange(n)/SR
pad=(np.sin(2*np.pi*55*t)+0.5*np.sin(2*np.pi*82.6*t)+0.3*np.sin(2*np.pi*110.3*t))*(0.6+0.4*np.sin(2*np.pi*0.07*t))
out+=(pad*np.clip(t/2,0,1)*np.clip((E.TOTAL-t)/2,0,1)*0.018).astype(np.float32)
out=np.tanh(out*1.1)/np.tanh(1.1)
sf.write(f'{ROOT}/mix.wav',out[:int(E.TOTAL*SR)],SR); print('mix ok')
