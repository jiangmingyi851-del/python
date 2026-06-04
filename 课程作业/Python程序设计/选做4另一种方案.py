import os, sys, time, json, math, re, random, warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score, jaccard_score, hamming_loss, accuracy_score
from scipy.sparse import coo_matrix
import networkx as nx

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel, AdamW, get_linear_schedule_with_warmup

# ---------- 固定随机种子 ----------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {DEVICE}")

# ---------- 1. 数据加载（与你的代码一致）----------
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
K = len(GENRES)                     # 标签总数
print(f'[data] N={len(df)}  K={K}  avg-labels={Y.sum(1).mean():.2f}')
print(f'[data] genres={GENRES[:10]}...' if K>10 else f'[data] genres={GENRES}')

X_text = df['text'].to_numpy(dtype=object)
X_tr, X_tmp, y_tr, y_tmp = train_test_split(X_text, Y, test_size=0.25, random_state=SEED)
X_va, X_te, y_va, y_te   = train_test_split(X_tmp, y_tmp, test_size=0.6, random_state=SEED)
print(f'[split] train={len(X_tr)}  val={len(X_va)}  test={len(X_te)}')

# ---------- 2. 构建标签图（基于训练集共现）----------
def build_label_graph(y_train, top_k=10, pmi_threshold=0.0):
    """从训练集的标签共现构建邻接矩阵（稀疏，带自环）"""
    # 计算共现矩阵
    co_occur = y_train.T @ y_train            # K x K
    np.fill_diagonal(co_occur, 0)
    # 计算每个标签出现的次数
    freq = y_train.sum(axis=0)                # shape (K,)
    
    # 计算 PMI: log( p(i,j) / (p(i)*p(j)) )
    p_ij = co_occur / len(y_train)
    p_i = freq / len(y_train)
    # 避免除零
    p_i = np.maximum(p_i, 1e-12)
    pmi = np.log(p_ij / np.outer(p_i, p_i) + 1e-12)
    pmi = np.maximum(pmi, 0.0)               # 只保留正相关
    
    # 方式二：也可以直接用共现次数归一化（条件概率），这里选择PMI
    # 为了保持图不太密，只保留每个标签的top-k个最相关邻居
    adj = np.zeros((K, K))
    for i in range(K):
        top_idx = np.argsort(pmi[i])[-top_k:][::-1]
        for j in top_idx:
            if pmi[i, j] > pmi_threshold and i != j:
                adj[i, j] = pmi[i, j]
                adj[j, i] = pmi[i, j]       # 无向对称
    # 添加自环
    adj = adj + np.eye(K)
    # 归一化: A_hat = D^{-1/2} A D^{-1/2}
    D = np.diag(np.sum(adj, axis=1) ** (-0.5))
    D = np.nan_to_num(D)
    adj_normalized = D @ adj @ D
    return torch.FloatTensor(adj_normalized).to(DEVICE)

print("[build] constructing label graph from training set...")
adj_label = build_label_graph(y_tr, top_k=8, pmi_threshold=0.01)
print(f"[build] label adjacency matrix shape: {adj_label.shape}, non-zero: {(adj_label>0).sum().item()}")

# ---------- 3. PyTorch Dataset ----------
class MovieDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=256):
        self.texts = texts
        self.labels = torch.FloatTensor(labels)
        self.tokenizer = tokenizer
        self.max_len = max_len
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'labels': self.labels[idx]
        }

# ---------- 4. GCN 模块（两层）----------
class GCN(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, adj):
        super().__init__()
        self.adj = adj   # 预计算的归一化邻接矩阵
        self.fc1 = nn.Linear(in_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, out_dim)
    def forward(self, x):
        # x: (num_labels, in_dim)
        x = F.relu(torch.mm(self.adj, x))          # A_hat * x
        x = self.fc1(x)
        x = F.relu(torch.mm(self.adj, x))
        x = self.fc2(x)                            # (num_labels, out_dim)
        return x

# ---------- 5. 完整模型：BERT + GCN ----------
class BERT_GCN_MultiLabel(nn.Module):
    def __init__(self, num_labels, label_adj, bert_name='bert-base-uncased', 
                 label_emb_dim=128, gcn_hidden=256):
        super().__init__()
        self.bert = BertModel.from_pretrained(bert_name)
        bert_out_dim = self.bert.config.hidden_size   # 768
        # 初始标签嵌入（可学习）
        self.label_emb = nn.Parameter(torch.randn(num_labels, label_emb_dim))
        # GCN
        self.gcn = GCN(label_emb_dim, gcn_hidden, bert_out_dim, label_adj)
        # 分类偏置（可选）
        self.bias = nn.Parameter(torch.zeros(num_labels))
        
    def forward(self, input_ids, attention_mask):
        # 1. BERT 编码
        bert_out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_vec = bert_out.last_hidden_state[:, 0, :]   # (batch, 768)
        # 2. GCN 更新标签嵌入
        label_emb_updated = self.gcn(self.label_emb)    # (num_labels, 768)
        # 3. 点积分类
        logits = torch.mm(cls_vec, label_emb_updated.t()) + self.bias  # (batch, num_labels)
        return logits

# ---------- 6. 训练准备 ----------
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
train_dataset = MovieDataset(X_tr, y_tr, tokenizer, max_len=256)
val_dataset   = MovieDataset(X_va, y_va, tokenizer, max_len=256)
test_dataset  = MovieDataset(X_te, y_te, tokenizer, max_len=256)

batch_size = 16   # CPU 可适当减小
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader   = DataLoader(val_dataset,   batch_size=batch_size, shuffle=False)
test_loader  = DataLoader(test_dataset,  batch_size=batch_size, shuffle=False)

model = BERT_GCN_MultiLabel(num_labels=K, label_adj=adj_label, 
                            label_emb_dim=128, gcn_hidden=256)
model.to(DEVICE)

# 处理标签不平衡：计算正样本权重
pos_freq = y_tr.sum(axis=0)
neg_freq = len(y_tr) - pos_freq
pos_weight = torch.FloatTensor(neg_freq / np.maximum(pos_freq, 1)).to(DEVICE)
criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# 优化器：BERT 层使用较小学习率
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.bert.named_parameters() if not any(nd in n for nd in no_decay)], 'lr': 2e-5},
    {'params': [p for n, p in model.bert.named_parameters() if any(nd in n for nd in no_decay)], 'lr': 2e-5, 'weight_decay': 0.0},
    {'params': model.gcn.parameters(), 'lr': 1e-3},
    {'params': [model.label_emb, model.bias], 'lr': 1e-3},
]
optimizer = AdamW(optimizer_grouped_parameters, weight_decay=0.01)
total_steps = len(train_loader) * 5   # 训练 5 个 epoch
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(0.1*total_steps), num_training_steps=total_steps)

# ---------- 7. 评估函数 ----------
def evaluate(loader, model, threshold=0.5):
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)
            logits = model(input_ids, attention_mask)
            probs = torch.sigmoid(logits)
            preds = (probs > threshold).int()
            y_true.append(labels.cpu().numpy())
            y_pred.append(preds.cpu().numpy())
    y_true = np.vstack(y_true)
    y_pred = np.vstack(y_pred)
    micro_f1 = f1_score(y_true, y_pred, average='micro')
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    ham_loss = hamming_loss(y_true, y_pred)
    return micro_f1, macro_f1, ham_loss

# ---------- 8. 训练循环 ----------
num_epochs = 5
best_micro_f1 = 0.0
for epoch in range(num_epochs):
    model.train()
    total_loss = 0.0
    for i, batch in enumerate(train_loader):
        input_ids = batch['input_ids'].to(DEVICE)
        attention_mask = batch['attention_mask'].to(DEVICE)
        labels = batch['labels'].to(DEVICE)
        
        optimizer.zero_grad()
        logits = model(input_ids, attention_mask)
        loss = criterion(logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item()
        if (i+1) % 20 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Batch {i+1}/{len(train_loader)}, Loss: {loss.item():.4f}")
    
    avg_loss = total_loss / len(train_loader)
    # 验证
    micro_f1, macro_f1, ham_loss = evaluate(val_loader, model)
    print(f"\nEpoch {epoch+1} | Train Loss: {avg_loss:.4f} | Val Micro F1: {micro_f1:.4f} | Macro F1: {macro_f1:.4f} | Hamming: {ham_loss:.4f}")
    
    if micro_f1 > best_micro_f1:
        best_micro_f1 = micro_f1
        torch.save(model.state_dict(), 'best_model.pt')
        print("  -> saved best model")

# ---------- 9. 测试 ----------
model.load_state_dict(torch.load('best_model.pt'))
test_micro, test_macro, test_ham = evaluate(test_loader, model)
print(f"\n[Test] Micro F1: {test_micro:.4f} | Macro F1: {test_macro:.4f} | Hamming Loss: {test_ham:.4f}")

# 可选：输出每个类别的 F1（诊断）
from sklearn.metrics import f1_score
model.eval()
all_true, all_pred = [], []
with torch.no_grad():
    for batch in test_loader:
        input_ids = batch['input_ids'].to(DEVICE)
        attention_mask = batch['attention_mask'].to(DEVICE)
        logits = model(input_ids, attention_mask)
        pred = (torch.sigmoid(logits) > 0.5).int()
        all_true.append(batch['labels'].cpu().numpy())
        all_pred.append(pred.cpu().numpy())
y_true_test = np.vstack(all_true)
y_pred_test = np.vstack(all_pred)
per_class_f1 = f1_score(y_true_test, y_pred_test, average=None)
print("\nPer-class F1:")
for i, g in enumerate(GENRES):
    print(f"  {g:15s} : {per_class_f1[i]:.4f}")