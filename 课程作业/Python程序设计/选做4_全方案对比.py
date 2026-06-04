"""
选做4 全方案优化对比
====================

目标：在「电影类型多标签分类 + 关键词提取」任务上，
系统比较 多种关键词算法 × 多种分类模型 × 后处理策略，
找出最佳组合并量化提升。

A. 关键词提取算法（5 种）
   1) LR 权重         (baseline，原作业方案)
   2) TF-IDF 类内均值  (统计型 baseline)
   3) TextRank        (无监督图算法，networkx 实现)
   4) LDA 主题词       (sklearn LatentDirichletAllocation)
   5) YAKE            (无监督统计短语提取)
   ※ BERT/RAKE 未启用（环境无 transformers / nltk_data）

B. 分类模型（4 种）
   1) Logistic Regression OVR (baseline)
   2) MLP (sklearn MLPClassifier，TF-IDF 输入)
   3) TextCNN (PyTorch，词序列输入)
   4) BiLSTM  (PyTorch，词序列输入)

C. 后处理（2 种）
   1) 标签共现概率修正 P_cond
   2) 验证集上的自适应阈值 θ*_g = argmax F1

输出：每组关键词 Top-8、各模型测试集指标、最优组合 vs baseline。
"""

import os, sys, time, json, math, re, random, warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import (f1_score, jaccard_score, hamming_loss,
                             accuracy_score)

import networkx as nx
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

SEED = 42
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEVICE = torch.device('cpu')

# ---------- 0. 数据 ----------
DATA_DIR = '/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/data'
movies_info = pd.read_csv(os.path.join(DATA_DIR, 'info.csv'), encoding='latin-1',
                          usecols=['id', 'name', 'genre', 'intro'])
movies_info.rename(columns={'id': 'movie_id'}, inplace=True)

def clean_text(s):
    s = str(s).lower()
    s = re.sub(r'<.*?>', '', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

df = movies_info.dropna(subset=['intro', 'genre']).copy()
df = df[df['genre'].str.len() > 0]
df['text']   = (df['name'].fillna('') + ' . ' + df['intro'].fillna('')).map(clean_text)
df['labels'] = df['genre'].str.split('|')

mlb = MultiLabelBinarizer()
Y   = mlb.fit_transform(df['labels'])
GENRES = list(mlb.classes_)
print(f'[data] N={len(df)}  K={len(GENRES)}  avg-labels={Y.sum(1).mean():.2f}')
print(f'[data] genres={GENRES}')

X_text = df['text'].to_numpy(dtype=object)
X_tr, X_tmp, y_tr, y_tmp = train_test_split(X_text, Y, test_size=0.25, random_state=SEED)
X_va, X_te, y_va, y_te   = train_test_split(X_tmp, y_tmp, test_size=0.6, random_state=SEED)
print(f'[split] train={len(X_tr)}  val={len(X_va)}  test={len(X_te)}')

# 共用 TF-IDF (1-2gram)
tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.95,
                        sublinear_tf=True, stop_words='english')
Xtr_v = tfidf.fit_transform(X_tr); Xva_v = tfidf.transform(X_va); Xte_v = tfidf.transform(X_te)
feat_names = np.array(tfidf.get_feature_names_out())
print(f'[tfidf] vocab={Xtr_v.shape[1]}')

# ====================================================
# A. 关键词提取算法 ——————————————————————————
# ====================================================
TOP_N = 8

def kw_lr_weights():
    """方案1: LR 权重 (原作业 baseline)"""
    lr = OneVsRestClassifier(LogisticRegression(max_iter=2000, C=4))
    lr.fit(Xtr_v, y_tr)
    out = {}
    for j, g in enumerate(GENRES):
        coef = lr.estimators_[j].coef_.ravel()
        idx = np.argsort(coef)[-TOP_N:][::-1]
        out[g] = feat_names[idx].tolist()
    return out, lr  # 顺便返回模型供后续

def kw_tfidf_mean():
    """方案2: 类内 TF-IDF 平均值"""
    Xa = Xtr_v.toarray()  # 训练样本数小，可承受
    out = {}
    for j, g in enumerate(GENRES):
        mask = y_tr[:, j] == 1
        if mask.sum() == 0:
            out[g] = []; continue
        mean_score = Xa[mask].mean(0) - Xa[~mask].mean(0)  # 区分度
        idx = np.argsort(mean_score)[-TOP_N:][::-1]
        out[g] = feat_names[idx].tolist()
    return out

def kw_textrank_per_genre():
    """方案3: TextRank。每个类型的所有剧情拼成图再排序"""
    cv = CountVectorizer(min_df=3, stop_words='english',
                         token_pattern=r'(?u)\b[a-z]{3,}\b')
    out = {}
    for j, g in enumerate(GENRES):
        docs = X_tr[y_tr[:, j] == 1]
        if len(docs) == 0:
            out[g] = []; continue
        # 共现窗 = 句内 5 词
        WIN = 5
        co = {}; vocab = {}
        for d in docs:
            toks = re.findall(r'\b[a-z]{3,}\b', d)
            toks = [t for t in toks if t not in cv.get_stop_words()]
            for i, w in enumerate(toks):
                vocab.setdefault(w, len(vocab))
                for k in range(i+1, min(i+WIN, len(toks))):
                    a, b = w, toks[k]
                    if a == b: continue
                    key = (min(a, b), max(a, b))
                    co[key] = co.get(key, 0) + 1
        if not co:
            out[g] = []; continue
        G = nx.Graph()
        for (a, b), w in co.items():
            G.add_edge(a, b, weight=w)
        try:
            pr = nx.pagerank(G, alpha=0.85, max_iter=50, tol=1e-4)
        except nx.PowerIterationFailedConvergence:
            pr = {n: 1.0/len(G) for n in G.nodes}
        ranked = sorted(pr.items(), key=lambda x: -x[1])[:TOP_N]
        out[g] = [w for w, _ in ranked]
    return out

def kw_lda():
    """方案4: LDA 主题词（n_topics=#genres，再用类内文档投票把主题对到类型）"""
    cv = CountVectorizer(min_df=5, max_df=0.95, stop_words='english',
                         token_pattern=r'(?u)\b[a-z]{3,}\b')
    Xc_tr = cv.fit_transform(X_tr); names = np.array(cv.get_feature_names_out())
    K = len(GENRES)
    lda = LatentDirichletAllocation(n_components=K, random_state=SEED,
                                    max_iter=20, learning_method='batch')
    doc_topic = lda.fit_transform(Xc_tr)              # (N, K)
    topic_word = lda.components_                      # (K, V)
    # 投票：每个 genre 的样本归属哪个主题最多 → 该主题就是该 genre 的代表
    g2t = {}
    for j in range(K):
        mask = y_tr[:, j] == 1
        if mask.sum() == 0: g2t[GENRES[j]] = j; continue
        # 选 mean-topic 概率最大的主题
        # 但要避免冲突：贪心匹配
        g2t[GENRES[j]] = int(doc_topic[mask].mean(0).argmax())
    # 简单冲突解决：若多 genre 命中同主题，给 genre 频次靠前者保留，其余降到次优
    used = set(); final = {}
    order = sorted(range(K), key=lambda j: -y_tr[:, j].sum())
    for j in order:
        m = y_tr[:, j] == 1
        if m.sum() == 0: final[GENRES[j]] = -1; continue
        ranked_t = doc_topic[m].mean(0).argsort()[::-1]
        chosen = next((int(t) for t in ranked_t if t not in used), int(ranked_t[0]))
        used.add(chosen); final[GENRES[j]] = chosen
    out = {}
    for g, t in final.items():
        if t < 0: out[g] = []; continue
        idx = topic_word[t].argsort()[-TOP_N:][::-1]
        out[g] = names[idx].tolist()
    return out

def kw_yake():
    """方案5: YAKE 短语级关键词（仅 unigram + bigram）"""
    import yake
    extractor = yake.KeywordExtractor(lan='en', n=2, top=TOP_N*2)
    out = {}
    for j, g in enumerate(GENRES):
        docs = X_tr[y_tr[:, j] == 1]
        if len(docs) == 0:
            out[g] = []; continue
        merged = ' . '.join(docs[:200])  # 截断，避免太慢
        try:
            kws = extractor.extract_keywords(merged)
        except Exception:
            kws = []
        # YAKE: 分越低越关键
        kws_sorted = sorted(kws, key=lambda x: x[1])
        seen = set(); picked = []
        for w, _ in kws_sorted:
            w = w.lower().strip()
            if w in seen: continue
            seen.add(w); picked.append(w)
            if len(picked) >= TOP_N: break
        out[g] = picked
    return out

print('\n=========== A. 关键词提取算法对比 ===========')
t0 = time.time(); kw1, lr_model = kw_lr_weights();    print(f'[kw1 LR-weight]  {time.time()-t0:.1f}s')
t0 = time.time(); kw2 = kw_tfidf_mean();              print(f'[kw2 TFIDF-mean] {time.time()-t0:.1f}s')
t0 = time.time(); kw3 = kw_textrank_per_genre();      print(f'[kw3 TextRank]   {time.time()-t0:.1f}s')
t0 = time.time(); kw4 = kw_lda();                     print(f'[kw4 LDA]        {time.time()-t0:.1f}s')
t0 = time.time(); kw5 = kw_yake();                    print(f'[kw5 YAKE]       {time.time()-t0:.1f}s')

# 对比表：每个 genre 一行 × 五种方案
print('\n[关键词对比 · 每 genre 取 Top-5 节选]')
for g in GENRES:
    print(f'\n>> {g}')
    print(f'   LR-weight  : {kw1[g][:5]}')
    print(f'   TFIDF-mean : {kw2[g][:5]}')
    print(f'   TextRank   : {kw3[g][:5]}')
    print(f'   LDA        : {kw4[g][:5]}')
    print(f'   YAKE       : {kw5[g][:5]}')

# ====================================================
# B. 多模型分类对比 ——————————————————————————
# ====================================================

def evaluate(name, y_true, y_pred):
    return dict(
        model=name,
        hamming   = round(hamming_loss(y_true, y_pred), 4),
        jaccard   = round(jaccard_score(y_true, y_pred, average='samples', zero_division=0), 4),
        f1_macro  = round(f1_score(y_true, y_pred, average='macro',   zero_division=0), 4),
        f1_micro  = round(f1_score(y_true, y_pred, average='micro',   zero_division=0), 4),
        f1_samples= round(f1_score(y_true, y_pred, average='samples', zero_division=0), 4),
        subset_acc= round(accuracy_score(y_true, y_pred), 4),
    )

results = []

# ---- B1: LR baseline (already trained as lr_model) ----
pred_lr = lr_model.predict(Xte_v)
proba_lr_va = lr_model.predict_proba(Xva_v)
proba_lr_te = lr_model.predict_proba(Xte_v)
results.append(evaluate('LR (baseline)', y_te, pred_lr))

# ---- B2: MLP on TF-IDF ----
print('\n[B2] MLPClassifier (sklearn) ...')
mlp = MLPClassifier(hidden_layer_sizes=(256, 128), early_stopping=True,
                    max_iter=60, random_state=SEED, batch_size=128)
# OvR 方式：直接用多输出（sklearn MLP 支持 multilabel-indicator）
mlp.fit(Xtr_v.astype(np.float32), y_tr)
proba_mlp_va = mlp.predict_proba(Xva_v.astype(np.float32))
proba_mlp_te = mlp.predict_proba(Xte_v.astype(np.float32))
pred_mlp = (proba_mlp_te > 0.5).astype(int)
# 防止全 0
for i in range(len(pred_mlp)):
    if pred_mlp[i].sum() == 0: pred_mlp[i, proba_mlp_te[i].argmax()] = 1
results.append(evaluate('MLP (TFIDF)', y_te, pred_mlp))

# ---- B3 / B4: 准备词序列 (PyTorch) ----
print('\n[B3/B4] 准备词序列输入 ...')
MAX_VOCAB = 8000
MAX_LEN   = 120

def tokenize(s):
    return re.findall(r'\b[a-z]{2,}\b', s)

# 词频统计
from collections import Counter
ctr = Counter()
for s in X_tr: ctr.update(tokenize(s))
itos = ['<pad>', '<unk>'] + [w for w, _ in ctr.most_common(MAX_VOCAB - 2)]
stoi = {w: i for i, w in enumerate(itos)}
PAD, UNK = 0, 1

def encode(s):
    toks = tokenize(s)[:MAX_LEN]
    ids  = [stoi.get(t, UNK) for t in toks]
    if len(ids) < MAX_LEN: ids += [PAD] * (MAX_LEN - len(ids))
    return ids

Xtr_seq = torch.tensor([encode(s) for s in X_tr], dtype=torch.long)
Xva_seq = torch.tensor([encode(s) for s in X_va], dtype=torch.long)
Xte_seq = torch.tensor([encode(s) for s in X_te], dtype=torch.long)
ytr_t = torch.tensor(y_tr, dtype=torch.float32)
yva_t = torch.tensor(y_va, dtype=torch.float32)
yte_t = torch.tensor(y_te, dtype=torch.float32)

class SeqDS(Dataset):
    def __init__(self, X, Y): self.X, self.Y = X, Y
    def __len__(self): return len(self.X)
    def __getitem__(self, i): return self.X[i], self.Y[i]

train_dl = DataLoader(SeqDS(Xtr_seq, ytr_t), batch_size=64, shuffle=True)
val_dl   = DataLoader(SeqDS(Xva_seq, yva_t), batch_size=128)
test_dl  = DataLoader(SeqDS(Xte_seq, yte_t), batch_size=128)

K_GENRE = len(GENRES); EMB = 100

def predict_proba_torch(model, dl):
    model.eval(); ps = []
    with torch.no_grad():
        for x, _ in dl:
            ps.append(torch.sigmoid(model(x)).cpu().numpy())
    return np.vstack(ps)

def train_torch(model, epochs=8, lr=1e-3, name='model'):
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    bce = nn.BCEWithLogitsLoss()
    best_f1 = -1; best_state = None
    for ep in range(epochs):
        model.train(); losses = []
        for x, y in train_dl:
            opt.zero_grad()
            logit = model(x)
            l = bce(logit, y)
            l.backward(); opt.step()
            losses.append(l.item())
        # 验证
        pv = predict_proba_torch(model, val_dl)
        pred_v = (pv > 0.5).astype(int)
        for i in range(len(pred_v)):
            if pred_v[i].sum() == 0: pred_v[i, pv[i].argmax()] = 1
        f1 = f1_score(y_va, pred_v, average='samples', zero_division=0)
        print(f'   {name} ep{ep+1}/{epochs}  loss={np.mean(losses):.4f}  val_f1_samples={f1:.4f}')
        if f1 > best_f1:
            best_f1 = f1
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)
    return model

# ----- TextCNN -----
class TextCNN(nn.Module):
    def __init__(self, V, E, K, kernels=(3, 4, 5), nf=64, drop=0.4):
        super().__init__()
        self.emb = nn.Embedding(V, E, padding_idx=0)
        self.convs = nn.ModuleList([nn.Conv1d(E, nf, k) for k in kernels])
        self.drop = nn.Dropout(drop)
        self.fc = nn.Linear(nf*len(kernels), K)
    def forward(self, x):
        e = self.emb(x).transpose(1, 2)            # (B, E, L)
        feats = [F.relu(c(e)).max(-1).values for c in self.convs]
        h = torch.cat(feats, 1)
        return self.fc(self.drop(h))

# ----- BiLSTM -----
class BiLSTM(nn.Module):
    def __init__(self, V, E, K, hid=128, drop=0.4):
        super().__init__()
        self.emb = nn.Embedding(V, E, padding_idx=0)
        self.lstm = nn.LSTM(E, hid, batch_first=True, bidirectional=True)
        self.drop = nn.Dropout(drop)
        self.fc = nn.Linear(hid*2, K)
    def forward(self, x):
        e = self.emb(x)
        o, _ = self.lstm(e)
        h = o.max(1).values   # max pooling over time
        return self.fc(self.drop(h))

print('\n[B3] TextCNN training ...')
cnn = TextCNN(len(itos), EMB, K_GENRE)
cnn = train_torch(cnn, epochs=8, name='TextCNN')
proba_cnn_va = predict_proba_torch(cnn, val_dl)
proba_cnn_te = predict_proba_torch(cnn, test_dl)
pred_cnn = (proba_cnn_te > 0.5).astype(int)
for i in range(len(pred_cnn)):
    if pred_cnn[i].sum() == 0: pred_cnn[i, proba_cnn_te[i].argmax()] = 1
results.append(evaluate('TextCNN', y_te, pred_cnn))

print('\n[B4] BiLSTM training ...')
lstm = BiLSTM(len(itos), EMB, K_GENRE)
lstm = train_torch(lstm, epochs=8, name='BiLSTM')
proba_lstm_va = predict_proba_torch(lstm, val_dl)
proba_lstm_te = predict_proba_torch(lstm, test_dl)
pred_lstm = (proba_lstm_te > 0.5).astype(int)
for i in range(len(pred_lstm)):
    if pred_lstm[i].sum() == 0: pred_lstm[i, proba_lstm_te[i].argmax()] = 1
results.append(evaluate('BiLSTM', y_te, pred_lstm))

# ====================================================
# C. 后处理 ——————————————————————————
# ====================================================

# 共现条件概率
co = (y_tr.T @ y_tr).astype(float)
diag = co.diagonal().clip(min=1)
P_cond = co / diag[:, None]            # P(j | i)

def co_occur_adjust(proba_te):
    adj = proba_te @ P_cond             # (N, K)
    pred = (adj > adj.mean(1, keepdims=True)).astype(int)
    for i in range(len(pred)):
        if pred[i].sum() == 0: pred[i, adj[i].argmax()] = 1
    return pred

def adaptive_threshold(proba_va, y_va_, proba_te):
    """每个 genre 在 val 上找最佳阈值。"""
    K = proba_va.shape[1]; thrs = np.zeros(K)
    for j in range(K):
        best, best_f1 = 0.5, -1
        for t in np.arange(0.10, 0.90, 0.02):
            pj = (proba_va[:, j] > t).astype(int)
            f = f1_score(y_va_[:, j], pj, zero_division=0)
            if f > best_f1: best, best_f1 = t, f
        thrs[j] = best
    pred = (proba_te > thrs).astype(int)
    for i in range(len(pred)):
        if pred[i].sum() == 0: pred[i, proba_te[i].argmax()] = 1
    return pred, thrs

# 找到 base 模型中 f1_samples 最高的，再叠加 C
proba_map_va = {'LR': proba_lr_va, 'MLP': proba_mlp_va, 'TextCNN': proba_cnn_va, 'BiLSTM': proba_lstm_va}
proba_map_te = {'LR': proba_lr_te, 'MLP': proba_mlp_te, 'TextCNN': proba_cnn_te, 'BiLSTM': proba_lstm_te}

base_scores = {r['model'].split()[0].rstrip(':').replace('(baseline)', '').strip(): r['f1_samples']
               for r in results}
print('\n=========== B. 各模型 baseline 评测 ===========')
print(pd.DataFrame(results).to_string(index=False))

best_base = max(['LR', 'MLP', 'TextCNN', 'BiLSTM'],
                key=lambda k: next(r['f1_samples'] for r in results if k in r['model']))
print(f'\n[best base model on f1_samples] => {best_base}')

# 对每个模型加共现 / 自适应阈值
print('\n=========== C. 后处理（对每个 base 模型）===========')
post_results = []
for k in ['LR', 'MLP', 'TextCNN', 'BiLSTM']:
    pv = proba_map_va[k]; pt = proba_map_te[k]
    pred_co = co_occur_adjust(pt)
    pred_th, _ = adaptive_threshold(pv, y_va, pt)
    # 组合：共现修正后再做阈值
    pt_co = pt @ P_cond
    pt_co = pt_co / pt_co.max(1, keepdims=True)  # 重新缩到 [0,1]
    pred_combo, _ = adaptive_threshold(pv @ P_cond / (pv @ P_cond).max(1, keepdims=True),
                                       y_va, pt_co)
    post_results.append(evaluate(f'{k} + Co-occur', y_te, pred_co))
    post_results.append(evaluate(f'{k} + AdaThr',   y_te, pred_th))
    post_results.append(evaluate(f'{k} + Co+AdaThr', y_te, pred_combo))

print(pd.DataFrame(post_results).to_string(index=False))

# ====================================================
# D. 汇总 & 选最优 ——————————————————————————
# ====================================================
all_results = results + post_results
df_all = pd.DataFrame(all_results).sort_values('f1_samples', ascending=False).reset_index(drop=True)
print('\n=========== D. 全方案排行（按 f1_samples 降序）===========')
print(df_all.to_string(index=False))

best = df_all.iloc[0]
base = next(r for r in results if r['model'] == 'LR (baseline)')
print(f'\n>>> 最优方案：{best["model"]}')
print(f'    f1_samples {base["f1_samples"]:.4f} → {best["f1_samples"]:.4f} '
      f'(+{(best["f1_samples"]-base["f1_samples"])*100:.2f} pp)')
print(f'    jaccard    {base["jaccard"]:.4f} → {best["jaccard"]:.4f} '
      f'(+{(best["jaccard"]-base["jaccard"])*100:.2f} pp)')
print(f'    hamming    {base["hamming"]:.4f} → {best["hamming"]:.4f} '
      f'({(best["hamming"]-base["hamming"])*100:+.2f} pp; 越低越好)')

# 保存结果到 csv，方便实验报告引用
out_dir = '/mnt/c/Users/32698/笔记与作业/code/python/考试/作业/python程设/期中大作业-蒋名仪-2500010771'
df_all.to_csv(os.path.join(out_dir, '选做4_全方案对比.csv'), index=False, encoding='utf-8-sig')

kw_table = pd.DataFrame({
    'genre': GENRES,
    'LR-weight' : [' / '.join(kw1[g][:6]) for g in GENRES],
    'TFIDF-mean': [' / '.join(kw2[g][:6]) for g in GENRES],
    'TextRank'  : [' / '.join(kw3[g][:6]) for g in GENRES],
    'LDA'       : [' / '.join(kw4[g][:6]) for g in GENRES],
    'YAKE'      : [' / '.join(kw5[g][:6]) for g in GENRES],
})
kw_table.to_csv(os.path.join(out_dir, '选做4_关键词对比.csv'), index=False, encoding='utf-8-sig')
print(f'\n[saved] 选做4_全方案对比.csv 与 选做4_关键词对比.csv 已写入 {out_dir}')
