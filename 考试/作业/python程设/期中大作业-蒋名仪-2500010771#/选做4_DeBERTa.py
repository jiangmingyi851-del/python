"""
DeBERTa 实验：用 microsoft/deberta-v3-small 抽 [CLS]/mean-pool 句嵌入 → LR 多标签分类
- 不微调（fine-tune 在 CPU 上不现实），仅作为「特征提取器」
- 与 baseline LR(TFIDF) 公平对比
"""
import os, re, time, warnings, numpy as np, pandas as pd, torch
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, jaccard_score, hamming_loss
from transformers import AutoTokenizer, AutoModel

SEED = 42; np.random.seed(SEED); torch.manual_seed(SEED)
DEVICE = 'cpu'

DATA_DIR='/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/data'
OUT_DIR='/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/期中大作业-蒋名仪-2500010771'
mi=pd.read_csv(os.path.join(DATA_DIR,'info.csv'),encoding='latin-1',
               usecols=['id','name','genre','intro'])
def clean(s):
    s=str(s).lower();s=re.sub(r'<.*?>','',s);s=re.sub(r'[^a-z0-9 ]',' ',s)
    return re.sub(r'\s+',' ',s).strip()
df=mi.dropna(subset=['intro','genre']).copy(); df=df[df['genre'].str.len()>0]
df['text']=(df['name'].fillna('')+' . '+df['intro'].fillna('')).map(clean)
df['labels']=df['genre'].str.split('|')
mlb=MultiLabelBinarizer(); Y=mlb.fit_transform(df['labels'])
GENRES=list(mlb.classes_)
X_text=df['text'].to_numpy(dtype=object)
X_tr,X_tmp,y_tr,y_tmp=train_test_split(X_text,Y,test_size=0.25,random_state=SEED)
X_va,X_te,y_va,y_te  =train_test_split(X_tmp,y_tmp,test_size=0.6,random_state=SEED)
print(f'[data] N={len(df)}  K={len(GENRES)}  train={len(X_tr)} val={len(X_va)} test={len(X_te)}')

MODEL='microsoft/deberta-v3-small'
print(f'[load] {MODEL}')
tk=AutoTokenizer.from_pretrained(MODEL)
m=AutoModel.from_pretrained(MODEL).to(DEVICE).eval()
print(f'  params={sum(p.numel() for p in m.parameters())/1e6:.1f}M')

@torch.no_grad()
def encode(texts, batch=8, max_len=128):
    out=[]
    for i in range(0,len(texts),batch):
        b=list(texts[i:i+batch])
        enc=tk(b, padding=True, truncation=True, max_length=max_len, return_tensors='pt').to(DEVICE)
        h=m(**enc).last_hidden_state           # (B, L, D)
        mask=enc['attention_mask'].unsqueeze(-1).float()
        # mean-pool with mask
        v=(h*mask).sum(1)/mask.sum(1).clamp(min=1)
        out.append(v.cpu().numpy())
        if (i//batch)%50==0:
            print(f'  encoded {i+len(b)}/{len(texts)}', flush=True)
    return np.vstack(out)

t0=time.time(); Etr=encode(X_tr); print(f'[encode] train {time.time()-t0:.1f}s shape={Etr.shape}')
t0=time.time(); Eva=encode(X_va); print(f'[encode] val   {time.time()-t0:.1f}s')
t0=time.time(); Ete=encode(X_te); print(f'[encode] test  {time.time()-t0:.1f}s')

print('[train LR on DeBERTa embeds]')
lr=OneVsRestClassifier(LogisticRegression(max_iter=2000, C=4))
lr.fit(Etr, y_tr)
P_va=lr.predict_proba(Eva); P_te=lr.predict_proba(Ete)

def evalp(name,yt,yp):
    return dict(model=name,
        hamming=round(hamming_loss(yt,yp),4),
        jaccard=round(jaccard_score(yt,yp,average='samples',zero_division=0),4),
        f1_macro=round(f1_score(yt,yp,average='macro',zero_division=0),4),
        f1_samples=round(f1_score(yt,yp,average='samples',zero_division=0),4))

# 0.5 阈值
pred05=(P_te>0.5).astype(int)
for i in range(len(pred05)):
    if pred05[i].sum()==0: pred05[i,P_te[i].argmax()]=1
r0=evalp('DeBERTa-small + LR (thr=0.5)', y_te, pred05)

# 自适应阈值（细网格）
GRID=np.arange(0.02,0.98,0.005)
def ada(Pv,yv,Pt,grid):
    K=Pv.shape[1]; thrs=np.zeros(K)
    for j in range(K):
        bf,bt=-1,grid[0]
        for t in grid:
            f=f1_score(yv[:,j],(Pv[:,j]>t).astype(int),zero_division=0)
            if f>bf: bf,bt=f,t
        thrs[j]=bt
    p=(Pt>thrs).astype(int)
    for i in range(len(p)):
        if p[i].sum()==0: p[i,Pt[i].argmax()]=1
    return p
pred_ada=ada(P_va,y_va,P_te,GRID)
r1=evalp('DeBERTa-small + LR + AdaThr-fine', y_te, pred_ada)

print('\n=== DeBERTa 结果 ===')
res=pd.DataFrame([r0,r1])
print(res.to_string(index=False))
res.to_csv(os.path.join(OUT_DIR,'选做4_DeBERTa结果.csv'), index=False, encoding='utf-8-sig')
print('[saved] 选做4_DeBERTa结果.csv')
