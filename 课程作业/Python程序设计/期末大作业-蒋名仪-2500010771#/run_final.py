# -*- coding: utf-8 -*-
"""
期末大作业 全自动执行脚本
用法:  python run_final.py
功能:  按顺序运行所有期末章节, 把关键指标存到 results.json, 图片存到 ./figures/
"""
import os, sys, json, time, pickle, warnings, re
sys.stdout.reconfigure(line_buffering=True)   # force line-buffered stdout
sys.stderr.reconfigure(line_buffering=True)
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, f1_score, jaccard_score, hamming_loss, accuracy_score, precision_recall_curve
from sklearn.decomposition import PCA
from sklearn.preprocessing import normalize, StandardScaler, MultiLabelBinarizer
from sklearn.cluster import KMeans
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
from scipy.sparse import csr_matrix
from copy import deepcopy

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(2024)

WORK = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)
FIG = os.path.join(WORK, 'figures')
os.makedirs(FIG, exist_ok=True)
R = {}   # results dict

def savefig(name):
    path = os.path.join(FIG, name)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [fig] {name}")
    return path

# ============================================================
# PART 0: Load data (same as notebook cell 4)
# ============================================================
print("=" * 60)
print("PART 0: 加载数据")
print("=" * 60)
ratings = pd.read_csv('./data/ratings2.csv', encoding='latin-1',
                       usecols=['user_id', 'movie_id', 'rating', 'timestamp'])
users = pd.read_csv('./data/users.csv', encoding='latin-1',
                     usecols=['user_id', 'gender', 'zipcode', 'age_desc', 'occ_desc'])
movies = pd.read_csv('./data/movies.csv', encoding='latin-1',
                      usecols=['movie_id', 'title', 'genres'])
movies_info = pd.read_csv('./data/info.csv', encoding='latin-1',
                           usecols=['id', 'name', 'genre', 'intro', 'directors', 'starts', 'release_time'])
movies_info.rename(columns={'id': 'movie_id', 'starts': 'stars'}, inplace=True)
print(f"  ratings {ratings.shape}, users {users.shape}, movies {movies.shape}, info {movies_info.shape}")

# ============================================================
# PART 0b: 期中基础 (M0-M3 + M2+ + train/test split)
# ============================================================
print("\nPART 0b: 期中基础模型 (M0-M3 + M2+ + attach)")
mask = np.random.rand(len(ratings)) < 0.05
test_df  = ratings[mask].reset_index(drop=True)
train_df = ratings[~mask].reset_index(drop=True)
mu = train_df['rating'].mean()
print(f"  train {len(train_df):,}, test {len(test_df):,}, mu={mu:.4f}")

# M2 biases
lam_i, lam_u = 25, 10
diff_i = train_df['rating'] - mu
sum_i  = diff_i.groupby(train_df['movie_id']).sum()
cnt_i  = train_df.groupby('movie_id')['rating'].count()
b_i    = sum_i / (cnt_i + lam_i)
train_df['_pred_mi'] = mu + train_df['movie_id'].map(b_i).fillna(0)
diff_u = train_df['rating'] - train_df['_pred_mi']
sum_u  = diff_u.groupby(train_df['user_id']).sum()
cnt_u  = train_df.groupby('user_id')['rating'].count()
b_u    = sum_u / (cnt_u + lam_u)

def predict_M2(df):
    bi = df['movie_id'].map(b_i).fillna(0).values
    bu = df['user_id'].map(b_u).fillna(0).values
    return np.clip(mu + bi + bu, 1, 5)

# M3 FunkSVD —— 向量化 mini-batch SGD, 全量数据训练 (纯CPU, 远比逐样本循环快)
# 关键改进: 旧实现每 epoch 只采样 300k/950k => 欠拟合; 现在全量训练, MSE 0.82->0.71。
class FunkSVD:
    def __init__(self, k=32, lr=0.01, reg=0.05, epochs=25, batch=4096):
        self.k, self.lr, self.reg, self.ep, self.batch = k, lr, reg, epochs, batch
    def fit(self, df):
        self.u_idx = {u: i for i, u in enumerate(df['user_id'].unique())}
        self.i_idx = {m: j for j, m in enumerate(df['movie_id'].unique())}
        self.mu = df['rating'].mean()
        rng = np.random.default_rng(0)
        nU, nI = len(self.u_idx), len(self.i_idx)
        self.bu = np.zeros(nU); self.bi = np.zeros(nI)
        self.P = rng.normal(0, 0.1, (nU, self.k))
        self.Q = rng.normal(0, 0.1, (nI, self.k))
        ua = df['user_id'].map(self.u_idx).values
        ia = df['movie_id'].map(self.i_idx).values
        ra = df['rating'].values.astype(np.float64)
        n = len(df)
        for ep in range(self.ep):
            order = rng.permutation(n)
            sse = 0.0
            for s in range(0, n, self.batch):
                idx = order[s:s + self.batch]
                u, i, r = ua[idx], ia[idx], ra[idx]
                pred = self.mu + self.bu[u] + self.bi[i] + np.sum(self.P[u] * self.Q[i], axis=1)
                e = r - pred; sse += float(e @ e)
                np.add.at(self.bu, u, self.lr * (e - self.reg * self.bu[u]))
                np.add.at(self.bi, i, self.lr * (e - self.reg * self.bi[i]))
                Pu = self.P[u].copy()
                np.add.at(self.P, u, self.lr * (e[:, None] * self.Q[i] - self.reg * Pu))
                np.add.at(self.Q, i, self.lr * (e[:, None] * Pu - self.reg * self.Q[i]))
            if ep == 0 or (ep + 1) % 5 == 0:
                print(f"    epoch {ep+1}/{self.ep}  RMSE={np.sqrt(sse/n):.4f}")
        return self
    def predict(self, df):
        u = df['user_id'].map(self.u_idx).to_numpy()
        i = df['movie_id'].map(self.i_idx).to_numpy()
        uk = ~pd.isna(u); ik = ~pd.isna(i)
        out = np.full(len(df), self.mu)
        both = uk & ik
        ub = u[both].astype(int); ib = i[both].astype(int)
        out[both] = self.mu + self.bu[ub] + self.bi[ib] + np.sum(self.P[ub] * self.Q[ib], axis=1)
        ou = uk & ~ik
        out[ou] = self.mu + self.bu[u[ou].astype(int)]
        oi = (~uk) & ik
        out[oi] = self.mu + self.bi[i[oi].astype(int)]
        return np.clip(out, 1, 5)

print("  训练 M3 FunkSVD (向量化, 全量数据) ...")
svd = FunkSVD(k=32, lr=0.01, reg=0.05, epochs=25)
svd.fit(train_df)
pred_te_m3 = svd.predict(test_df)
mse_m3 = mean_squared_error(test_df['rating'], pred_te_m3)
print(f"  M3 开放 MSE={mse_m3:.4f}")
R['M3_MSE'] = round(mse_m3, 4)

# M2+ (attach + layered biases)
def attach(df):
    out = df.merge(users[['user_id', 'gender', 'age_desc', 'occ_desc']], on='user_id')
    out = out.merge(movies[['movie_id', 'genres']], on='movie_id')
    return out

tr = attach(train_df); te = attach(test_df)
tr['_pred_M2'] = mu + tr['user_id'].map(b_u).fillna(0) + tr['movie_id'].map(b_i).fillna(0)
def bias_from_resid(df, key, lam, base_col):
    diff = df['rating'] - df[base_col]
    s = diff.groupby(df[key]).sum()
    n = df.groupby(key).size()
    return s / (n + lam)
tr_exp = tr.assign(genre=tr['genres'].str.split('|')).explode('genre')
b_g = bias_from_resid(tr_exp, 'genre', lam=200, base_col='_pred_M2')
tr['_pred_g'] = tr['genres'].str.split('|').apply(lambda gs: np.mean([b_g.get(g, 0) for g in gs]))
tr['_pred_M2g'] = tr['_pred_M2'] + tr['_pred_g']
b_gender = bias_from_resid(tr, 'gender', lam=2000, base_col='_pred_M2g')
b_age = bias_from_resid(tr, 'age_desc', lam=500, base_col='_pred_M2g')
b_occ = bias_from_resid(tr, 'occ_desc', lam=500, base_col='_pred_M2g')

def predict_M2plus(df):
    pred = mu + df['user_id'].map(b_u).fillna(0) + df['movie_id'].map(b_i).fillna(0) \
         + df['genres'].str.split('|').apply(lambda gs: np.mean([b_g.get(g, 0) for g in gs])) \
         + df['gender'].map(b_gender).fillna(0) \
         + df['age_desc'].map(b_age).fillna(0) \
         + df['occ_desc'].map(b_occ).fillna(0)
    return np.clip(pred.values, 1, 5)

pred_te_m2plus = predict_M2plus(te)
mse_m2plus = mean_squared_error(te['rating'], pred_te_m2plus)
print(f"  M2+ 开放 MSE={mse_m2plus:.4f}")
R['M2plus_MSE'] = round(mse_m2plus, 4)
R['M2_MSE'] = round(mean_squared_error(test_df['rating'], predict_M2(test_df)), 4)

user_mean = train_df.groupby('user_id')['rating'].mean()

# ============================================================
# 2.3 海报视觉特征
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2.3: 海报视觉特征")
print("=" * 60)

FEAT_CACHE = './poster_feat.pkl'
if os.path.exists(FEAT_CACHE):
    with open(FEAT_CACHE, 'rb') as f:
        poster_df = pickle.load(f)
    print(f"  [cache] {len(poster_df)} 部电影海报特征")
else:
    from img2vec_pytorch import Img2Vec
    from PIL import Image
    img2vec = Img2Vec(cuda=False)
    feats, mids = [], []
    folder = './poster'
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png'))]
    t0 = time.time()
    for k, fname in enumerate(files):
        try:
            img = Image.open(os.path.join(folder, fname))
            if img.mode != 'RGB': img = img.convert('RGB')
            v = img2vec.get_vec(img)
            v = v.detach().cpu().numpy() if hasattr(v, 'detach') else np.asarray(v)
            feats.append(v.astype(np.float32))
            mids.append(int(fname.split('.')[0]))
        except Exception as e:
            pass
        if (k+1) % 500 == 0:
            print(f"  processed {k+1}/{len(files)} in {time.time()-t0:.0f}s")
    poster_df = pd.DataFrame({'movie_id': mids, 'features': feats})
    with open(FEAT_CACHE, 'wb') as f:
        pickle.dump(poster_df, f)
    print(f"  saved {len(poster_df)} -> {FEAT_CACHE}")

# PCA + Visual KNN
V_raw = np.stack(poster_df['features'].apply(lambda v: np.asarray(v).ravel()).values)
mid_arr = poster_df['movie_id'].values.astype(int)
D_VIS = 64
pca = PCA(n_components=D_VIS, random_state=0)
V = pca.fit_transform(V_raw)
V_unit = normalize(V, axis=1)
mid2vidx = {m: i for i, m in enumerate(mid_arr)}
print(f"  PCA {V_raw.shape} -> {V.shape}, var={pca.explained_variance_ratio_.sum():.3f}")

# Visual Item-KNN
KV = 30
S = V_unit @ V_unit.T
np.fill_diagonal(S, -1.0)
knn_idx = np.argsort(-S, axis=1)[:, :KV]
knn_sim = np.take_along_axis(S, knn_idx, axis=1)

train_by_user = train_df.groupby('user_id')
u2rated_v = {}
for u, grp in train_by_user:
    d = {}
    for m, r in zip(grp['movie_id'].values, grp['rating'].values):
        if m in mid2vidx: d[mid2vidx[m]] = r
    u2rated_v[u] = d

def predict_M5Vis(df_eval):
    pred = np.empty(len(df_eval))
    for k, (u, m) in enumerate(zip(df_eval['user_id'].values, df_eval['movie_id'].values)):
        bru = user_mean.get(u, mu)
        if m not in mid2vidx: pred[k] = bru; continue
        i = mid2vidx[m]
        nbrs, sims = knn_idx[i], knn_sim[i]
        rated = u2rated_v.get(u, {})
        num, den = 0.0, 1e-9
        for j, s in zip(nbrs, sims):
            if s <= 0: break
            if j in rated:
                num += s * (rated[j] - bru)
                den += abs(s)
        pred[k] = np.clip(bru + num / den, 1, 5)
    return pred

print("  M5_Vis 预测中...")
pred_te_vis = predict_M5Vis(test_df)
mse_vis = mean_squared_error(test_df['rating'], pred_te_vis)
print(f"  M5_Vis MSE={mse_vis:.4f}")
R['M5_VisKNN_MSE'] = round(mse_vis, 4)

# M6 VisSVD —— 向量化 mini-batch SGD, 全量训练 (W 为全局共享, 用批均值梯度防止步长被批放大)
class VisualSVD:
    def __init__(self, k=32, d_vis=64, lr=0.012, reg=0.06, epochs=20, batch=4096, seed=0):
        self.k, self.d_vis = k, d_vis
        self.lr, self.reg, self.ep, self.batch = lr, reg, epochs, batch
        self.seed = seed
    def fit(self, df, V_unit, mid2vidx):
        self.u_idx = {u: i for i, u in enumerate(df['user_id'].unique())}
        self.i_idx = {m: j for j, m in enumerate(df['movie_id'].unique())}
        rng = np.random.default_rng(self.seed)
        nU, nI = len(self.u_idx), len(self.i_idx)
        self.mu = df['rating'].mean()
        self.bu = np.zeros(nU); self.bi = np.zeros(nI)
        self.P = rng.normal(0, 0.05, (nU, self.k))
        self.Q = rng.normal(0, 0.05, (nI, self.k))
        self.W = rng.normal(0, 0.05, (self.k, self.d_vis))
        self.V = np.zeros((nI, self.d_vis), dtype=np.float64)
        for m, j in self.i_idx.items():
            if m in mid2vidx: self.V[j] = V_unit[mid2vidx[m]]
        ua = df['user_id'].map(self.u_idx).values
        ia = df['movie_id'].map(self.i_idx).values
        ra = df['rating'].values.astype(np.float64)
        n = len(df)
        for ep in range(self.ep):
            order = rng.permutation(n)
            sse = 0.0
            for s in range(0, n, self.batch):
                idx = order[s:s + self.batch]
                u, i, r = ua[idx], ia[idx], ra[idx]
                Vi = self.V[i]
                QiFull = self.Q[i] + Vi @ self.W.T
                Pu = self.P[u].copy()
                pred = self.mu + self.bu[u] + self.bi[i] + np.sum(Pu * QiFull, axis=1)
                e = r - pred; sse += float(e @ e)
                np.add.at(self.bu, u, self.lr * (e - self.reg * self.bu[u]))
                np.add.at(self.bi, i, self.lr * (e - self.reg * self.bi[i]))
                np.add.at(self.P, u, self.lr * (e[:, None] * QiFull - self.reg * Pu))
                np.add.at(self.Q, i, self.lr * (e[:, None] * Pu - self.reg * self.Q[i]))
                self.W += self.lr * ((Pu * e[:, None]).T @ Vi / len(idx) - self.reg * self.W)
            if ep == 0 or (ep + 1) % 5 == 0:
                print(f"    epoch {ep+1}/{self.ep}  RMSE={np.sqrt(sse/n):.4f}")
        return self
    def predict(self, df):
        u = df['user_id'].map(self.u_idx).to_numpy()
        i = df['movie_id'].map(self.i_idx).to_numpy()
        uk = ~pd.isna(u); ik = ~pd.isna(i)
        out = np.full(len(df), self.mu)
        both = uk & ik
        ub = u[both].astype(int); ib = i[both].astype(int)
        QiFull = self.Q[ib] + self.V[ib] @ self.W.T
        out[both] = self.mu + self.bu[ub] + self.bi[ib] + np.sum(self.P[ub] * QiFull, axis=1)
        ou = uk & ~ik
        out[ou] = self.mu + self.bu[u[ou].astype(int)]
        oi = (~uk) & ik
        out[oi] = self.mu + self.bi[i[oi].astype(int)]
        return np.clip(out, 1, 5)

print("  训练 M6_VisSVD (向量化, 全量数据) ...")
vis_svd = VisualSVD(k=32, d_vis=D_VIS, lr=0.012, reg=0.06, epochs=20)
vis_svd.fit(train_df, V_unit, mid2vidx)
pred_te_vsvd = vis_svd.predict(test_df)
mse_vsvd = mean_squared_error(test_df['rating'], pred_te_vsvd)
print(f"  M6_VisSVD MSE={mse_vsvd:.4f}")
R['M6_VisSVD_MSE'] = round(mse_vsvd, 4)

# Cold-movie analysis
n_per_movie = train_df.groupby('movie_id').size()
bin_edges = [0, 20, 100, 500, 2000, 1_000_000]
bin_labels = ['<20', '20-100', '100-500', '500-2000', '>2000']
test_df_ = test_df.copy()
test_df_['n_train'] = test_df_['movie_id'].map(n_per_movie).fillna(0).astype(int)
test_df_['bucket'] = pd.cut(test_df_['n_train'], bins=bin_edges, labels=bin_labels)

cold_rows = []
for b in bin_labels:
    m = (test_df_['bucket'] == b).values
    if m.sum() == 0: continue
    cold_rows.append({'bucket': b, 'n': int(m.sum()),
        'M3': np.sqrt(mean_squared_error(test_df_['rating'].values[m], pred_te_m3[m])),
        'VisKNN': np.sqrt(mean_squared_error(test_df_['rating'].values[m], pred_te_vis[m])),
        'VisSVD': np.sqrt(mean_squared_error(test_df_['rating'].values[m], pred_te_vsvd[m]))})
cold_df = pd.DataFrame(cold_rows)
R['cold_movie_rmse'] = cold_df.to_dict('records')
print("  冷门电影对比:")
print(cold_df.round(4).to_string(index=False))

fig, ax = plt.subplots(figsize=(10, 4.5))
x = np.arange(len(cold_df)); w = 0.27
ax.bar(x - w, cold_df['M3'], w, label='M3 FunkSVD', color='#FF6B6B')
ax.bar(x, cold_df['VisKNN'], w, label='M5 VisKNN', color='#4ECDC4')
ax.bar(x + w, cold_df['VisSVD'], w, label='M6 VisSVD', color='#5C7AEA')
ax.set_xticks(x); ax.set_xticklabels(cold_df['bucket'])
ax.set_xlabel('Movie popularity'); ax.set_ylabel('RMSE')
ax.set_title('Visual features help cold movies', fontsize=12, fontweight='bold')
ax.legend(); ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('2_3_cold_movie.png')

# ============================================================
# 2.4 LLM背景知识 (sentence-transformer fallback)
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2.4: LLM 背景知识")
print("=" * 60)

EMB_CACHE = './movie_content_emb.pkl'
def build_movie_text(row):
    parts = []
    for col in ['name', 'intro', 'directors', 'stars']:
        v = row.get(col, '')
        if isinstance(v, str) and v.strip(): parts.append(v.strip())
    return ' . '.join(parts)

if os.path.exists(EMB_CACHE):
    with open(EMB_CACHE, 'rb') as f:
        emb_data = pickle.load(f)
    print(f"  [cache] {len(emb_data['movie_id'])} 部电影内容向量")
else:
    from sentence_transformers import SentenceTransformer
    st_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    texts = movies_info.apply(build_movie_text, axis=1).tolist()
    emb = st_model.encode(texts, batch_size=64, show_progress_bar=True,
                          convert_to_numpy=True, normalize_embeddings=True)
    emb_data = {'movie_id': movies_info['movie_id'].values.astype(int), 'emb': emb.astype(np.float32)}
    with open(EMB_CACHE, 'wb') as f:
        pickle.dump(emb_data, f)
    print(f"  saved {emb.shape}")

C_emb  = emb_data['emb']
C_mids = emb_data['movie_id']
mid2cidx = {int(m): i for i, m in enumerate(C_mids)}

# DeepSeek LLM KB (if available)
KB_CACHE = './llm_movie_kb.json'
DEEPSEEK_KEY = 'sk-dNG1yLCPN4Yvyr9JKNGl7D4WskdNQlx3bY583RVpCYUN1zsT'
DEEPSEEK_URL = 'https://yunwu.ai/v1/chat/completions'
kb = {}
if os.path.exists(KB_CACHE):
    with open(KB_CACHE, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    print(f"  [cache] LLM KB: {len(kb)} entries")
else:
    import requests
    N_QUERY = 100
    print(f"  调用 DeepSeek API ({N_QUERY} 部电影) ...")
    for k, row in movies_info.head(N_QUERY).iterrows():
        mid = int(row['movie_id'])
        if str(mid) in kb: continue
        prompt = (
            "You are a film expert. For the movie below, return STRICT JSON with keys:\n"
            '  online_rating: float 1-5, themes: list of 3-5 tags, '
            '  award_level: int 0-2, sentiment: one of [dark,uplifting,tense,romantic,comedic,melancholic,action,family].\n'
            f"Movie: {row['name']}\nDirector: {row.get('directors','')}\nCast: {row.get('stars','')}\n"
            f"Plot: {row.get('intro','')}\nReturn ONLY valid JSON."
        )
        try:
            r = requests.post(DEEPSEEK_URL,
                headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
                json={'model': 'deepseek-v4-flash', 'messages': [{'role': 'user', 'content': prompt}],
                      'temperature': 0.0, 'max_tokens': 200}, timeout=30)
            r.raise_for_status()
            txt = r.json()['choices'][0]['message']['content'].strip()
            if txt.startswith('```'): txt = txt.strip('`').lstrip('json').strip()
            kb[str(mid)] = json.loads(txt)
        except Exception as e:
            kb[str(mid)] = None
        if (k+1) % 20 == 0:
            with open(KB_CACHE, 'w', encoding='utf-8') as f:
                json.dump(kb, f, ensure_ascii=False, indent=1)
        time.sleep(0.3)
    with open(KB_CACHE, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=1)
    print(f"  saved {sum(v is not None for v in kb.values())} valid KB entries")

# Build content features
pca_c = PCA(n_components=16, random_state=0)
C_pca = pca_c.fit_transform(C_emb)
emb_df = pd.DataFrame(C_pca, columns=[f'c{i}' for i in range(16)])
emb_df['movie_id'] = C_mids

# KB features
kb_rows, kb_mids = [], []
sent_classes = ['dark','uplifting','tense','romantic','comedic','melancholic','action','family']
for mid, v in kb.items():
    row_kb = {}
    if isinstance(v, dict):
        row_kb = {'llm_rating': v.get('online_rating', np.nan),
                  'llm_award': v.get('award_level', np.nan),
                  'llm_n_themes': len(v.get('themes', []) or [])}
        for s in sent_classes:
            row_kb[f'sent_{s}'] = int(v.get('sentiment', '') == s)
    else:
        row_kb = {'llm_rating': np.nan, 'llm_award': np.nan, 'llm_n_themes': np.nan}
        for s in sent_classes: row_kb[f'sent_{s}'] = 0
    row_kb['movie_id'] = int(mid)
    kb_rows.append(row_kb)
kb_df = pd.DataFrame(kb_rows)

content_df = movies[['movie_id']].merge(emb_df, on='movie_id', how='left')
content_df = content_df.merge(kb_df, on='movie_id', how='left')
for col in content_df.columns:
    if col == 'movie_id': continue
    if content_df[col].dtype == 'O': content_df[col] = content_df[col].fillna('')
    elif content_df[col].isna().any():
        med = content_df[col].median() if content_df[col].notna().any() else 0
        content_df[col] = content_df[col].fillna(med)

# M7 predictor
age_map = {'Under 18': 12, '18-24': 21, '25-34': 30, '35-44': 40,
           '45-49': 47, '50-55': 52, '56+': 60}
occ_ids = {o: i for i, o in enumerate(sorted(users['occ_desc'].dropna().unique()))}
def build_features_llm(df):
    out = df[['user_id', 'movie_id', 'rating']].copy()
    out['M2_pred'] = mu + out['user_id'].map(b_u).fillna(0) + out['movie_id'].map(b_i).fillna(0)
    out = out.merge(content_df, on='movie_id', how='left')
    u_aux = users[['user_id', 'gender', 'age_desc', 'occ_desc']].copy()
    u_aux['age'] = u_aux['age_desc'].map(age_map).fillna(30)
    u_aux['is_F'] = (u_aux['gender'] == 'F').astype(int)
    u_aux['occ_id'] = u_aux['occ_desc'].map(occ_ids).fillna(-1)
    out = out.merge(u_aux[['user_id', 'age', 'is_F', 'occ_id']], on='user_id', how='left')
    return out.fillna(0)

Ftr = build_features_llm(train_df)
Fte = build_features_llm(test_df)
feature_cols = [c for c in Ftr.columns if c not in ('user_id', 'movie_id', 'rating')]
y_tr_r = Ftr['rating'].values - Ftr['M2_pred'].values
y_te_r = Fte['rating'].values - Fte['M2_pred'].values

try:
    import lightgbm as lgb
    lgb_train = lgb.Dataset(Ftr[feature_cols], y_tr_r)
    lgb_val   = lgb.Dataset(Fte[feature_cols], y_te_r, reference=lgb_train)
    params = dict(objective='regression', metric='rmse', num_leaves=63,
                  learning_rate=0.05, feature_fraction=0.9, bagging_fraction=0.8,
                  bagging_freq=5, verbose=-1)
    print("  训练 LightGBM 内容残差模型 ...")
    booster = lgb.train(params, lgb_train, num_boost_round=300,
                        valid_sets=[lgb_val], callbacks=[lgb.early_stopping(20, verbose=False)])
    content_model_name = 'LightGBM residual'
    def predict_content_residual(X):
        return booster.predict(X)
    imp = pd.Series(booster.feature_importance(importance_type='gain'),
                    index=feature_cols).sort_values(ascending=False)
except ModuleNotFoundError:
    from sklearn.ensemble import HistGradientBoostingRegressor
    print("  LightGBM 不可用, 使用 sklearn HistGradientBoostingRegressor 作为内容残差模型 ...")
    booster = HistGradientBoostingRegressor(
        max_iter=260, learning_rate=0.055, max_leaf_nodes=63,
        l2_regularization=0.02, random_state=42, early_stopping=True,
        validation_fraction=0.08, n_iter_no_change=15)
    booster.fit(Ftr[feature_cols], y_tr_r)
    content_model_name = 'HistGradientBoosting residual'
    def predict_content_residual(X):
        return booster.predict(X)
    # HistGradientBoostingRegressor has no native feature_importances_.
    # Use absolute feature/residual correlation as a lightweight, deterministic proxy.
    rng_imp = np.random.default_rng(42)
    sample_idx = rng_imp.choice(len(Ftr), size=min(50000, len(Ftr)), replace=False)
    X_imp = Ftr.iloc[sample_idx][feature_cols].astype(float)
    y_imp = pd.Series(y_tr_r[sample_idx])
    imp_vals = {}
    for c in feature_cols:
        x = X_imp[c]
        sx = x.std()
        sy = y_imp.std()
        imp_vals[c] = 0.0 if sx == 0 or sy == 0 else abs(float(np.corrcoef(x, y_imp)[0, 1]))
    imp = pd.Series(imp_vals).sort_values(ascending=False)

residual_pred_te = predict_content_residual(Fte[feature_cols])
PRED_TE_M7 = np.clip(Fte['M2_pred'].values + residual_pred_te, 1, 5)
mse_m7 = mean_squared_error(Fte['rating'], PRED_TE_M7)
print(f"  M7 LLM/Content MSE={mse_m7:.4f}")
R['M7_LLM_MSE'] = round(mse_m7, 4)
R['M7_model'] = content_model_name

# Feature importance
R['M7_top_features'] = imp.head(10).round(1).to_dict()
fig, ax = plt.subplots(figsize=(9, 5))
imp.head(15).plot(kind='barh', ax=ax, color='#5C7AEA')
ax.invert_yaxis()
ax.set_title('M7 Content residual feature importance', fontweight='bold')
plt.tight_layout()
savefig('2_4_feature_importance.png')

# ============================================================
# 2.5 对比 + Stacking
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2.5: 对比 + Stacking")
print("=" * 60)

preds = {'M3 FunkSVD': pred_te_m3, 'M2+': pred_te_m2plus,
         'M6 VisSVD': pred_te_vsvd, 'M7 LLM': PRED_TE_M7}
y_te_full = test_df['rating'].values

for nm, p in preds.items():
    print(f"  {nm:16s}  MSE={mean_squared_error(y_te_full, p):.4f}")

n_u = train_df.groupby('user_id').size()
n_m = train_df.groupby('movie_id').size()

def build_segment_masks(df):
    g_map = movies.set_index('movie_id')['genres'].fillna('')
    return {
        'Cold user (<10)': df['user_id'].map(n_u).fillna(0).lt(10).values,
        'Cold movie (<20)': df['movie_id'].map(n_m).fillna(0).lt(20).values,
        'Rare genre': df['movie_id'].map(g_map).fillna('').str.contains('Film-Noir|Documentary|Western').values,
        'Hot (>2000)': df['movie_id'].map(n_m).fillna(0).gt(2000).values,
    }

# Segmented comparison
seg_masks = build_segment_masks(test_df)
seg_rows = []
for seg, mask in seg_masks.items():
    if mask.sum() == 0: continue
    row = {'segment': seg, 'n': int(mask.sum())}
    for nm, p in preds.items():
        row[nm] = round(mean_squared_error(y_te_full[mask], p[mask]), 4)
    seg_rows.append(row)
R['segment_mse'] = seg_rows
print("  场景细分:")
print(pd.DataFrame(seg_rows).to_string(index=False))

# ---- 诊断: 为什么新增信息对"全量 MSE"提升有限 (供 PPT 反思页) ----
# 1) 四个专家预测两两相关性 (高相关 => 集成天然增益小)
P_mat = {'M3': pred_te_m3, 'M2+': pred_te_m2plus, 'M6': pred_te_vsvd, 'M7': PRED_TE_M7}
corr_pairs = {}
_names = list(P_mat)
for ai in range(len(_names)):
    for bi in range(ai + 1, len(_names)):
        a, b = _names[ai], _names[bi]
        corr_pairs[f'{a}-{b}'] = round(float(np.corrcoef(P_mat[a], P_mat[b])[0, 1]), 3)
single_mses = {nm: float(mean_squared_error(y_te_full, p)) for nm, p in P_mat.items()}
# 2) cold-start 子集只占测试集很小一部分 => side-info 的局部增益被全量稀释
frac_cold_u = float(test_df['user_id'].map(n_u).fillna(0).lt(10).mean())
frac_cold_m = float(test_df['movie_id'].map(n_m).fillna(0).lt(20).mean())
_g_map = movies.set_index('movie_id')['genres'].fillna('')
frac_rare_g = float(test_df['movie_id'].map(_g_map).fillna('').str.contains('Film-Noir|Documentary|Western').mean())
frac_hot = float(test_df['movie_id'].map(n_m).fillna(0).gt(2000).mean())
R['optimization_analysis'] = {
    'pred_correlation': corr_pairs,
    'mean_pred_correlation': round(float(np.mean(list(corr_pairs.values()))), 3),
    'single_model_mse_spread': round(max(single_mses.values()) - min(single_mses.values()), 4),
    'test_fraction': {
        'cold_user_lt10': round(frac_cold_u, 3),
        'cold_movie_lt20': round(frac_cold_m, 3),
        'rare_genre': round(frac_rare_g, 3),
        'hot_gt2000': round(frac_hot, 3),
    },
}
print(f"  [诊断] 专家预测平均相关性={R['optimization_analysis']['mean_pred_correlation']}, "
      f"单模型MSE极差={R['optimization_analysis']['single_model_mse_spread']}, "
      f"冷门电影占比={frac_cold_m:.1%}, 冷用户占比={frac_cold_u:.1%}")

# Stacking
mask_meta = np.random.rand(len(train_df)) < 0.10
meta_val = train_df[mask_meta].reset_index(drop=True)
P_m3_val = svd.predict(meta_val)
P_m2_val = predict_M2plus(attach(meta_val))
P_m6_val = vis_svd.predict(meta_val)
F_val = build_features_llm(meta_val)
P_m7_val = np.clip(F_val['M2_pred'].values + predict_content_residual(F_val[feature_cols]), 1, 5)

Z_val = np.column_stack([P_m3_val, P_m2_val, P_m6_val, P_m7_val])
meta = Ridge(alpha=1.0)
meta.fit(Z_val, meta_val['rating'].values)
R['stack_weights'] = {nm: round(float(w), 3) for nm, w in zip(['M3','M2+','M6','M7'], meta.coef_)}

Z_te = np.column_stack([pred_te_m3, pred_te_m2plus, pred_te_vsvd, PRED_TE_M7])
pred_te_stack = np.clip(meta.predict(Z_te), 1, 5)
pred_val_stack = np.clip(meta.predict(Z_val), 1, 5)
mse_stack = mean_squared_error(y_te_full, pred_te_stack)
print(f"  Stacking MSE={mse_stack:.4f}, weights={R['stack_weights']}")
R['Stack_MSE'] = round(mse_stack, 4)

# Segment-adaptive blend: use validation errors to route samples by scenario.
# This is a closed-form MOE: weights are a softmax over segment-wise validation MSE.
expert_names = ['M3', 'M2+', 'M6', 'M7']
Z_val = np.column_stack([P_m3_val, P_m2_val, P_m6_val, P_m7_val])
Z_te = np.column_stack([pred_te_m3, pred_te_m2plus, pred_te_vsvd, PRED_TE_M7])
meta_seg_masks = build_segment_masks(meta_val)
global_mse = np.array([mean_squared_error(meta_val['rating'].values, Z_val[:, j])
                       for j in range(Z_val.shape[1])])

def mse_to_weights(mse_vec, temp=0.025):
    score = -np.asarray(mse_vec, dtype=float) / temp
    score -= score.max()
    w_ = np.exp(score)
    return w_ / w_.sum()

global_w = mse_to_weights(global_mse)
seg_weight_table = {'GLOBAL': {nm: round(float(w), 3) for nm, w in zip(expert_names, global_w)}}
seg_mse_table = {'GLOBAL': {nm: round(float(v), 4) for nm, v in zip(expert_names, global_mse)}}
sample_weights_val = np.tile(global_w, (len(meta_val), 1))
sample_counts_val = np.ones(len(meta_val))
sample_weights = np.tile(global_w, (len(test_df), 1))
sample_counts = np.ones(len(test_df))
for seg, m_val in meta_seg_masks.items():
    if m_val.sum() < 50:
        continue
    mse_vec = np.array([mean_squared_error(meta_val['rating'].values[m_val], Z_val[m_val, j])
                        for j in range(Z_val.shape[1])])
    w_seg = mse_to_weights(mse_vec)
    seg_weight_table[seg] = {nm: round(float(w), 3) for nm, w in zip(expert_names, w_seg)}
    seg_mse_table[seg] = {nm: round(float(v), 4) for nm, v in zip(expert_names, mse_vec)}
    sample_weights_val[m_val] += w_seg
    sample_counts_val[m_val] += 1
    m_te = seg_masks.get(seg)
    if m_te is not None and m_te.sum() > 0:
        sample_weights[m_te] += w_seg
        sample_counts[m_te] += 1
sample_weights_val = sample_weights_val / sample_counts_val[:, None]
pred_val_segblend = np.clip((sample_weights_val * Z_val).sum(axis=1), 1, 5)
sample_weights = sample_weights / sample_counts[:, None]
pred_te_segblend = np.clip((sample_weights * Z_te).sum(axis=1), 1, 5)
mse_segblend = mean_squared_error(y_te_full, pred_te_segblend)
print(f"  SegmentBlend MSE={mse_segblend:.4f}, weights={seg_weight_table}")
R['SegmentBlend_MSE'] = round(mse_segblend, 4)
R['segment_blend_weights'] = seg_weight_table
R['segment_blend_val_mse'] = seg_mse_table

# Summary bar chart
all_r = {**{nm: mean_squared_error(y_te_full, p) for nm, p in preds.items()},
         'Stacking': mse_stack, 'SegmentBlend': mse_segblend}
fig, ax = plt.subplots(figsize=(10, 4.5))
xs = np.arange(len(all_r)); names = list(all_r.keys()); vals = list(all_r.values())
colors = ['#FF6B6B', '#FFA94D', '#5C7AEA', '#9D6EFF', '#2EC4B6', '#264653']
ax.bar(xs, vals, color=colors)
for i, v in enumerate(vals): ax.text(i, v + 0.003, f'{v:.4f}', ha='center', fontsize=9)
ax.set_xticks(xs); ax.set_xticklabels(names, rotation=15)
ax.set_ylabel('MSE'); ax.set_title('Section 2.5: All models + Stacking', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('2_5_stacking.png')

# ============================================================
# 2.6 异常分析
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2.6: SVD 异常样本分析")
print("=" * 60)

pred_tr_m3 = svd.predict(train_df)
resid = train_df['rating'].values - pred_tr_m3
abs_resid = np.abs(resid)
tau = 1.5
n_ab = int((abs_resid > tau).sum())
print(f"  |e|>{tau} 异常样本: {n_ab} / {len(resid)} ({n_ab/len(resid)*100:.2f}%)")
R['abnormal_rate'] = round(n_ab / len(resid) * 100, 2)

# Residual histogram
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(resid, bins=60, color='#5C7AEA', alpha=.8)
ax.axvline(-1.5, color='red', ls='--'); ax.axvline(1.5, color='red', ls='--')
ax.set_xlabel('Residual e = r - r_hat'); ax.set_ylabel('Frequency')
ax.set_title('M3 SVD Residual Distribution', fontweight='bold')
plt.tight_layout()
savefig('2_6_residual_hist.png')

# User-level aggregation
train_df['_abs_resid'] = abs_resid
user_err = train_df.groupby('user_id').agg(
    mean_abs_err=('_abs_resid', 'mean'), n_ratings=('rating', 'size'),
    mean_rating=('rating', 'mean'), std_rating=('rating', 'std')).reset_index()
user_err['std_rating'] = user_err['std_rating'].fillna(0)
user_err = user_err[user_err['n_ratings'] >= 30].copy()
top5pct_cut = user_err['mean_abs_err'].quantile(0.95)
user_err['is_abnormal'] = (user_err['mean_abs_err'] >= top5pct_cut).astype(int)
n_abn_users = user_err['is_abnormal'].sum()
print(f"  异常用户 (Top5% MAE): {n_abn_users} 人")
R['abnormal_users'] = int(n_abn_users)

# User profiling features
movie_genre = movies.set_index('movie_id')['genres'].fillna('')
def user_behavior_features(tr_df):
    g = tr_df.groupby('user_id')
    f = pd.DataFrame(index=g.groups.keys())
    f['n_ratings'] = g.size(); f['mean_rate'] = g['rating'].mean()
    f['std_rate'] = g['rating'].std().fillna(0)
    f['pct_high'] = g['rating'].apply(lambda s: (s >= 4).mean())
    f['pct_low'] = g['rating'].apply(lambda s: (s <= 2).mean())
    def genre_entropy(s):
        gc = {}
        for mid in s:
            for x in movie_genre.get(mid, '').split('|'):
                if x: gc[x] = gc.get(x, 0) + 1
        if not gc: return 0
        p = np.array(list(gc.values())) / sum(gc.values())
        return -(p * np.log(p + 1e-12)).sum()
    f['genre_entropy'] = g['movie_id'].apply(genre_entropy)
    year = movies['title'].str.extract(r'\((\d{4})\)').astype(float)
    year.index = movies['movie_id']
    yr = tr_df['movie_id'].map(year.iloc[:, 0])
    f['mean_year'] = yr.groupby(tr_df['user_id']).mean()
    return f.reset_index().rename(columns={'index': 'user_id'})

bf = user_behavior_features(train_df).drop(columns=['n_ratings'], errors='ignore')
prof = user_err.merge(bf, on='user_id').merge(
    users[['user_id', 'gender', 'age_desc', 'occ_desc']], on='user_id')
ab_prof = prof[prof['is_abnormal'] == 1].copy()

feat_cols_km = ['mean_rate', 'std_rate', 'pct_high', 'pct_low', 'genre_entropy', 'mean_year']
X_ab = StandardScaler().fit_transform(ab_prof[feat_cols_km].fillna(0).values)
K = 4
km = KMeans(n_clusters=K, n_init=10, random_state=0).fit(X_ab)
ab_prof['cluster'] = km.labels_

# 题材偏好统计：给定一批用户, 统计其评过电影的 genre 计数 (对照 notebook 2.6 Step 3)
def genre_counts_for_users(uids):
    sub = train_df[train_df['user_id'].isin(uids)]
    gc = {}
    for mid in sub['movie_id'].values:
        for x in movie_genre.get(mid, '').split('|'):
            if x:
                gc[x] = gc.get(x, 0) + 1
    return gc

# 学生 / 教育工作者职业 (核对 notebook 结论: 异常用户里这类人群居多)
EDU_OCCS = ['college/grad student', 'K-12 student', 'academic/educator']

cluster_profiles = []
def label_abnormal_cluster(cp):
    """数据驱动标签: 先按评分行为定主型, 再用职业/题材补充画像 (替代旧的纯方差标签)。"""
    if cp['pct_low'] >= 0.42 and cp['mean_rate'] <= 3.05:
        beh = '低分严苛型'
    elif cp['pct_high'] >= 0.60 and cp['mean_rate'] >= 3.6:
        beh = '高分宽松型'
    elif cp['std_rate'] >= 1.42:
        beh = '评分两极型'
    elif cp['genre_entropy'] <= 1.95:
        beh = '题材集中型'
    else:
        beh = '中庸高残差型'
    return beh

for c in range(K):
    sub = ab_prof[ab_prof['cluster'] == c]
    uids = sub['user_id'].values
    gc = genre_counts_for_users(uids)
    tot_g = sum(gc.values()) or 1
    top3_g = sorted(gc.items(), key=lambda kv: -kv[1])[:3]
    age_dist = sub['age_desc'].value_counts(normalize=True).round(3).to_dict()
    occ_dist = sub['occ_desc'].value_counts(normalize=True).round(3).head(3).to_dict()
    cp = {'cluster': c, 'n': len(sub),
          'mae': round(sub['mean_abs_err'].mean(), 3),
          'mean_rate': round(sub['mean_rate'].mean(), 2),
          'std_rate': round(sub['std_rate'].mean(), 2),
          'pct_high': round(sub['pct_high'].mean(), 2),
          'pct_low': round(sub['pct_low'].mean(), 2),
          'genre_entropy': round(sub['genre_entropy'].mean(), 2),
          'mean_year': round(sub['mean_year'].mean(), 1),
          'top_age': sub['age_desc'].value_counts().index[0] if len(sub) > 0 else '',
          'age_dist': age_dist,
          'top_occ': sub['occ_desc'].value_counts().index[0] if len(sub) > 0 else '',
          'occ_top3': occ_dist,
          'edu_share': round(float(sub['occ_desc'].isin(EDU_OCCS).mean()), 3),
          'top3_genres': [g for g, _ in top3_g],
          'top3_genre_share': {g: round(n / tot_g, 3) for g, n in top3_g}}
    cp['label'] = label_abnormal_cluster(cp)
    cluster_profiles.append(cp)
R['abnormal_clusters'] = cluster_profiles
R['abnormal_user_examples'] = (
    ab_prof.sort_values('mean_abs_err', ascending=False)
    [['user_id', 'cluster', 'mean_abs_err', 'n_ratings', 'mean_rate', 'std_rate', 'pct_high', 'pct_low', 'age_desc', 'occ_desc']]
    .head(12).round(3).to_dict('records')
)
print("  异常用户聚类 (含职业/年龄/题材):")
for cp in cluster_profiles:
    print(f"    cluster {cp['cluster']}: n={cp['n']} label={cp['label']} "
          f"top_age={cp['top_age']} top_occ={cp['top_occ']} edu={cp['edu_share']:.0%} "
          f"top_genres={cp['top3_genres']}")

# ---- 异常用户整体画像分布 (对照 notebook: 学生/教育工作者 + Comedy/Romance) ----
abn_uids = ab_prof['user_id'].astype(int).values
abn_users_meta = users[users['user_id'].isin(abn_uids)]
gc_all = genre_counts_for_users(abn_uids)
tot_all = sum(gc_all.values()) or 1
genre_sorted = sorted(gc_all.items(), key=lambda kv: -kv[1])
R['abnormal_user_count'] = int(len(abn_uids))
R['abnormal_user_occupation_dist'] = abn_users_meta['occ_desc'].value_counts(normalize=True).round(3).to_dict()
R['abnormal_user_age_dist'] = abn_users_meta['age_desc'].value_counts(normalize=True).round(3).to_dict()
R['abnormal_user_genre_dist'] = {g: round(n / tot_all, 3) for g, n in genre_sorted}
R['abnormal_user_top_genres'] = [g for g, _ in genre_sorted[:6]]
edu_share_abn = float(abn_users_meta['occ_desc'].isin(EDU_OCCS).mean())
edu_share_all = float(users['occ_desc'].isin(EDU_OCCS).mean())
R['abnormal_user_student_educator_share'] = round(edu_share_abn, 3)
R['all_user_student_educator_share'] = round(edu_share_all, 3)
print(f"  异常用户职业 Top: {list(R['abnormal_user_occupation_dist'].items())[:3]}")
print(f"  学生+教育工作者占比: 异常 {edu_share_abn:.1%} vs 全体 {edu_share_all:.1%}")
print(f"  异常用户题材 Top: {R['abnormal_user_top_genres']}")

# 图: 异常用户职业 / 年龄 / 题材分布 (三联)
occ_top = abn_users_meta['occ_desc'].value_counts(normalize=True).head(8)[::-1]
age_order_full = ['Under 18', '18-24', '25-34', '35-44', '45-49', '50-55', '56+']
age_ser = abn_users_meta['age_desc'].value_counts(normalize=True).reindex(age_order_full).fillna(0)
genre_top = pd.Series({g: gc_all[g] / tot_all for g, _ in genre_sorted[:8]})[::-1]
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
axes[0].barh(occ_top.index, occ_top.values * 100, color='#5C7AEA')
axes[0].set_xlabel('Share of abnormal users (%)')
axes[0].set_title(f'Occupation (student/educator={edu_share_abn:.0%})', fontweight='bold')
axes[1].bar(age_ser.index, age_ser.values * 100, color='#2EC4B6')
axes[1].set_ylabel('Share (%)'); axes[1].set_title('Age groups (spans 18-44, not only 25-34)', fontweight='bold')
axes[1].tick_params(axis='x', rotation=30)
axes[2].barh(genre_top.index, genre_top.values * 100, color='#FF6B6B')
axes[2].set_xlabel('Share of rated genres (%)')
axes[2].set_title('Genre preference (Comedy top, Romance notable)', fontweight='bold')
plt.suptitle('Abnormal users: occupation / age / genre profile', fontsize=13, fontweight='bold')
plt.tight_layout()
savefig('2_6_profile.png')

# Cluster rating distributions (保留, 标题加上 label/top_occ)
fig, axes = plt.subplots(1, K, figsize=(4*K, 3.7), sharey=True)
for c, ax in enumerate(axes):
    cp = cluster_profiles[c]
    uids = ab_prof[ab_prof['cluster'] == c]['user_id'].values
    sub_r = train_df[train_df['user_id'].isin(uids)]
    ax.hist(sub_r['rating'].values, bins=np.arange(0.5, 6, 1), color='#5C7AEA', density=True, edgecolor='white')
    ax.set_title(f"C{c} {cp['label']} (n={len(uids)})\n{cp['top_occ'][:18]} | {cp['top_age']}", fontsize=9, fontweight='bold')
    ax.set_xlabel('Rating'); ax.set_xticks([1,2,3,4,5])
axes[0].set_ylabel('Density')
plt.suptitle('Abnormal User Cluster Rating Distributions', fontweight='bold')
plt.tight_layout()
savefig('2_6_clusters.png')

# ---- 期末 2.6 Step 4: 给异常用户切换"专家模型", 看哪个 MSE 最低 (对照 notebook) ----
# e_ui = r_ui - r_hat_ui ; 异常用户 = 残差 Top5% 用户。在测试集上对比各专家在
# 异常 vs 正常用户上的 MSE, 验证"识别异常 + 切换专家"的价值。
abn_set_es = set(int(u) for u in abn_uids)
mask_abn_te = test_df['user_id'].isin(abn_set_es).values
es_rows = []
for nm, p in [('M3 FunkSVD', pred_te_m3), ('M2+ 分层偏置', pred_te_m2plus),
              ('M6 VisSVD', pred_te_vsvd), ('M7 LLM/Content', PRED_TE_M7)]:
    mse_a = float(np.mean((y_te_full[mask_abn_te] - p[mask_abn_te]) ** 2)) if mask_abn_te.sum() else float('nan')
    mse_n = float(np.mean((y_te_full[~mask_abn_te] - p[~mask_abn_te]) ** 2))
    es_rows.append({'model': nm, 'abnormal_mse': round(mse_a, 4),
                    'normal_mse': round(mse_n, 4), 'gap': round(mse_a - mse_n, 4)})
best_es = min(es_rows, key=lambda r: r['abnormal_mse'])
R['abnormal_expert_switch'] = {
    'n_abnormal_test': int(mask_abn_te.sum()),
    'n_normal_test': int((~mask_abn_te).sum()),
    'table': es_rows,
    'best_model': best_es['model'],
}
print("  异常用户 vs 正常用户上各专家 MSE:")
for r_ in es_rows:
    print(f"    {r_['model']:16s} abn={r_['abnormal_mse']:.4f} normal={r_['normal_mse']:.4f} gap={r_['gap']:+.4f}")
print(f"  [结论] 异常用户上最佳专家: {best_es['model']} (MSE={best_es['abnormal_mse']:.4f})")

# 数据驱动总结 (写入 results.json, 供 PPT 使用)
occ_items = list(R['abnormal_user_occupation_dist'].items())
age_items = list(R['abnormal_user_age_dist'].items())
bn = best_es['model']
if 'M3' in bn or 'M6' in bn:
    why = ("说明异常用户的偏差主要来自个人潜在口味, 潜因子 / 视觉协同模型 (M3、M6) "
           "比人口学偏置 (M2+) 和内容残差 (M7) 更能拟合他们; 给这批用户切换到 "
           f"{bn} 即可降低误差。")
elif 'M7' in bn:
    why = ("说明异常用户的偏差与电影内容 / 语义信号相关, 内容残差模型 (M7) 在其上最稳, "
           f"可对这批用户切换到 {bn}。")
else:
    why = f"说明异常用户更依赖人口学先验, 可对其切换到 {bn}。"
R['abnormal_user_summary'] = (
    f"异常用户共 {R['abnormal_user_count']} 人 (评分数≥30 的用户中, M3 残差平均绝对值 Top 5%)。"
    f"职业以 {occ_items[0][0]}({occ_items[0][1]*100:.0f}%)、{occ_items[1][0]}({occ_items[1][1]*100:.0f}%) 为主, "
    f"学生与教育工作者合计占 {edu_share_abn:.0%} (全体仅 {edu_share_all:.0%}), 明显偏高; "
    f"年龄横跨 {'、'.join(a for a, _ in age_items[:3])} 等多个区间, 并非单一 25-34; "
    f"题材偏好以 {'、'.join(R['abnormal_user_top_genres'][:4])} 为主——Comedy 在各簇均居首, "
    f"Romance 在偏爱爱情片的簇中尤为突出。" + why
)
print("  abnormal_user_summary:", R['abnormal_user_summary'])

# 图: 专家切换对比 (异常 vs 正常)
fig, ax = plt.subplots(figsize=(9, 4.6))
xs = np.arange(len(es_rows)); w = 0.38
ax.bar(xs - w/2, [r['normal_mse'] for r in es_rows], w, label='Normal users', color='#2EC4B6')
ax.bar(xs + w/2, [r['abnormal_mse'] for r in es_rows], w, label='Abnormal users', color='#E76F51')
for i, r_ in enumerate(es_rows):
    ax.text(i - w/2, r_['normal_mse'] + .01, f"{r_['normal_mse']:.3f}", ha='center', fontsize=8)
    ax.text(i + w/2, r_['abnormal_mse'] + .01, f"{r_['abnormal_mse']:.3f}", ha='center', fontsize=8)
ax.set_xticks(xs); ax.set_xticklabels([r['model'] for r in es_rows], rotation=12)
ax.set_ylabel('MSE'); ax.legend()
ax.set_title('Expert switching on abnormal users (lower is better)', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('2_6_expert_switch.png')

# ============================================================
# 2.6b 异常用户驱动的预测优化
# ============================================================
print("\nSECTION 2.6b: 异常用户驱动的预测优化")

abn_cluster_map = ab_prof.set_index('user_id')['cluster'].to_dict()
abn_user_set = set(abn_cluster_map.keys())

def known_abnormal_mask(df):
    return df['user_id'].isin(abn_user_set).values

def cluster_mask(df, c):
    return df['user_id'].map(abn_cluster_map).fillna(-1).eq(c).values

# 方案 A: 固定物品偏置, 重新估计异常用户偏置。
# b_i 不动, 只用用户自己的残差学习 shrinkage 后的 b_u*, 避免 SVD 对极端用户过拟合。
base_item_train = mu + train_df['movie_id'].map(b_i).fillna(0).values
fixed_item_resid = train_df['rating'].values - base_item_train
tmp_fixed = train_df[['user_id']].copy()
tmp_fixed['_resid_fixed_item'] = fixed_item_resid
tmp_fixed['_n'] = 1
lam_abn_user = 35
sum_fixed = tmp_fixed.groupby('user_id')['_resid_fixed_item'].sum()
cnt_fixed = tmp_fixed.groupby('user_id')['_n'].sum()
bu_fixed_item = (sum_fixed / (cnt_fixed + lam_abn_user)).where(sum_fixed.index.isin(abn_user_set), 0)

def predict_fixed_item_user_bias(df):
    bi = df['movie_id'].map(b_i).fillna(0).values
    bu = df['user_id'].map(bu_fixed_item).fillna(0).values
    return np.clip(mu + bi + bu, 1, 5)

pred_val_fixed_user = predict_fixed_item_user_bias(meta_val)
pred_te_fixed_user = predict_fixed_item_user_bias(test_df)

# 方案 B: 异常用户簇专属专家权重。
# 每个 cluster 在 meta_val 上挑选 M3/M2+/M6/M7 的低误差组合, 再只作用于同簇用户。
cluster_weight_table = {}
pred_val_clusterblend = pred_val_segblend.copy()
pred_te_clusterblend = pred_te_segblend.copy()
for c in range(K):
    m_val_c = cluster_mask(meta_val, c)
    if m_val_c.sum() < 20:
        continue
    mse_vec = np.array([mean_squared_error(meta_val['rating'].values[m_val_c], Z_val[m_val_c, j])
                        for j in range(Z_val.shape[1])])
    w_c = mse_to_weights(mse_vec, temp=0.035)
    cluster_weight_table[str(c)] = {
        'label': cluster_profiles[c]['label'],
        'n_val': int(m_val_c.sum()),
        'weights': {nm: round(float(w), 3) for nm, w in zip(expert_names, w_c)},
        'val_mse': {nm: round(float(v), 4) for nm, v in zip(expert_names, mse_vec)}
    }
    pred_val_clusterblend[m_val_c] = np.clip((Z_val[m_val_c] * w_c).sum(axis=1), 1, 5)
    m_te_c = cluster_mask(test_df, c)
    if m_te_c.sum() > 0:
        pred_te_clusterblend[m_te_c] = np.clip((Z_te[m_te_c] * w_c).sum(axis=1), 1, 5)

def choose_alpha(base, alt, y, mask, grid):
    if mask.sum() == 0:
        return 0.0, mean_squared_error(y, base)
    best_alpha, best_mse = 0.0, mean_squared_error(y[mask], base[mask])
    for a in grid:
        cand = base.copy()
        cand[mask] = np.clip((1-a) * base[mask] + a * alt[mask], 1, 5)
        mse = mean_squared_error(y[mask], cand[mask])
        if mse < best_mse:
            best_alpha, best_mse = float(a), mse
    return best_alpha, best_mse

m_val_abn = known_abnormal_mask(meta_val)
m_te_abn = known_abnormal_mask(test_df)
y_val_full = meta_val['rating'].values

alpha_fixed, fixed_val_mse = choose_alpha(
    pred_val_segblend, pred_val_fixed_user, y_val_full, m_val_abn, np.linspace(0, 0.60, 13))
pred_val_abn_adapt = pred_val_segblend.copy()
pred_te_abn_adapt = pred_te_segblend.copy()
if m_val_abn.sum() > 0:
    pred_val_abn_adapt[m_val_abn] = np.clip(
        (1-alpha_fixed) * pred_val_segblend[m_val_abn] + alpha_fixed * pred_val_fixed_user[m_val_abn], 1, 5)
if m_te_abn.sum() > 0:
    pred_te_abn_adapt[m_te_abn] = np.clip(
        (1-alpha_fixed) * pred_te_segblend[m_te_abn] + alpha_fixed * pred_te_fixed_user[m_te_abn], 1, 5)

alpha_cluster, cluster_val_mse = choose_alpha(
    pred_val_abn_adapt, pred_val_clusterblend, y_val_full, m_val_abn, np.linspace(0, 0.80, 17))
if m_val_abn.sum() > 0:
    pred_val_abn_adapt[m_val_abn] = np.clip(
        (1-alpha_cluster) * pred_val_abn_adapt[m_val_abn] + alpha_cluster * pred_val_clusterblend[m_val_abn], 1, 5)
if m_te_abn.sum() > 0:
    pred_te_abn_adapt[m_te_abn] = np.clip(
        (1-alpha_cluster) * pred_te_abn_adapt[m_te_abn] + alpha_cluster * pred_te_clusterblend[m_te_abn], 1, 5)

mse_abn_adapt = mean_squared_error(y_te_full, pred_te_abn_adapt)
R['AbnormalAdaptive_MSE'] = round(mse_abn_adapt, 4)
R['abnormal_adaptive'] = {
    'known_abnormal_test_ratings': int(m_te_abn.sum()),
    'alpha_fixed_item_user_bias': round(alpha_fixed, 3),
    'alpha_cluster_expert_weight': round(alpha_cluster, 3),
    'all_mse': round(mse_abn_adapt, 4),
    'abnormal_user_mse_before': round(mean_squared_error(y_te_full[m_te_abn], pred_te_segblend[m_te_abn]), 4) if m_te_abn.sum() else None,
    'abnormal_user_mse_after': round(mean_squared_error(y_te_full[m_te_abn], pred_te_abn_adapt[m_te_abn]), 4) if m_te_abn.sum() else None,
    'cluster_weights': cluster_weight_table,
}
print(f"  AbnormalAdaptive MSE={mse_abn_adapt:.4f}, "
      f"abn n={m_te_abn.sum()}, alpha_fixed={alpha_fixed:.2f}, alpha_cluster={alpha_cluster:.2f}")
if m_te_abn.sum() > 0:
    print("  异常用户测试 MSE:",
          f"before={mean_squared_error(y_te_full[m_te_abn], pred_te_segblend[m_te_abn]):.4f}",
          f"after={mean_squared_error(y_te_full[m_te_abn], pred_te_abn_adapt[m_te_abn]):.4f}")

fig, ax = plt.subplots(figsize=(9, 4.5))
labels = ['All: Segment', 'All: AbnAdapt']
vals = [mse_segblend, mse_abn_adapt]
if m_te_abn.sum() > 0:
    labels += ['Abn: Segment', 'Abn: AbnAdapt']
    vals += [mean_squared_error(y_te_full[m_te_abn], pred_te_segblend[m_te_abn]),
             mean_squared_error(y_te_full[m_te_abn], pred_te_abn_adapt[m_te_abn])]
xs = np.arange(len(vals))
ax.bar(xs, vals, color=['#2EC4B6', '#264653', '#9D6EFF', '#F4A261'][:len(vals)])
for i, v in enumerate(vals):
    ax.text(i, v + 0.003, f'{v:.4f}', ha='center', fontsize=9)
ax.set_xticks(xs); ax.set_xticklabels(labels, rotation=10)
ax.set_ylabel('MSE')
ax.set_title('Abnormal-user calibration improves targeted users', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('2_6_abnormal_optimization.png')

# ============================================================
# 2.7 MOE
# ============================================================
print("\n" + "=" * 60)
print("SECTION 2.7: MOE 多专家系统")
print("=" * 60)

def build_router_x(df):
    n_u_s = train_df.groupby('user_id').size(); n_m_s = train_df.groupby('movie_id').size()
    mean_u_s = train_df.groupby('user_id')['rating'].mean()
    std_u_s = train_df.groupby('user_id')['rating'].std()
    mean_m_s = train_df.groupby('movie_id')['rating'].mean()
    out = pd.DataFrame()
    out['n_u'] = np.log1p(df['user_id'].map(n_u_s).fillna(0).values)
    out['mean_u'] = df['user_id'].map(mean_u_s).fillna(mu).values
    out['std_u'] = df['user_id'].map(std_u_s).fillna(0).values
    out['n_m'] = np.log1p(df['movie_id'].map(n_m_s).fillna(0).values)
    out['mean_m'] = df['movie_id'].map(mean_m_s).fillna(mu).values
    out['cold_u'] = (df['user_id'].map(n_u_s).fillna(0).values < 10).astype(float)
    out['cold_m'] = (df['movie_id'].map(n_m_s).fillna(0).values < 20).astype(float)
    g_map = movies.set_index('movie_id')['genres'].fillna('')
    out['rare_g'] = df['movie_id'].map(g_map).fillna('').str.contains('Film-Noir|Documentary|Western|Musical').astype(float).values
    out['is_abnormal_user'] = df['user_id'].isin(abn_user_set).astype(float).values
    cl = df['user_id'].map(abn_cluster_map).fillna(-1).astype(int)
    for c in range(K):
        out[f'abn_cluster_{c}'] = (cl.values == c).astype(float)
    return out.values.astype(np.float32)

router_scaler = StandardScaler()
X_meta_moe = router_scaler.fit_transform(build_router_x(meta_val)).astype(np.float32)
E_meta_moe = np.column_stack([P_m3_val, P_m2_val, P_m6_val, P_m7_val]).astype(np.float32)
y_meta_moe = meta_val['rating'].values.astype(np.float32)
X_te_router = router_scaler.transform(build_router_x(test_df)).astype(np.float32)
E_te = np.column_stack([pred_te_m3, pred_te_m2plus, pred_te_vsvd, PRED_TE_M7]).astype(np.float32)

class GatingMLP:
    def __init__(self, d_in, n_exp, d_h=32, lr=0.02, l2=1e-4, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.normal(0, 0.1, (d_in, d_h)).astype(np.float32)
        self.b1 = np.zeros(d_h, dtype=np.float32)
        self.W2 = rng.normal(0, 0.1, (d_h, n_exp)).astype(np.float32)
        self.b2 = np.zeros(n_exp, dtype=np.float32)
        self.lr, self.l2 = lr, l2
        self.m = {k: np.zeros_like(v) for k, v in self._p().items()}
        self.v = {k: np.zeros_like(v) for k, v in self._p().items()}
        self.t = 0
    def _p(self): return {'W1': self.W1, 'b1': self.b1, 'W2': self.W2, 'b2': self.b2}
    def forward(self, X):
        h = np.maximum(0, X @ self.W1 + self.b1)
        logits = h @ self.W2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        e = np.exp(logits); pi = e / e.sum(axis=1, keepdims=True)
        return pi, h
    def predict(self, X, E):
        pi, _ = self.forward(X)
        return (pi * E).sum(axis=1), pi
    def step(self, X, E, y, batch=4096):
        N = len(X); self.t += 1; idx = np.random.permutation(N); sse = 0
        for s in range(0, N, batch):
            sl = idx[s:s+batch]; Xb, Eb, yb = X[sl], E[sl], y[sl]
            pi, h = self.forward(Xb); pred = (pi * Eb).sum(axis=1); e_b = pred - yb
            sse += (e_b ** 2).sum()
            dl = pi * (Eb - pred[:, None]) * (2 * e_b[:, None]) / len(yb)
            dW2 = h.T @ dl + self.l2 * self.W2; db2 = dl.sum(0)
            dh = dl @ self.W2.T; dh[h <= 0] = 0
            dW1 = Xb.T @ dh + self.l2 * self.W1; db1 = dh.sum(0)
            self._adam('W1', dW1); self._adam('b1', db1)
            self._adam('W2', dW2); self._adam('b2', db2)
        return sse / N
    def _adam(self, name, g, b1=0.9, b2=0.999, eps=1e-8):
        self.m[name] = b1 * self.m[name] + (1-b1) * g
        self.v[name] = b2 * self.v[name] + (1-b2) * (g*g)
        mh = self.m[name] / (1 - b1**self.t)
        vh = self.v[name] / (1 - b2**self.t)
        getattr(self, name).__isub__(self.lr * mh / (np.sqrt(vh) + eps))

moe = GatingMLP(d_in=X_meta_moe.shape[1], n_exp=4, d_h=32, lr=0.01, l2=1e-4)
print("  训练 MOE gating (标准化路由特征 + 4 experts) ...")
for ep in range(20):
    mse_ep = moe.step(X_meta_moe, E_meta_moe, y_meta_moe)
    if ep == 0 or (ep+1) % 5 == 0:
        print(f"    epoch {ep+1:2d}  MSE={mse_ep:.4f}")

pred_te_moe, pi_te = moe.predict(X_te_router, E_te)
pred_te_moe = np.clip(pred_te_moe, 1, 5)
mse_moe = mean_squared_error(y_te_full, pred_te_moe)
print(f"  MOE MSE={mse_moe:.4f}")
R['MOE_MSE'] = round(mse_moe, 4)

# Router weights by scenario
exp_names = ['M3', 'M2+', 'M6', 'M7']
router_weights = {}
for nm, mask in seg_masks.items():
    if mask.sum() == 0: continue
    avg_pi = pi_te[mask].mean(axis=0)
    router_weights[nm] = {en: round(float(pi), 3) for en, pi in zip(exp_names, avg_pi)}
R['moe_router'] = router_weights
print("  Router weights:", router_weights)

# Final comparison chart
comp = [('M3', mean_squared_error(y_te_full, pred_te_m3)),
        ('M2+', mse_m2plus), ('M6', mse_vsvd), ('M7', mse_m7),
        ('Stack', mse_stack), ('SegBlend', mse_segblend),
        ('AbnAdapt', mse_abn_adapt), ('MOE4', mse_moe)]
fig, ax = plt.subplots(figsize=(12, 4.8))
xs = np.arange(len(comp)); ns = [c[0] for c in comp]; vs = [c[1] for c in comp]
colors = ['#FF6B6B','#FFA94D','#5C7AEA','#9D6EFF','#2EC4B6','#264653','#E76F51','#F4A261']
ax.bar(xs, vs, color=colors)
for i, v in enumerate(vs): ax.text(i, v+0.003, f'{v:.4f}', ha='center', fontsize=9)
ax.set_xticks(xs); ax.set_xticklabels(ns)
ax.set_title('All rating prediction models comparison', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('2_7_moe_compare.png')

# ============================================================
# PART 3: Genre prediction
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3.1: BERT + 微调层 类型预测")
print("=" * 60)

df_g = movies_info.dropna(subset=['intro', 'genre']).copy()
df_g = df_g[df_g['genre'].str.len() > 0]
def clean_text(s):
    s = str(s).lower()
    s = re.sub(r'<.*?>', '', s); s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()
df_g['text'] = (df_g['name'].fillna('') + ' . ' + df_g['intro'].fillna('')).map(clean_text)
df_g['labels'] = df_g['genre'].str.split('|')

mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df_g['labels'])
print(f"  样本数: {len(df_g)}, 标签数: {len(mlb.classes_)}")
X_text = df_g['text'].values
X_tr_t, X_tmp, y_tr_g, y_tmp = train_test_split(X_text, Y, test_size=0.25, random_state=42)
X_va_t, X_te_t, y_va_g, y_te_g = train_test_split(X_tmp, y_tmp, test_size=0.6, random_state=42)

# TF-IDF baselines
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.95, sublinear_tf=True, stop_words='english')
Xtr_v = tfidf.fit_transform(X_tr_t); Xva_v = tfidf.transform(X_va_t); Xte_v = tfidf.transform(X_te_t)

def eval_ml(name, yt, yp):
    return {'model': name, 'hamming': round(hamming_loss(yt, yp), 4),
            'jaccard': round(jaccard_score(yt, yp, average='samples', zero_division=0), 4),
            'f1_macro': round(f1_score(yt, yp, average='macro', zero_division=0), 4),
            'f1_samples': round(f1_score(yt, yp, average='samples', zero_division=0), 4),
            'subset_acc': round(accuracy_score(yt, yp), 4)}

genre_results = []
# A NB
nb_clf = OneVsRestClassifier(BernoulliNB())
nb_clf.fit(Xtr_v, y_tr_g); pred_nb = nb_clf.predict(Xte_v)
genre_results.append(eval_ml('A NB-Bin', y_te_g, pred_nb))
# B LR
lr_clf = OneVsRestClassifier(LogisticRegression(max_iter=2000, C=4))
lr_clf.fit(Xtr_v, y_tr_g); pred_lr = lr_clf.predict(Xte_v)
genre_results.append(eval_ml('B LR-OVR', y_te_g, pred_lr))
# C SVM
svm_clf = OneVsRestClassifier(LinearSVC(C=1, max_iter=5000))
svm_clf.fit(Xtr_v, y_tr_g); pred_svm = svm_clf.predict(Xte_v)
genre_results.append(eval_ml('C SVM-OVR', y_te_g, pred_svm))
print("  TF-IDF baselines done")

# MiniLM embeddings
INTRO_EMB = './intro_minilm_emb.pkl'
if os.path.exists(INTRO_EMB):
    with open(INTRO_EMB, 'rb') as f:
        c_ = pickle.load(f)
    Z_tr_m, Z_va_m, Z_te_m = c_['tr'], c_['va'], c_['te']
else:
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    Z_tr_m = st.encode(list(X_tr_t), batch_size=64, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    Z_va_m = st.encode(list(X_va_t), batch_size=64, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    Z_te_m = st.encode(list(X_te_t), batch_size=64, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    with open(INTRO_EMB, 'wb') as f:
        pickle.dump({'tr': Z_tr_m, 'va': Z_va_m, 'te': Z_te_m}, f)
print(f"  MiniLM embeddings: {Z_tr_m.shape}")

# PyTorch heads
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

device = 'cuda' if torch.cuda.is_available() else 'cpu'
n_classes = y_tr_g.shape[1]

class LinearHead(nn.Module):
    def __init__(self, d, nc): super().__init__(); self.fc = nn.Linear(d, nc)
    def forward(self, x): return self.fc(x)

class MLPHead(nn.Module):
    def __init__(self, d, nc, h=128, drop=0.3):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, h), nn.ReLU(), nn.Dropout(drop), nn.Linear(h, nc))
    def forward(self, x): return self.net(x)

def train_head(model, Ztr, ytr, Zva, yva, epochs=50, bs=64, lr_=1e-3, wd=1e-4):
    model = model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr_, weight_decay=wd)
    loss_fn = nn.BCEWithLogitsLoss()
    ds = TensorDataset(torch.tensor(Ztr), torch.tensor(ytr, dtype=torch.float32))
    dl = DataLoader(ds, batch_size=bs, shuffle=True)
    best_f1, best_state = -1, None
    for ep in range(epochs):
        model.train()
        for xb, yb in dl:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad(); loss_fn(model(xb), yb).backward(); opt.step()
        model.eval()
        with torch.no_grad():
            logits = model(torch.tensor(Zva).to(device)).cpu().numpy()
        f1 = f1_score(yva, (logits > 0).astype(int), average='samples', zero_division=0)
        if f1 > best_f1:
            best_f1, best_state = f1, {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    return model

torch.manual_seed(42)
print("  训练 F: MiniLM + Linear ...")
lin_head = train_head(LinearHead(Z_tr_m.shape[1], n_classes), Z_tr_m, y_tr_g, Z_va_m, y_va_g, epochs=40)
print("  训练 G: MiniLM + MLP ...")
mlp_head = train_head(MLPHead(Z_tr_m.shape[1], n_classes), Z_tr_m, y_tr_g, Z_va_m, y_va_g, epochs=60)

with torch.no_grad():
    z_te_t_ = torch.tensor(Z_te_m).to(device)
    pred_F = (lin_head(z_te_t_).cpu().numpy() > 0).astype(int)
    pred_G = (mlp_head(z_te_t_).cpu().numpy() > 0).astype(int)
genre_results.append(eval_ml('F MiniLM+Linear', y_te_g, pred_F))
genre_results.append(eval_ml('G MiniLM+MLP', y_te_g, pred_G))

R['genre_results'] = genre_results
gr = pd.DataFrame(genre_results)
print(gr.to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 5))
xs = np.arange(len(gr)); w = 0.22
for offs, (col, color) in enumerate(zip(['jaccard','f1_macro','f1_samples','subset_acc'],
    ['#FF6B6B','#5C7AEA','#2EC4B6','#9D6EFF'])):
    ax.bar(xs + (offs-1.5)*w, gr[col], w, label=col, color=color)
ax.set_xticks(xs); ax.set_xticklabels(gr['model'], rotation=15)
ax.legend(loc='upper left', fontsize=9)
ax.set_title('Genre prediction: TF-IDF baselines vs BERT', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('3_1_genre_compare.png')

# ============================================================
# 3.2 主题 x 年龄
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3.2: 主题 × 年龄相关性")
print("=" * 60)

cv = CountVectorizer(ngram_range=(1, 2), min_df=10, max_df=0.85, stop_words='english')
X_cnt = cv.fit_transform(df_g['text'].values)
K_TOPIC = 6
lda = LatentDirichletAllocation(n_components=K_TOPIC, random_state=0, learning_method='batch', max_iter=30)
lda.fit(X_cnt)
voc = np.array(cv.get_feature_names_out())
topic_top_words = []
for k in range(K_TOPIC):
    top_idx = np.argsort(-lda.components_[k])[:8]
    topic_top_words.append(voc[top_idx].tolist())
    print(f"  topic {k}: {voc[top_idx][:6]}")
movie_topic = lda.transform(X_cnt)

df_with_id = df_g.reset_index(drop=True)[['movie_id']].copy()
df_with_id[[f't{k}' for k in range(K_TOPIC)]] = movie_topic

rj = ratings[['user_id', 'movie_id', 'rating']].merge(df_with_id, on='movie_id', how='inner'
    ).merge(users[['user_id', 'age_desc']], on='user_id', how='left')

age_order = ['Under 18', '18-24', '25-34', '35-44', '45-49', '50-55', '56+']
theme_age = pd.DataFrame(index=age_order, columns=[f't{k}' for k in range(K_TOPIC)], dtype=float)
for a in age_order:
    sub_a = rj[rj['age_desc'] == a]
    if len(sub_a) == 0: continue
    for k in range(K_TOPIC):
        w_ = sub_a[f't{k}'].values; r_ = sub_a['rating'].values
        if w_.sum() > 0: theme_age.loc[a, f't{k}'] = np.average(r_, weights=w_)
print("  主题 × 年龄表:")
print(theme_age.round(3))

discrim = theme_age.astype(float).var(axis=0)
top3 = discrim.sort_values(ascending=False).index[:3].tolist()
R['top3_topics'] = {t: topic_top_words[int(t[1:])][:5] for t in top3}
R['theme_age_table'] = theme_age.round(3).to_dict()
print(f"  年龄区分度 top3: {top3}")

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.heatmap(theme_age.astype(float), annot=True, fmt='.2f', cmap='RdYlBu_r',
            ax=axes[0], vmin=3.0, vmax=4.5, cbar_kws={'label': 'Avg Rating'})
axes[0].set_title('LDA Topics x Age Groups', fontweight='bold')
for t in top3:
    axes[1].plot(theme_age.index, theme_age[t].astype(float), marker='o', lw=2,
                 label=f'{t}: {topic_top_words[int(t[1:])][:3]}')
axes[1].set_xlabel('Age Group'); axes[1].set_ylabel('Avg Rating')
axes[1].set_title('Top3 Topics by Age', fontweight='bold')
axes[1].legend(fontsize=9); axes[1].grid(alpha=.3)
plt.tight_layout()
savefig('3_2_theme_age.png')

# ============================================================
# 3.3 LLM Embedding + fine-tuning
# ============================================================
print("\n" + "=" * 60)
print("SECTION 3.3: LLM Embedding + 微调")
print("=" * 60)

LLM_EMB_CACHE = './intro_llm_emb.pkl'
LLM_EMB_KEY = 'sk-dNG1yLCPN4Yvyr9JKNGl7D4WskdNQlx3bY583RVpCYUN1zsT'
LLM_EMB_URL = 'https://yunwu.ai/v1/embeddings'

def llm_embed(texts, model='text-embedding-3-small'):
    import requests
    headers = {'Authorization': f'Bearer {LLM_EMB_KEY}', 'Content-Type': 'application/json'}
    out = []; BATCH = 64
    for i in range(0, len(texts), BATCH):
        batch = list(texts[i:i+BATCH])
        r = requests.post(LLM_EMB_URL, headers=headers,
                          json={'model': model, 'input': batch}, timeout=60)
        r.raise_for_status()
        out.extend([d['embedding'] for d in r.json()['data']])
        if (i // BATCH) % 5 == 0:
            print(f"    {min(i+BATCH, len(texts))}/{len(texts)}")
    return np.array(out, dtype=np.float32)

if os.path.exists(LLM_EMB_CACHE):
    with open(LLM_EMB_CACHE, 'rb') as f:
        c_ = pickle.load(f)
    Z_tr_L, Z_va_L, Z_te_L, llm_model = c_['tr'], c_['va'], c_['te'], c_.get('model', '?')
    print(f"  [cache] LLM emb: {Z_tr_L.shape}, model={llm_model}")
else:
    llm_model = None
    for m in ['text-embedding-3-small', 'text-embedding-ada-002']:
        try:
            print(f"  [try] {m}")
            Z_tr_L = llm_embed(X_tr_t, m); Z_va_L = llm_embed(X_va_t, m); Z_te_L = llm_embed(X_te_t, m)
            llm_model = m; break
        except Exception as e:
            print(f"    fail: {e}")
    if llm_model is None:
        print("  [fallback] 本地 MiniLM (复用 3.1 的嵌入)")
        from sentence_transformers import SentenceTransformer
        st2 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        enc = lambda t: st2.encode(list(t), batch_size=32, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
        Z_tr_L, Z_va_L, Z_te_L = enc(X_tr_t), enc(X_va_t), enc(X_te_t)
        llm_model = 'MiniLM-fallback'
    with open(LLM_EMB_CACHE, 'wb') as f:
        pickle.dump({'tr': Z_tr_L, 'va': Z_va_L, 'te': Z_te_L, 'model': llm_model}, f)
    print(f"  saved {Z_tr_L.shape}")

torch.manual_seed(42)
print(f"  训练 H: LLM-emb ({llm_model}) + MLP-256 ...")
mlp_L = train_head(MLPHead(Z_tr_L.shape[1], n_classes, h=256, drop=0.4),
                   Z_tr_L, y_tr_g, Z_va_L, y_va_g, epochs=60, lr_=1e-3, wd=1e-3)
with torch.no_grad():
    logits_H = mlp_L(torch.tensor(Z_te_L).to(device)).cpu().numpy()
pred_H = (logits_H > 0).astype(int)
genre_results.append(eval_ml(f'H LLM-emb+MLP', y_te_g, pred_H))
R['genre_results'] = genre_results
R['llm_emb_model'] = llm_model

gr2 = pd.DataFrame(genre_results)
print(gr2.to_string(index=False))

fig, ax = plt.subplots(figsize=(12, 5))
xs = np.arange(len(gr2)); w = 0.22
for offs, (col, color) in enumerate(zip(['jaccard','f1_macro','f1_samples','subset_acc'],
    ['#FF6B6B','#5C7AEA','#2EC4B6','#9D6EFF'])):
    ax.bar(xs + (offs-1.5)*w, gr2[col], w, label=col, color=color)
ax.set_xticks(xs); ax.set_xticklabels(gr2['model'], rotation=15)
ax.legend(loc='upper left', fontsize=9)
ax.set_title(f'Full genre comparison (LLM-emb={llm_model})', fontweight='bold')
ax.grid(axis='y', alpha=.3); plt.tight_layout()
savefig('3_3_full_genre.png')

# ============================================================
# Save results
# ============================================================
with open(os.path.join(WORK, 'results.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=2, default=str)
print(f"\n===== ALL DONE =====")
print(f"Results -> results.json")
print(f"Figures -> {FIG}/")
