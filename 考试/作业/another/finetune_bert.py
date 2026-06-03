# -*- coding: utf-8 -*-
"""
BERT 端到端微调 — 电影类型多标签预测
复用 run_final.py 相同的数据加载和划分逻辑
"""
import os, sys, json, re, time, warnings
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, jaccard_score, hamming_loss, accuracy_score

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification

np.random.seed(2024)
torch.manual_seed(42)

WORK = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)
FIG = os.path.join(WORK, 'figures')
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Device: {DEVICE}")

MODEL_NAME = os.path.expanduser('~/.cache/hf_local/distilbert-base-uncased')
MAX_LEN = 128
BATCH_SIZE = 16
EPOCHS = 4
LR = 2e-5

# ===== 加载数据 (与 run_final.py PART 3 完全一致) =====
print("Loading data...")
movies_info = pd.read_csv('./data/info.csv', encoding='latin-1',
                           usecols=['id', 'name', 'genre', 'intro'])
movies_info.rename(columns={'id': 'movie_id'}, inplace=True)
df_g = movies_info.dropna(subset=['intro', 'genre']).copy()
df_g = df_g[df_g['genre'].str.len() > 0]

def clean_text(s):
    s = str(s).lower()
    s = re.sub(r'<.*?>', '', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

df_g['text'] = (df_g['name'].fillna('') + ' . ' + df_g['intro'].fillna('')).map(clean_text)
df_g['labels'] = df_g['genre'].str.split('|')

mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(df_g['labels'])
n_classes = len(mlb.classes_)
X_text = df_g['text'].values
print(f"  Samples: {len(df_g)}, Classes: {n_classes}")
print(f"  Labels: {list(mlb.classes_)}")

X_tr_t, X_tmp, y_tr_g, y_tmp = train_test_split(X_text, Y, test_size=0.25, random_state=42)
X_va_t, X_te_t, y_va_g, y_te_g = train_test_split(X_tmp, y_tmp, test_size=0.6, random_state=42)
print(f"  Train: {len(X_tr_t)}, Val: {len(X_va_t)}, Test: {len(X_te_t)}")

# ===== Tokenizer =====
print(f"Loading tokenizer: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# ===== Dataset =====
class MovieDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.encodings = tokenizer(
            list(texts), padding='max_length', truncation=True,
            max_length=max_len, return_tensors='pt'
        )
        self.labels = torch.tensor(labels, dtype=torch.float32)

    def __getitem__(self, idx):
        item = {k: v[idx] for k, v in self.encodings.items()}
        item['labels'] = self.labels[idx]
        return item

    def __len__(self):
        return len(self.labels)

print("Tokenizing...")
t0 = time.time()
tr_dataset = MovieDataset(X_tr_t, y_tr_g, tokenizer, MAX_LEN)
va_dataset = MovieDataset(X_va_t, y_va_g, tokenizer, MAX_LEN)
te_dataset = MovieDataset(X_te_t, y_te_g, tokenizer, MAX_LEN)
print(f"  Tokenization done in {time.time()-t0:.1f}s")

tr_loader = DataLoader(tr_dataset, batch_size=BATCH_SIZE, shuffle=True)
va_loader = DataLoader(va_dataset, batch_size=BATCH_SIZE)
te_loader = DataLoader(te_dataset, batch_size=BATCH_SIZE)

# ===== Model =====
print(f"Loading model: {MODEL_NAME}")
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=n_classes,
    problem_type='multi_label_classification'
).to(DEVICE)
total_params = sum(p.numel() for p in model.parameters())
print(f"  Total params: {total_params:,}")

# ===== Training =====
optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
loss_fn = nn.BCEWithLogitsLoss()

def evaluate(model, loader):
    model.eval()
    all_logits, all_labels = [], []
    with torch.no_grad():
        for batch in loader:
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels']
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            all_logits.append(outputs.logits.cpu())
            all_labels.append(labels)
    logits = torch.cat(all_logits).numpy()
    labels = torch.cat(all_labels).numpy()
    preds = (torch.sigmoid(torch.tensor(logits)).numpy() > 0.5).astype(int)
    f1 = f1_score(labels, preds, average='samples', zero_division=0)
    return f1, preds, labels, logits

best_f1 = -1
best_state = None
print(f"\n{'='*60}")
print(f"Fine-tuning {MODEL_NAME} for {EPOCHS} epochs")
print(f"{'='*60}")

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    t_start = time.time()
    for step, batch in enumerate(tr_loader):
        input_ids = batch['input_ids'].to(DEVICE)
        attention_mask = batch['attention_mask'].to(DEVICE)
        labels = batch['labels'].to(DEVICE)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
        if (step + 1) % 50 == 0:
            print(f"  Epoch {epoch+1}/{EPOCHS} step {step+1}/{len(tr_loader)} loss={loss.item():.4f}")

    avg_loss = total_loss / len(tr_loader)
    val_f1, _, _, _ = evaluate(model, va_loader)
    elapsed = time.time() - t_start
    print(f"  Epoch {epoch+1}/{EPOCHS}: loss={avg_loss:.4f}, val_f1={val_f1:.4f}, time={elapsed:.0f}s")

    if val_f1 > best_f1:
        best_f1 = val_f1
        best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
        print(f"  ** New best val F1: {best_f1:.4f}")

# ===== Load best and evaluate on test =====
model.load_state_dict(best_state)
te_f1, te_preds, te_labels, te_logits = evaluate(model, te_loader)

hamming = hamming_loss(te_labels, te_preds)
jaccard = jaccard_score(te_labels, te_preds, average='samples', zero_division=0)
f1_macro = f1_score(te_labels, te_preds, average='macro', zero_division=0)
f1_samples = f1_score(te_labels, te_preds, average='samples', zero_division=0)
subset_acc = accuracy_score(te_labels, te_preds)

print(f"\n{'='*60}")
print(f"TEST RESULTS — {MODEL_NAME} fine-tuned")
print(f"{'='*60}")
print(f"  Hamming Loss: {hamming:.4f}")
print(f"  Jaccard:      {jaccard:.4f}")
print(f"  F1 macro:     {f1_macro:.4f}")
print(f"  F1 samples:   {f1_samples:.4f}")
print(f"  Subset Acc:   {subset_acc:.4f}")

result = {
    'model': 'I BERT-finetune',
    'hamming': round(hamming, 4),
    'jaccard': round(jaccard, 4),
    'f1_macro': round(f1_macro, 4),
    'f1_samples': round(f1_samples, 4),
    'subset_acc': round(subset_acc, 4)
}
print(f"\nResult dict: {json.dumps(result, indent=2)}")

# ===== Update results.json =====
results_path = os.path.join(WORK, 'results.json')
with open(results_path, 'r', encoding='utf-8') as f:
    R = json.load(f)

existing = [r for r in R['genre_results'] if r['model'] != 'I BERT-finetune']
existing.append(result)
R['genre_results'] = existing
R['bert_finetune_model'] = MODEL_NAME

with open(results_path, 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=2, default=str)
print(f"Updated {results_path}")

# ===== Generate updated comparison figure =====
gr = pd.DataFrame(R['genre_results'])
fig, ax = plt.subplots(figsize=(13, 5))
xs = np.arange(len(gr))
w = 0.20
for offs, (col, color) in enumerate(zip(
    ['jaccard', 'f1_macro', 'f1_samples', 'subset_acc'],
    ['#FF6B6B', '#5C7AEA', '#2EC4B6', '#9D6EFF'])):
    ax.bar(xs + (offs - 1.5) * w, gr[col], w, label=col, color=color)
ax.set_xticks(xs)
ax.set_xticklabels(gr['model'], rotation=15, ha='right')
ax.legend(loc='upper left', fontsize=9)
ax.set_title('Genre Prediction: All Models Comparison', fontweight='bold')
ax.set_ylabel('Score')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
fig_path = os.path.join(FIG, '3_4_bert_finetune.png')
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()
print(f"Saved figure: {fig_path}")

print("\nDone!")
