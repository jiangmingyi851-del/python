# -*- coding: utf-8 -*-
"""
严格按 presentation.html 23 页内容生成 PPTX
图名完全匹配 HTML 中的 src="figures/xxx.png"
字号放大，Cobalt Grid 配色
"""
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

WORK = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)
with open('results.json', 'r', encoding='utf-8') as f:
    R = json.load(f)
FIG = os.path.join(WORK, 'figures')
OUT = os.path.join(WORK, '期末大作业汇报-2500010771-蒋名仪.pptx')

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Cobalt Grid 调色板 ──
BG   = RGBColor(0xF0, 0xEB, 0xDE)  # 奶油纸底
INK  = RGBColor(0x1F, 0x2B, 0xE0)  # 钴蓝
DARK = RGBColor(0x1A, 0x1E, 0x30)  # 正文深色
FADE = RGBColor(0x70, 0x6D, 0x60)  # 次级灰
FBOX = RGBColor(0xE4, 0xDF, 0xD2)  # 公式框底色
FN   = 'Microsoft YaHei'
FN_T = 'Georgia'                    # 标题衬线

# ── 样式表 (size, color, bold, space_before_pt, space_after_pt) ──
S = {
    'sec':  (18, INK,  True,  14, 4),   # 小节标题 (SEC-H)
    'body': (17, DARK, False,  2, 4),   # body-text
    'sub':  (16, FADE, False,  0, 3),   # body-sub
    'key':  (18, INK,  True,   4, 5),   # key-result
    'fm':   (18, INK,  False,  6, 3),   # 公式
    'fn':   (14, FADE, False,  0, 2),   # 公式注释
    'note': (14, FADE, False,  4, 2),   # 注
}

# ═══════════════════════ 工具函数 ═══════════════════════

def new_slide():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg = s.background.fill; bg.solid(); bg.fore_color.rgb = BG
    return s

def _line(slide, left, top, width):
    sh = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Pt(1.5))
    sh.fill.solid(); sh.fill.fore_color.rgb = INK; sh.line.fill.background()

def chrome(slide, tag, title):
    """上下发线 + 标题栏"""
    _line(slide, 0.6, 0.25, 12.13)
    _line(slide, 0.6, 7.15, 12.13)
    box = slide.shapes.add_textbox(Inches(0.6), Inches(0.38), Inches(12.13), Inches(0.72))
    tf = box.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]
    if tag:
        r = p.add_run(); r.text = tag + '   '
        r.font.size = Pt(18); r.font.color.rgb = INK; r.font.name = 'Consolas'
    r2 = p.add_run(); r2.text = title
    r2.font.size = Pt(32); r2.font.color.rgb = INK; r2.font.name = FN_T
    _line(slide, 0.6, 1.08, 12.13)

def tb(slide, left, top, width, height, blocks):
    """多段文本块"""
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame; tf.word_wrap = True
    first = True
    for kind, text in blocks:
        sz, clr, bold, sb, sa = S[kind]
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(sb); p.space_after = Pt(sa)
        r = p.add_run(); r.text = text
        r.font.size = Pt(sz); r.font.bold = bold; r.font.color.rgb = clr; r.font.name = FN
    return box

def pic(slide, name, left, top, width, height=None):
    fp = os.path.join(FIG, name)
    if not os.path.exists(fp):
        tb(slide, left, top, width, 0.5, [('note', f'[图缺失: {name}]')])
        return
    if height:
        slide.shapes.add_picture(fp, Inches(left), Inches(top), Inches(width), Inches(height))
    else:
        slide.shapes.add_picture(fp, Inches(left), Inches(top), Inches(width))

def pnum(slide, n, total=23):
    box = slide.shapes.add_textbox(Inches(11.6), Inches(6.85), Inches(1.4), Inches(0.3))
    p = box.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = f'{n:02d} / {total}'
    r.font.size = Pt(14); r.font.color.rgb = INK; r.font.name = 'Consolas'

# ── 左列 / 右列快捷常量 ──
L, R_X = 0.65, 6.95      # 左/右列 x
CW = 5.9                  # 列宽
CT = 1.2                  # content top
CH = 5.8                  # content height

# ═══════════════════════════════════════════════════════════
# SLIDE 1 — 封面
# ═══════════════════════════════════════════════════════════
s = new_slide()
_line(s, 0.6, 0.25, 12.13); _line(s, 0.6, 7.15, 12.13)
box = s.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(10), Inches(0.4))
r = box.text_frame.paragraphs[0].add_run(); r.text = 'FINAL PROJECT REPORT · 2026'
r.font.size = Pt(16); r.font.color.rgb = INK; r.font.name = 'Consolas'
box2 = s.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11), Inches(1.8))
p = box2.text_frame.paragraphs[0]
r2 = p.add_run(); r2.text = '期末大作业汇报'
r2.font.size = Pt(80); r2.font.color.rgb = INK; r2.font.name = FN_T
p2 = box2.text_frame.add_paragraph(); p2.space_before = Pt(12)
r3 = p2.add_run(); r3.text = '电影推荐系统 · 评分预测的优化与深化\n+ 电影类型预测的深化'
r3.font.size = Pt(26); r3.font.color.rgb = FADE; r3.font.name = FN
_line(s, 0.8, 4.6, 1.2)
box3 = s.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(5), Inches(0.4))
r4 = box3.text_frame.paragraphs[0].add_run(); r4.text = '蒋名仪  |  2500010771'
r4.font.size = Pt(18); r4.font.color.rgb = INK; r4.font.name = 'Consolas'
pnum(s, 1)

# ═══════════════════════════════════════════════════════════
# SLIDE 2 — 总览
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '', '期末新增任务一览')
rows = [
    ('2.3', '海报视觉特征增强评分预测',        'ResNet-50 → PCA → VisSVD',               '必做1a'),
    ('2.4', 'LLM 背景知识增强评分预测',        'DeepSeek + MiniLM → LightGBM 残差',       '必做1b'),
    ('2.5', '传统 SVD 与新方案对比 + Stacking', '4 专家 × 4 场景 + Ridge 元学习器',         '必做1c'),
    ('2.6', 'SVD 异常用户分析 + 画像 + 定向优化','残差阈值 → KMeans → 专家切换',            '必做2a'),
    ('2.7', '复杂模型：多专家 MOE',             'Gating MLP + softmax 动态路由',            '可选3'),
    ('3.1', 'MiniLM + 微调层预测电影类型',      'frozen MiniLM → Linear / MLP 头',          '必做T2'),
    ('3.2', '主题电影类 × 年龄相关性',          'LDA 主题 → 年龄区分度',                    '可选B1'),
    ('3.3', 'LLM Embedding + 微调预测类型',     'text-embedding-3-small → MLP-256',         '可选B2'),
    ('3.4', 'BERT 端到端微调预测类型',          'DistilBERT 67M → 多标签分类',              'NEW'),
]
for i, (n, ti, de, tag) in enumerate(rows):
    y = 1.22 + i * 0.6
    tb(s, 0.7,  y, 0.7, 0.5, [('key', n)])
    tb(s, 1.5,  y, 4.6, 0.5, [('body', ti)])
    tb(s, 6.2,  y, 5.2, 0.5, [('sub', de)])
    tb(s, 11.6, y, 1.4, 0.5, [('sub', tag)])
tb(s, 0.7, 6.75, 12, 0.4, [('note', '期中基线: M2 r̂=μ+bᵤ+bᵢ ; M3 FunkSVD 加潜因子 qᵢᵀpᵤ ; M2+ 叠加类型/人口学偏置')])
pnum(s, 2)

# ═══════════════════════════════════════════════════════════
# SLIDE 3 — 2.3 海报视觉 (思路+公式)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.3', '海报视觉：为什么需要图像信息？')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', '协同过滤只看"谁给哪部电影打了几分"，完全忽略电影的视觉风格。'),
    ('body', '对于几乎没人评分的冷门电影，潜因子 qᵢ 根本学不到——评分太少。但海报特征始终可用。'),
    ('sec',  '解决思路'),
    ('body', '把海报视觉向量 ṽᵢ 注入 SVD：即使 qᵢ 学不动，W·ṽᵢ 仍提供非零信号，缓解冷启动。'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  'M6 VisSVD 公式'),
    ('fm',   '  r̂ᵤᵢ = μ + bᵤ + bᵢ + pᵤᵀ(qᵢ + W·ṽᵢ)'),
    ('fn',   'ṽᵢ: 海报经 ResNet-50 → 512 维 → PCA 降至 64 维'),
    ('fn',   'W: 可学习的视觉→潜空间投影矩阵'),
    ('fn',   'qᵢ: 自由潜因子; 冷门电影 qᵢ≈0 时 W·ṽᵢ 兜底'),
    ('sec',  '实现流程'),
    ('sub',  'Step 1  ResNet-50 抽 512 维特征 → 缓存'),
    ('sub',  'Step 2  PCA 降到 64 维; 余弦相似度建 Visual Item-KNN (M5)'),
    ('sub',  'Step 3  将 ṽᵢ 注入 FunkSVD，联合训练 W (M6)'),
    ('sub',  'Step 4  按电影流行度分桶，考察冷门电影增益'),
])
pnum(s, 3)

# ═══════════════════════════════════════════════════════════
# SLIDE 4 — 2.3 海报视觉 (结果)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.3', '视觉特征结果：冷门电影增益最明显')
tb(s, L, CT, CW, CH, [
    ('sec',  '全量开放测试集 MSE'),
    ('key',  'M3 FunkSVD = 0.7144（训练充分的基座）'),
    ('sub',  'M5 Visual-KNN = 1.3373（纯视觉，无协同，较差）'),
    ('key',  'M6 VisSVD = 0.7184（协同 + 视觉）'),
    ('sec',  '为什么全量 MSE 提升不大？'),
    ('body', '视觉 side-info 只在冷门电影（评分<100）上 RMSE 降低明显。但冷门电影仅占测试集 0.6%，加权到全量后被严重稀释。'),
    ('sec',  '结论'),
    ('key',  '→ 典型的 "side-info 只在稀疏区域有效"'),
    ('sub',  '视觉特征的价值在于缓解冷启动，而非提升全量精度。'),
])
pic(s, '2_3_cold_movie.png', R_X, CT, CW)
pnum(s, 4)

# ═══════════════════════════════════════════════════════════
# SLIDE 5 — 2.4 LLM (思路+公式)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.4', 'LLM 背景知识：用"世界知识"补充协同')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', 'ratings 表只有行为信号。缺少电影的"世界知识"：口碑、主题、奖项、情绪基调。'),
    ('sec',  '双路径设计'),
    ('body', 'A 在线 LLM: DeepSeek API 返回 online_rating / themes / award_level / sentiment'),
    ('body', 'B 本地 MiniLM: name+intro+导演+主演 → 384 维语义向量 (API fallback)'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  'M7 内容残差模型公式'),
    ('fm',   '  r̂ᵤᵢ = r̂ᵤᵢ^(M2+) + g_θ(cᵢ, uᵤ)'),
    ('fn',   'cᵢ: 电影内容特征 (LLM ⊕ MiniLM 句向量)'),
    ('fn',   'uᵤ: 用户人口学特征 (年龄/性别/职业)'),
    ('fn',   'g_θ: LightGBM 学"基线遗漏的残差"'),
    ('sec',  '为什么用残差而非直接预测？'),
    ('body', 'M2+ 已拟合大部分评分模式。内容特征只学基线遗漏的部分，降低过拟合风险。'),
])
pnum(s, 5)

# ═══════════════════════════════════════════════════════════
# SLIDE 6 — 2.4 LLM (结果)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.4', 'LLM 内容残差：结果与启示')
tb(s, L, CT, CW, CH, [
    ('sec',  '关键结果'),
    ('key',  'M7 内容残差 (LightGBM) 开放 MSE = 0.8149'),
    ('sub',  '对比：M3 FunkSVD = 0.7144（训练充分的纯协同）'),
    ('sec',  '特征重要性分析'),
    ('body', 'M2_pred（协同基线）占绝对主导。occ/age/内容向量有补充贡献，但远不如协同信号。'),
    ('sec',  '为什么 M7 没有超过 M3？'),
    ('body', '基座 M3 训练充分后，已从行为信号中提取了绝大部分可预测信息。外部内容是补充而非主力。'),
    ('sec',  '结论'),
    ('key',  '该数据集行为信号已足够强——LLM 知识价值在冷启动场景'),
])
pic(s, '2_4_feature_importance.png', R_X, CT, CW)
pnum(s, 6)

# ═══════════════════════════════════════════════════════════
# SLIDE 7 — 2.5 Stacking (公式)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.5', 'Stacking：如何协同四个专家？')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', '四个专家各有所长，单看全量 MSE 看不出差异——在不同场景下优势不同。'),
    ('sec',  'Stacking 公式'),
    ('fm',   '  r̂^Stack = α₀ + αᵀz,   z = (M3, M2+, M6, M7)'),
    ('fm',   '  α = argmin ‖y − α₀1 − Zα‖² + λ‖α‖²'),
    ('fn',   'z: 四模型预测拼成 4 维向量; α: Ridge 元学习器权重'),
    ('fn',   '防泄漏: 用 meta-val 学 α, 不碰测试集'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  '场景分桶实测'),
    ('body', '冷门电影 → M6 VisSVD 略优 (视觉兜底)'),
    ('body', '稀有 genre / 热门头部 → M3 最优 (协同最强)'),
    ('body', 'M2+/M7 全场景被压制——行为协同已足够'),
    ('sec',  '为什么外部信息被压制？'),
    ('body', 'M3 训练充分后，行为信号已够强。人口学/内容与协同高度冗余 (相关性 0.98)。'),
])
pnum(s, 7)

# ═══════════════════════════════════════════════════════════
# SLIDE 8 — 2.5 Stacking (结果)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.5', 'Stacking 结果：强相关专家集成增益有限')
tb(s, L, CT, CW, CH, [
    ('sec',  '关键数值'),
    ('key',  'M3 FunkSVD（单模型）= 0.7144'),
    ('sub',  'Stacking（4 专家线性组合）= 0.7386'),
    ('sub',  'SegmentBlend（分场景混合）= 0.7132'),
    ('sec',  'Stacking 权重揭示了什么？'),
    ('body', 'M3 = 1.86, M2+ = −0.849, M6 = −0.277, M7 = 0.282'),
    ('body', 'M3 权重远超其他 → 元学习器几乎只信 M3'),
    ('sec',  '结论'),
    ('key',  '全局 Stacking 反而略差于 M3 单模型'),
    ('body', '专家高度相关时线性组合容易 meta 过拟合。集成要有真增益，专家必须"错在不同地方"。'),
])
pic(s, '2_5_stacking.png', R_X, CT, CW)
pnum(s, 8)

# ═══════════════════════════════════════════════════════════
# SLIDE 9 — 2.6① 异常定义+画像
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.6 ①', '异常用户：如何定义？画像是什么？')
tb(s, L, CT, CW, CH, [
    ('sec',  '异常定义（残差阈值法）'),
    ('fm',   '  异常 ← MAE_u ∈ Top 5%（评分数≥30 的活跃用户）'),
    ('fn',   'MAE_u: 用户 u 在 M3 上的平均绝对残差'),
    ('key',  '异常样本 ≈ 4.57%；异常用户 = 260 人'),
    ('sec',  '真实画像'),
    ('body', '职业：学生+教育工作者 32%（全体仅 25%）→ 偏高'),
    ('body', '年龄：横跨 18-24 / 25-34 / 35-44，非单一年龄段'),
    ('body', '题材：Comedy 各簇均居首，Romance 在爱情片簇突出'),
    ('sec',  '为什么这些人"异常"？'),
    ('sub',  '评分习惯个性化（过严/过松/口味偏窄），全局 M3 难拟合'),
])
pic(s, '2_6_profile.png', R_X, CT, CW, 2.6)
pic(s, '2_6_residual_hist.png', R_X, CT+2.8, CW, 2.6)
pnum(s, 9)

# ═══════════════════════════════════════════════════════════
# SLIDE 10 — 2.6② 聚类+专家切换
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.6 ②', '聚类画像 + 切换专家：谁该信谁？')
tb(s, L, CT, CW, CH, [
    ('sec',  'KMeans 聚类（行为特征）'),
    ('sub',  'C0/C1 中庸高残差型 — 均分中等，评分模式多样'),
    ('sub',  'C2 低分严苛型 — 均分低，低分比例高'),
    ('sub',  'C3 高分宽松型 — 均分高，高分比例高'),
    ('sec',  '异常用户上谁最准？'),
    ('body', 'M3 = 1.346  |  M6 VisSVD = 1.342（最优）'),
    ('body', 'M2+ = 1.510  |  M7 LLM = 1.490（远差）'),
    ('sec',  '启示'),
    ('key',  '异常用户误差 ≈ 正常用户的 2 倍'),
    ('body', 'M2+/M7 反而更差 → 异常源于个人潜在口味，潜因子+视觉最贴合'),
])
pic(s, '2_6_clusters.png', R_X, CT, CW, 2.6)
pic(s, '2_6_expert_switch.png', R_X, CT+2.8, CW, 2.6)
pnum(s, 10)

# ═══════════════════════════════════════════════════════════
# SLIDE 11 — 2.6③ 定向优化
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.6 ③', '异常用户定向优化：效果与反思')
tb(s, L, CT, CW, CH, [
    ('sec',  '方法一：重估用户偏置'),
    ('fm',   '  bᵤ* = Σ(rᵤᵢ − μ − bᵢ) / (|I(u)| + λᵤ)'),
    ('fn',   '固定 bᵢ，只用用户自己的残差收缩估计 bᵤ*'),
    ('sec',  '方法二：簇专属专家融合'),
    ('fm',   '  r̂ᵤᵢ = Σₖ w_{g(u),k} · r̂ᵤᵢ^(k)'),
    ('fm',   '  w_g = softmax(−MSE_g / τ)'),
    ('fn',   'g(u): 用户所属簇; 按各专家在该簇的误差学权重'),
    ('sec',  '结果'),
    ('key',  '异常用户 MSE: 1.342 → 1.344（基本持平）'),
    ('body', '基座训练充分后，异常用户误差已是不可约噪声，后处理无效。'),
    ('body', '价值在于"识别+分流"，而非强行校准。'),
])
pic(s, '2_6_abnormal_optimization.png', R_X, CT, CW)
pnum(s, 11)

# ═══════════════════════════════════════════════════════════
# SLIDE 12 — 2.7 MOE (公式)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.7', 'MOE：按样本动态选专家')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', 'Stacking 给所有样本同一组权重。但不同场景、不同用户，该信的专家不同。'),
    ('sec',  'MOE 公式'),
    ('fm',   '  r̂ᵤᵢ = Σₖ πₖ(xᵤᵢ;θ) · r̂ₖ(u,i),  Σπₖ = 1'),
    ('fm',   '  π = softmax(W₂ · ReLU(W₁x + b₁) + b₂)'),
    ('fn',   'πₖ: 第 k 个专家的 softmax 权重 (样本级动态)'),
    ('fn',   'xᵤᵢ: 上下文特征; 专家参数固定，只训练 gating'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  '与 Stacking 的关键区别'),
    ('body', 'Stacking = 全局固定权重 α（所有样本共享）'),
    ('body', 'MOE = 按样本动态权重 π(x)（软路由）'),
    ('sec',  'Router 输入特征'),
    ('body', '用户评分数/均值/方差'),
    ('body', '电影热度、冷启动标志、稀有 genre 标志'),
    ('body', '异常用户簇 one-hot'),
    ('sub',  '→ 让路由自动选最合适的专家'),
])
pnum(s, 12)

# ═══════════════════════════════════════════════════════════
# SLIDE 13 — 2.7 MOE (结果)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '2.7', 'MOE 结果：为什么 MOE ≈ M3？')
tb(s, L, CT, CW, CH, [
    ('sec',  '关键结果'),
    ('key',  'MOE 开放 MSE = 0.7143'),
    ('sub',  '4 experts: M3 / M2+ / M6 / M7'),
    ('sub',  '对比 M3 = 0.7144 — 几乎相同'),
    ('sec',  '路由权重分析'),
    ('body', 'Router 收敛到几乎只用 M3（权重 ≈ 0.99）'),
    ('body', '这是 MOE 的正确行为：某专家全场景更优时，理性路由器自动归一到它。'),
    ('sec',  '结论'),
    ('key',  'MOE 动态路由比 Stacking 固定权重更合理'),
    ('body', '但"一家独大"格局下，动态路由没有发挥空间。需要更互补的专家。'),
])
pic(s, '2_7_moe_compare.png', R_X, CT, CW)
pnum(s, 13)

# ═══════════════════════════════════════════════════════════
# SLIDE 14 — 3.1 MiniLM (公式)
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '3.1', 'MiniLM 语义替代 TF-IDF 预测电影类型')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', '期中用 TF-IDF 词袋做类型预测，丢了词序与上下文语义。改用预训练 transformer 语义表示。'),
    ('sec',  '为什么冻结 encoder + 浅头？'),
    ('body', '数据仅 ~2k 部电影。全微调容易过拟合。冻结 MiniLM (22M 参数) 抽 384 维句向量，只训练浅分类头。'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  '公式'),
    ('fm',   '  zᵢ = MiniLM(introᵢ) ∈ ℝ³⁸⁴'),
    ('fm',   '  F (线性头): ŷ = σ(W·zᵢ + b)'),
    ('fm',   '  G (MLP 头): ŷ = σ(W₂·ReLU(W₁·zᵢ) + b)'),
    ('fn',   'σ: sigmoid (逐 genre 独立输出 0/1)'),
    ('fn',   '损失: BCEWithLogitsLoss (多标签二分类)'),
    ('sec',  '评测指标 (多标签)'),
    ('sub',  'Hamming loss · Jaccard · F1-macro · F1-samples · Subset accuracy'),
])
pnum(s, 14)

# ═══════════════════════════════════════════════════════════
# SLIDE 15 — 3.1 MiniLM (结果)
# ═══════════════════════════════════════════════════════════
gr = R['genre_results']
s = new_slide(); chrome(s, '3.1', 'MiniLM 结果：语义表示稳定提升')
tb(s, L, CT, CW, CH, [
    ('sec',  '横向对比'),
    ('sub',  f'B  LR-OVR (TF-IDF): F1-samples = {gr[1]["f1_samples"]}'),
    ('sub',  f'F  MiniLM + Linear: F1-samples = {gr[3]["f1_samples"]}'),
    ('key',  f'G  MiniLM + MLP: F1-samples = {gr[4]["f1_samples"]}'),
    ('sec',  '逐级提升的原因'),
    ('body', 'TF-IDF → MiniLM：关键词匹配 → 语义理解'),
    ('body', 'Linear → MLP：genre 间非线性关系 (Action+Sci-Fi 共现)，MLP 能捕捉交互模式'),
    ('sec',  '结论'),
    ('key',  'MLP 头 > 线性头 > TF-IDF 基线'),
    ('sub',  '语义表示 + 适当分类头 = 小数据多标签最佳实践'),
])
pic(s, '3_1_genre_compare.png', R_X, CT, CW)
pnum(s, 15)

# ═══════════════════════════════════════════════════════════
# SLIDE 16 — 3.2 主题×年龄
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '3.2', 'LDA 主题 × 年龄：哪些偏好随年龄变化？')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', '用 LDA 从简介中抽取语义主题，研究哪些主题偏好随年龄显著变化。'),
    ('sec',  '公式'),
    ('fm',   '  πd ∈ Δ^(K-1)  (电影 d 的 LDA 主题分布)'),
    ('fm',   '  discrimₖ = (1/|A|) Σₐ (r̄ₖₐ − r̄ₖ)²'),
    ('fn',   'r̄ₖₐ: 年龄段 a 对主题 k 的加权平均评分'),
    ('sec',  'Top 年龄敏感主题'),
    ('sub',  't1: love, man, falls, woman, young (爱情/青春)'),
    ('sub',  't2: war, world, ii, group, evil (战争/历史)'),
    ('sub',  't5: new, life, york (都市/生活)'),
    ('sec',  '结论'),
    ('key',  '各主题评分都随年龄升高 → 年长用户打分更宽容'),
])
pic(s, '3_2_theme_age.png', R_X, CT, CW)
pnum(s, 16)

# ═══════════════════════════════════════════════════════════
# SLIDE 17 — 3.3 LLM Embedding
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '3.3', 'LLM 高维嵌入：进一步提升类型预测')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心问题'),
    ('body', 'MiniLM 384 维是通用小模型。能否换成大模型句嵌入 (1536 维)？'),
    ('sec',  '公式'),
    ('fm',   '  zᵢ^LLM = Embed_API(introᵢ) ∈ ℝ¹⁵³⁶'),
    ('fm',   '  H: ŷ = σ(MLP₂₅₆(zᵢ^LLM))'),
    ('fn',   '1536 维 → 256 隐层 MLP → sigmoid 多标签'),
    ('fn',   'Dropout=0.4 + weight decay 抑制过拟合'),
    ('sec',  '结果'),
    ('sub',  f'G MiniLM+MLP: F1 = {gr[4]["f1_samples"]}'),
    ('key',  f'H LLM-emb+MLP: F1 = {gr[5]["f1_samples"]}'),
    ('sec',  '结论'),
    ('key',  '高维语义嵌入 + 正则 → 冻结方案最优'),
    ('sub',  '但嵌入是"冻结"的——能否端到端学习？→ 3.4'),
])
pic(s, '3_3_full_genre.png', R_X, CT, CW)
pnum(s, 17)

# ═══════════════════════════════════════════════════════════
# SLIDE 18 — 3.4 BERT 微调 (NEW)
# ═══════════════════════════════════════════════════════════
bert_r = [r for r in gr if r['model'] == 'I BERT-finetune']
bert_f1 = bert_r[0]['f1_samples'] if bert_r else '—'
s = new_slide(); chrome(s, '3.4', 'BERT 端到端微调：让语义表示针对任务学习')
tb(s, L, CT, CW, CH, [
    ('sec',  '核心思路'),
    ('body', '之前的方案都是冻结嵌入+训练浅头——预训练模型不了解"电影类型"任务。'),
    ('body', '端到端微调：让 DistilBERT 6700 万参数全部针对分类任务更新。'),
    ('sec',  '公式'),
    ('fm',   '  I: ŷ = σ(Wc · ReLU(Wp · BERT_θ(introᵢ)_[CLS]))'),
    ('fn',   'θ 端到端更新, lr=2e-5, 4 epochs, CPU ~95 min'),
    ('sec',  '结果对比'),
    ('sub',  f'H LLM-emb+MLP (冻结 1536 维): F1 = {gr[5]["f1_samples"]}'),
    ('key',  f'I BERT-finetune (端到端 67M): F1 = {bert_f1}'),
    ('sec',  '分析'),
    ('body', 'DistilBERT 微调 4 epoch 已接近冻结 LLM 1536 维方案。'),
    ('body', 'CPU 限制了训练轮数；GPU 或更多 epoch 可进一步提升。'),
])
pic(s, '3_4_bert_finetune.png', R_X, CT, CW)
pnum(s, 18)

# ═══════════════════════════════════════════════════════════
# SLIDE 19 — 关键发现
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '关键发现', '最大杠杆：把基座 SVD 训练充分')
tb(s, L, CT, CW, CH, [
    ('sec',  '发现了什么？'),
    ('body', '原始 FunkSVD 每 epoch 仅采样 ~32% 数据 → 严重欠拟合。'),
    ('body', '改为全量向量化 mini-batch SGD，纯 CPU，≈ 35s。'),
    ('sec',  '效果'),
    ('key',  'M3 MSE: 0.823 → 0.714   ↓ 13.2%'),
    ('key',  '异常用户 MSE: 1.69 → 1.34'),
    ('body', '这一步的提升，远超海报/LLM/Stacking/MOE 全部叠加之和。'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  '为什么这才是关键？'),
    ('body', 'side-info 只在协同信号不足时有用。基座没训练好时，side-info 看起来"有效"，实际只是弥补欠拟合。'),
    ('body', '一旦基座训练充分，side-info 的边际贡献几乎消失。'),
    ('sec',  '核心 Takeaway'),
    ('key',  '主瓶颈是基座是否训练充分，不是缺信息'),
])
pnum(s, 19)

# ═══════════════════════════════════════════════════════════
# SLIDE 20 — 反思诊断
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '反思', '为什么新增信息对全量 MSE 提升有限？')
tb(s, L, CT, 12, CH, [
    ('sec',  '根因一：新增信息与协同高度冗余'),
    ('body', 'M3 与 M6 预测相关性 0.98。冷门电影仅占测试集 0.6%，冷用户 0%——side-info 加权到全量后被稀释。'),
    ('sec',  '根因二：误差已接近不可约噪声地板'),
    ('body', '同一用户对同类电影评分波动大。M3 = 0.714 已逼近该数据的可预测性极限。'),
    ('sec',  '根因三：集成/后处理天然增益小'),
    ('body', 'M2+/M7 全面被 M3 压制; Stacking = 0.739 反而 > M3 (meta 过拟合); 异常后处理持平。'),
    ('body', '这些是结构性原因：行为信号足够强、基座充分训练后，外部信息边际收益天然很小。'),
])
pnum(s, 20)

# ═══════════════════════════════════════════════════════════
# SLIDE 21 — 更优方向
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '反思', '更能提升的方向')
tb(s, L, CT, 12, CH, [
    ('sec',  '① 升级矩阵分解模型'),
    ('body', 'SVD++ (纳入隐式反馈)、timeSVD++ (偏置随时间漂移)。当前 FunkSVD 只用了显式评分。'),
    ('sec',  '② 联合建模而非"残差外挂"'),
    ('body', 'FM / DeepFM 把潜因子+人口学+内容放进一个模型，直接学交叉项。'),
    ('sec',  '③ 集成要"去相关"'),
    ('body', '加入 user/item-KNN 等误差结构不同的模型，集成才有真增益。'),
    ('sec',  '④ 换评测目标'),
    ('body', '推荐真正在意排序 (NDCG / Recall@K)，side-info 对排序帮助远大于逐点 MSE。'),
])
pnum(s, 21)

# ═══════════════════════════════════════════════════════════
# SLIDE 22 — 总结
# ═══════════════════════════════════════════════════════════
s = new_slide(); chrome(s, '总结', '期末总结与关键结论')
tb(s, L, CT, CW, CH, [
    ('sec',  '评分预测 (Part 2) 全量 MSE'),
    ('key',  'M3 FunkSVD（训练充分）  0.7144 ← 最佳'),
    ('sub',  'M6 VisSVD 0.7184 · M7 LLM 0.8149'),
    ('sub',  'Stacking 0.739 · SegBlend 0.713 · MOE 0.714'),
    ('sec',  '类型预测 (Part 3)'),
    ('key',  f'最佳 H (LLM 1536 维 + MLP-256) F1 = {gr[5]["f1_samples"]}'),
    ('sub',  f'I BERT 微调 (端到端 67M) F1 = {bert_f1}'),
    ('sec',  '异常用户'),
    ('sub',  '260 人，学生/教育工作者偏多，应"识别+分流"'),
])
tb(s, R_X, CT, CW, CH, [
    ('sec',  '核心 Takeaways'),
    ('body', '① Side-info 只在稀疏区域有价值，全量提升有限是结构性的'),
    ('body', '② 异常用户应"识别+分流到合适专家"'),
    ('body', '③ MOE 动态路由比 Stacking 更合理'),
    ('body', '④ 语义嵌入+浅头 = 小数据最优; 端到端微调是进一步方向'),
    ('key',  '⑤ 最大杠杆 = 训练充分的基座 SVD（↓13%）'),
])
pnum(s, 22)

# ═══════════════════════════════════════════════════════════
# SLIDE 23 — 谢谢
# ═══════════════════════════════════════════════════════════
s = new_slide()
_line(s, 0.6, 0.25, 12.13); _line(s, 0.6, 7.15, 12.13)
box = s.shapes.add_textbox(Inches(3), Inches(2.2), Inches(7.3), Inches(2))
p = box.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
r = p.add_run(); r.text = '谢谢'
r.font.size = Pt(100); r.font.color.rgb = INK; r.font.name = FN_T
_line(s, 9.1, 4.3, 1.2)
box2 = s.shapes.add_textbox(Inches(3), Inches(4.6), Inches(7.3), Inches(0.5))
p2 = box2.text_frame.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
r2 = p2.add_run(); r2.text = '蒋名仪   2500010771'
r2.font.size = Pt(20); r2.font.color.rgb = INK; r2.font.name = 'Consolas'
pnum(s, 23)

# ═══════════════════════════════════════════════════════════
prs.save(OUT)
print(f'Saved: {OUT}')
print(f'Total slides: {len(prs.slides)}')

# 验证图片是否全部找到
import re
html_figs = set()
with open(os.path.join(WORK, 'presentation.html'), 'r', encoding='utf-8') as f:
    for m in re.finditer(r'src="figures/([^"]+)"', f.read()):
        html_figs.add(m.group(1))
existing = set(os.listdir(FIG))
missing = html_figs - existing
print(f'\nHTML references {len(html_figs)} figures, {len(html_figs & existing)} found, {len(missing)} missing')
if missing:
    for m in sorted(missing):
        print(f'  MISSING: {m}')
