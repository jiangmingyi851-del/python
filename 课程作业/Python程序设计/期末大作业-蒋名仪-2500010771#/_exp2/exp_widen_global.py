# -*- coding: utf-8 -*-
# 拓宽异常用户范围 -> 对全部异常用户做"簇专家融合"优化 -> 观察【全量总MSE】变化
# 专家: M3 / M2+ / M6 (向量化全量训练)。纯CPU。
import numpy as np, pandas as pd, time, sys, pickle
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
np.random.seed(2024)
def fl(): sys.stdout.flush()

ratings = pd.read_csv('./data/ratings2.csv', encoding='latin-1', usecols=['user_id','movie_id','rating','timestamp'])
movies = pd.read_csv('./data/movies.csv', encoding='latin-1', usecols=['movie_id','genres'])
mask = np.random.rand(len(ratings)) < 0.05
test = ratings[mask].reset_index(drop=True); train = ratings[~mask].reset_index(drop=True)
mu = train['rating'].mean()

# M2+ (简化: 仅 b_u+b_i 的 M2, 作为对照专家足够)
b_i = (train['rating']-mu).groupby(train['movie_id']).sum()/(train.groupby('movie_id')['rating'].count()+25)
train['_pmi']=mu+train['movie_id'].map(b_i).fillna(0)
b_u = (train['rating']-train['_pmi']).groupby(train['user_id']).sum()/(train.groupby('user_id')['rating'].count()+10)
ucnt = train.groupby('user_id')['rating'].size()
def m2(df): return np.clip(mu+df['user_id'].map(b_u).fillna(0).values+df['movie_id'].map(b_i).fillna(0).values,1,5)

# ---- 向量化 SVD 基类 (M3=纯潜因子, M6=加视觉) ----
ui={u:i for i,u in enumerate(train['user_id'].unique())}; ii={m:j for j,m in enumerate(train['movie_id'].unique())}
ua=train['user_id'].map(ui).values; ia=train['movie_id'].map(ii).values; ra=train['rating'].values.astype(float)
def train_svd(Vmat=None, k=32, ep=22, lr=0.012, reg=0.06):
    rng=np.random.default_rng(0); nU,nI=len(ui),len(ii)
    bu=np.zeros(nU); bi=np.zeros(nI); Pm=rng.normal(0,.1,(nU,k)); Qm=rng.normal(0,.1,(nI,k))
    W=rng.normal(0,.05,(k,Vmat.shape[1])) if Vmat is not None else None
    for e_ in range(ep):
        o=rng.permutation(len(ua))
        for s in range(0,len(o),4096):
            ix=o[s:s+4096]; u,i,r=ua[ix],ia[ix],ra[ix]
            if Vmat is None:
                QF=Qm[i]
            else:
                QF=Qm[i]+Vmat[i]@W.T
            Pu=Pm[u].copy(); e=r-(mu+bu[u]+bi[i]+np.sum(Pu*QF,axis=1))
            np.add.at(bu,u,lr*(e-reg*bu[u])); np.add.at(bi,i,lr*(e-reg*bi[i]))
            np.add.at(Pm,u,lr*(e[:,None]*QF-reg*Pu)); np.add.at(Qm,i,lr*(e[:,None]*Pu-reg*Qm[i]))
            if Vmat is not None: W+=lr*((Pu*e[:,None]).T@Vmat[i]/len(ix)-reg*W)
    return bu,bi,Pm,Qm,W
def pred_svd(df,P,Vmat=None):
    bu,bi,Pm,Qm,W=P
    u=df['user_id'].map(ui).to_numpy(); i=df['movie_id'].map(ii).to_numpy()
    uk=~pd.isna(u); ik=~pd.isna(i); out=np.full(len(df),mu); b=uk&ik
    ub=u[b].astype(int); ib=i[b].astype(int)
    QF=Qm[ib]+(Vmat[ib]@W.T if Vmat is not None else 0)
    out[b]=mu+bu[ub]+bi[ib]+np.sum(Pm[ub]*QF,axis=1)
    out[uk&~ik]=mu+bu[u[uk&~ik].astype(int)]; out[~uk&ik]=mu+bi[i[~uk&ik].astype(int)]
    return np.clip(out,1,5)

t=time.time(); P3=train_svd(None); print(f"M3 trained {time.time()-t:.0f}s"); fl()
# 视觉矩阵
with open('./poster_feat.pkl','rb') as f: pdf=pickle.load(f)
Vr=np.stack(pdf['features'].apply(lambda v:np.asarray(v).ravel()).values); midA=pdf['movie_id'].values.astype(int)
Vu=normalize(PCA(64,random_state=0).fit_transform(Vr),axis=1); m2v={m:i for i,m in enumerate(midA)}
Vmat=np.zeros((len(ii),64))
for m,j in ii.items():
    if m in m2v: Vmat[j]=Vu[m2v[m]]
t=time.time(); P6=train_svd(Vmat); print(f"M6 trained {time.time()-t:.0f}s"); fl()

# 各模型 train/test/meta 预测
tr3=pred_svd(train,P3); te3=pred_svd(test,P3); te6=pred_svd(test,P6,Vmat); te2=m2(test)
y=test['rating'].values
print(f"\n全量基线 MSE: M3={mean_squared_error(y,te3):.4f}  M6={mean_squared_error(y,te6,):.4f}  M2={mean_squared_error(y,te2):.4f}"); fl()

# meta_val (train 的 10%) 学簇权重
mv_mask=np.random.rand(len(train))<0.10; mv=train[mv_mask].reset_index(drop=True)
mv3=pred_svd(mv,P3); mv6=pred_svd(mv,P6,Vmat); mv2=m2(mv); ymv=mv['rating'].values
E_te=np.column_stack([te3,te2,te6]); E_mv=np.column_stack([mv3,mv2,mv6])

# 异常识别 (M3残差)
res=np.abs(train['rating'].values-tr3)
ue=pd.DataFrame({'u':train['user_id'].values,'ae':res}).groupby('u')['ae'].mean()
cand=ue[ucnt.reindex(ue.index).fillna(0)>=30]
gp=train.groupby('user_id');
bf=pd.DataFrame(index=cand.index)
bf['mr']=gp['rating'].mean().reindex(bf.index); bf['sr']=gp['rating'].std().reindex(bf.index).fillna(0)
bf['ph']=gp['rating'].apply(lambda s:(s>=4).mean()).reindex(bf.index); bf['pl']=gp['rating'].apply(lambda s:(s<=2).mean()).reindex(bf.index)

def softmax_w(mse,tau=0.02):
    sc=-np.asarray(mse)/tau; sc-=sc.max(); w=np.exp(sc); return w/w.sum()

print("\n[拓宽异常范围 -> 对全部异常用户做簇专家融合 -> 全量总MSE]"); fl()
print(f"  {'范围':>7} {'异常用户':>6} {'测试异常样本':>10} {'全量MSE(优化后)':>14} {'Δ全量':>9} {'异常MSE:前->后':>16}"); fl()
base_all=mean_squared_error(y,te3)
for q in [0.95,0.90,0.85,0.80]:
    cut=cand.quantile(q); abn=set(cand[cand>=cut].index)
    # 聚类
    Xb=StandardScaler().fit_transform(bf.loc[list(abn)].fillna(0).values)
    cl=KMeans(4,n_init=10,random_state=0).fit_predict(Xb); clm=dict(zip(list(abn),cl))
    # meta 上学每簇权重
    mv_cl=mv['user_id'].map(clm); te_cl=test['user_id'].map(clm)
    pred=te3.copy()  # 正常用户保持 M3
    for c in range(4):
        mmv=(mv_cl==c).values
        if mmv.sum()<20: continue
        mse_k=[mean_squared_error(ymv[mmv],E_mv[mmv,j]) for j in range(3)]
        w=softmax_w(mse_k)
        mte=(te_cl==c).values
        pred[mte]=np.clip(E_te[mte]@w,1,5)
    m_abn=test['user_id'].isin(abn).values
    all_opt=mean_squared_error(y,pred)
    abn_before=mean_squared_error(y[m_abn],te3[m_abn]); abn_after=mean_squared_error(y[m_abn],pred[m_abn])
    print(f"  Top{int((1-q)*100):>2}%  {len(abn):>6}  {m_abn.sum():>10}  {all_opt:>14.4f}  {all_opt-base_all:>+9.4f}  {abn_before:.4f}->{abn_after:.4f}"); fl()
print(f"\n  [对照] 全员 M3 全量MSE = {base_all:.4f}"); fl()
print("  解读: 看'Δ全量'是正(变差)还是负(变好), 以及随范围拓宽的趋势。"); fl()
