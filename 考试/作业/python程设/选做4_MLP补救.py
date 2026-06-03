"""
MLP 补救实验（快速版）：用 Temperature Scaling 替代 CalibratedClassifierCV。
Temperature: 在验证集上为每类找最优温度 T，logits/T 后再 sigmoid，使概率分布"摊平"。
"""
import os, re, time, warnings, numpy as np, pandas as pd
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score, jaccard_score, hamming_loss

SEED = 42; np.random.seed(SEED)
DATA_DIR = '/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/data'
mi = pd.read_csv(os.path.join(DATA_DIR,'info.csv'),encoding='latin-1',
                 usecols=['id','name','genre','intro'])
mi.rename(columns={'id':'movie_id'}, inplace=True)
def clean(s):
    s=str(s).lower();s=re.sub(r'<.*?>','',s);s=re.sub(r'[^a-z0-9 ]',' ',s)
    return re.sub(r'\s+',' ',s).strip()
df=mi.dropna(subset=['intro','genre']).copy(); df=df[df['genre'].str.len()>0]
df['text']=(df['name'].fillna('')+' . '+df['intro'].fillna('')).map(clean)
df['labels']=df['genre'].str.split('|')
mlb=MultiLabelBinarizer(); Y=mlb.fit_transform(df['labels'])
X_text=df['text'].to_numpy(dtype=object)
X_tr,X_tmp,y_tr,y_tmp=train_test_split(X_text,Y,test_size=0.25,random_state=SEED)
X_va,X_te,y_va,y_te  =train_test_split(X_tmp,y_tmp,test_size=0.6,random_state=SEED)
tfidf=TfidfVectorizer(ngram_range=(1,2),min_df=5,max_df=0.95,sublinear_tf=True,stop_words='english')
Xtr_v=tfidf.fit_transform(X_tr);Xva_v=tfidf.transform(X_va);Xte_v=tfidf.transform(X_te)

print('[训练 LR]')
lr=OneVsRestClassifier(LogisticRegression(max_iter=2000,C=4)); lr.fit(Xtr_v,y_tr)
P_lr_va=lr.predict_proba(Xva_v); P_lr_te=lr.predict_proba(Xte_v)

print('[训练 MLP]')
mlp=MLPClassifier(hidden_layer_sizes=(256,128),early_stopping=True,
                  max_iter=60,random_state=SEED,batch_size=128)
mlp.fit(Xtr_v.astype(np.float32),y_tr)
P_mlp_va=mlp.predict_proba(Xva_v.astype(np.float32))
P_mlp_te=mlp.predict_proba(Xte_v.astype(np.float32))

print('[训练 MLP 强正则版]')
mlp2=MLPClassifier(hidden_layer_sizes=(128,),alpha=1e-3,
                   early_stopping=True,max_iter=40,random_state=SEED,batch_size=128)
mlp2.fit(Xtr_v.astype(np.float32),y_tr)
P_m2_va=mlp2.predict_proba(Xva_v.astype(np.float32))
P_m2_te=mlp2.predict_proba(Xte_v.astype(np.float32))

# --- Temperature Scaling (per class) ---
def temp_scale(P_va, y_va_, P_te):
    EPS=1e-7
    L_va=np.log(P_va.clip(EPS,1-EPS)/(1-P_va).clip(EPS,1-EPS))   # logit
    L_te=np.log(P_te.clip(EPS,1-EPS)/(1-P_te).clip(EPS,1-EPS))
    K=L_va.shape[1]; T_opt=np.ones(K)
    for j in range(K):
        best_f, best_T = -1, 1.0
        for T in np.arange(0.3, 3.1, 0.1):
            p_t = 1/(1+np.exp(-L_va[:,j]/T))
            # 用对应类别 0.5 阈值的 f1 作目标
            f = f1_score(y_va_[:,j], (p_t>0.5).astype(int), zero_division=0)
            if f > best_f: best_f, best_T = f, T
        T_opt[j] = best_T
    P_va_T = 1/(1+np.exp(-L_va/T_opt))
    P_te_T = 1/(1+np.exp(-L_te/T_opt))
    return P_va_T, P_te_T, T_opt

print('[Temperature Scaling MLP]')
P_mt_va, P_mt_te, T_opt = temp_scale(P_mlp_va, y_va, P_mlp_te)
print(f'  T 范围: min={T_opt.min():.2f} max={T_opt.max():.2f} mean={T_opt.mean():.2f}')

def diag(name, P):
    p = P.ravel()
    print(f'  {name:25s}  mean={p.mean():.3f}  '
          f'<0.05:{(p<0.05).mean():.2%}  0.05-0.95:{((p>=0.05)&(p<=0.95)).mean():.2%}  '
          f'>0.95:{(p>0.95).mean():.2%}')

print('\n=== 概率分布对比 (val) ===')
diag('LR', P_lr_va); diag('MLP-原始', P_mlp_va)
diag('MLP-Reg', P_m2_va); diag('MLP-Temp', P_mt_va)

def ada_thr(P_va, y_va_, P_te, grid):
    K=P_va.shape[1]; thrs=np.zeros(K)
    for j in range(K):
        best, best_f = grid[0], -1
        for t in grid:
            f = f1_score(y_va_[:,j], (P_va[:,j]>t).astype(int), zero_division=0)
            if f > best_f: best, best_f = t, f
        thrs[j] = best
    pred = (P_te > thrs).astype(int)
    for i in range(len(pred)):
        if pred[i].sum()==0: pred[i, P_te[i].argmax()] = 1
    return pred, thrs

def evalp(name, y_t, y_p):
    return dict(model=name,
        hamming=round(hamming_loss(y_t,y_p),4),
        jaccard=round(jaccard_score(y_t,y_p,average='samples',zero_division=0),4),
        f1_macro=round(f1_score(y_t,y_p,average='macro',zero_division=0),4),
        f1_samples=round(f1_score(y_t,y_p,average='samples',zero_division=0),4))

GRID_FINE = np.arange(0.02, 0.98, 0.005)
GRID_COARSE = np.arange(0.10, 0.90, 0.02)

cases = [
    ('LR',         P_lr_va, P_lr_te),
    ('MLP-原始',   P_mlp_va, P_mlp_te),
    ('MLP-Reg',    P_m2_va, P_m2_te),
    ('MLP-Temp',   P_mt_va, P_mt_te),
]
res = []
for name, Pv, Pt in cases:
    pred05 = (Pt > 0.5).astype(int)
    for i in range(len(pred05)):
        if pred05[i].sum()==0: pred05[i, Pt[i].argmax()] = 1
    res.append(evalp(f'{name} (thr=0.5)', y_te, pred05))
    p_c, _ = ada_thr(Pv, y_va, Pt, GRID_COARSE)
    res.append(evalp(f'{name} +AdaThr-coarse', y_te, p_c))
    p_f, _ = ada_thr(Pv, y_va, Pt, GRID_FINE)
    res.append(evalp(f'{name} +AdaThr-fine', y_te, p_f))

dfR = pd.DataFrame(res).sort_values('f1_samples', ascending=False).reset_index(drop=True)
print('\n=== 最终对比（细阈值 + 各 MLP 变种）===')
print(dfR.to_string(index=False))
out='/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/期中大作业-蒋名仪-2500010771'
dfR.to_csv(os.path.join(out,'选做4_MLP补救实验.csv'),index=False,encoding='utf-8-sig')
print(f'[saved] 选做4_MLP补救实验.csv')
