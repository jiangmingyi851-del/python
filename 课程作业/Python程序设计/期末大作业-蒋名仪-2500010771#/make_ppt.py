# -*- coding: utf-8 -*-
"""
生成期末大作业汇报 PPT (重做版)
用法:  python make_ppt.py
依赖:  python-pptx, results.json, figures/

设计原则 (对齐待办要求):
- 只讲期末新增任务 2.3-2.7 / 3.1-3.3; 期中模型仅作为"已有基线 SVD/M2+"一句带过。
- 每个算法页按 notebook markdown 的逻辑写: 问题动机 -> 核心思想 -> 公式(含符号解释)
  -> 实现步骤 -> 评测设计 -> 结果与结论, 而不是只堆技术名。
- 异常用户分析以 notebook 真实结论为准: 学生/教育工作者居多, Comedy 主导 + Romance 突出,
  年龄横跨 18-44, 异常用户上潜因子/视觉协同专家最优。
- 公式用 Unicode 排版, 符号在下一行解释; 文字精炼但保留逻辑与公式。
"""
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

WORK = os.path.dirname(os.path.abspath(__file__))
os.chdir(WORK)
with open('results.json', 'r', encoding='utf-8') as f:
    R = json.load(f)
FIG = os.path.join(WORK, 'figures')
OUT = os.path.join(WORK, '期末大作业汇报-2500010771-蒋名仪.pptx')

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ---------- palette ----------
BG = RGBColor(0x14, 0x18, 0x2B)
BG2 = RGBColor(0x1C, 0x24, 0x42)
BLUE = RGBColor(0x6F, 0x9B, 0xFF)
TEAL = RGBColor(0x2E, 0xC4, 0xB6)
RED = RGBColor(0xFF, 0x77, 0x77)
GOLD = RGBColor(0xFF, 0xC4, 0x5A)
WHITE = RGBColor(0xF2, 0xF4, 0xFA)
GRAY = RGBColor(0xA6, 0xAE, 0xC8)
FONT = 'Microsoft YaHei'


def num(key, default='—'):
    v = R.get(key, None)
    return default if v is None else v


def slide_blank():
    s = prs.slides.add_slide(prs.slide_layouts[6])
    f = s.background.fill
    f.solid()
    f.fore_color.rgb = BG
    return s


def title_bar(slide, tag, title, color=BLUE):
    # 左侧色条 + 编号 chip + 标题
    bar = slide.shapes.add_textbox(Inches(0.0), Inches(0.28), Inches(0.18), Inches(0.72))
    bf = bar.fill
    box = slide.shapes.add_textbox(Inches(0.45), Inches(0.28), Inches(12.4), Inches(0.95))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = tag + '   '
    r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = color; r.font.name = FONT
    r2 = p.add_run(); r2.text = title
    r2.font.size = Pt(26); r2.font.bold = True; r2.font.color.rgb = WHITE; r2.font.name = FONT
    # underline rule
    line = slide.shapes.add_shape(1, Inches(0.45), Inches(1.18), Inches(12.45), Pt(2))
    line.fill.solid(); line.fill.fore_color.rgb = color
    line.line.fill.background()
    return box


# styles for text blocks: (size, color, bold, space_before, space_after, indent_chars)
STYLE = {
    'h':  (15, GOLD, True, 6, 2),     # 小节标题 (动机/核心思想/...)
    'b':  (13, WHITE, False, 0, 2),   # 普通要点
    'sub':(12, GRAY, False, 0, 1),    # 次级说明
    'f':  (14, TEAL, False, 3, 1),    # 公式
    'fn': (11, GRAY, False, 0, 3),    # 公式符号解释
    'n':  (12, GRAY, False, 2, 1),    # 注
    'k':  (14, BLUE, True, 2, 2),     # 关键结果
}


def textcol(slide, left, top, width, height, blocks, base=None):
    """blocks: list of (kind, text). kind in STYLE keys."""
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for kind, text in blocks:
        size, color, bold, sb, sa = STYLE[kind]
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(sb)
        p.space_after = Pt(sa)
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = FONT
    return tb


def img(slide, name, left, top, width, height=None):
    fp = os.path.join(FIG, name)
    if os.path.exists(fp):
        if height:
            slide.shapes.add_picture(fp, Inches(left), Inches(top), Inches(width), Inches(height))
        else:
            slide.shapes.add_picture(fp, Inches(left), Inches(top), Inches(width))
    else:
        textcol(slide, left, top, width, 0.6, [('n', f'[图缺失: {name} — 请先运行 run_final.py]')])


def caption(slide, left, top, width, text, color=GRAY, size=11):
    textcol(slide, left, top, width, 0.5, [('sub', text)])


# =================================================================
# Slide 1: 封面
# =================================================================
s = slide_blank()
s.shapes.add_picture  # noop ref
band = s.shapes.add_shape(1, Inches(0), Inches(2.55), Inches(13.333), Inches(1.7))
band.fill.solid(); band.fill.fore_color.rgb = BG2; band.line.fill.background()
textcol(s, 1.0, 1.15, 11.3, 1.2, [('h', '')])
t = s.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.3), Inches(1.0))
p = t.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = '期末大作业汇报'
r.font.size = Pt(46); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
textcol(s, 1.0, 3.75, 11.3, 0.7,
        [('b', '电影推荐系统 · 评分预测的优化与深化  +  电影类型预测的深化')]).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
sub = s.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.3), Inches(0.5))
pp = sub.text_frame.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
rr = pp.add_run(); rr.text = '蒋名仪   |   2500010771'
rr.font.size = Pt(20); rr.font.color.rgb = BLUE; rr.font.name = FONT
foot = s.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(0.5))
pf = foot.text_frame.paragraphs[0]; pf.alignment = PP_ALIGN.CENTER
rf = pf.add_run()
rf.text = '期末新增任务: 海报视觉 · LLM 背景知识 · 多方案协同 · 异常用户画像 · MOE · BERT/LLM 类型预测'
rf.font.size = Pt(13); rf.font.color.rgb = GRAY; rf.font.name = FONT

# =================================================================
# Slide 2: 期末任务总览 (期中仅一句带过)
# =================================================================
s = slide_blank()
title_bar(s, '总览', '期末新增任务一览')
rows = [
    ('2.3', '海报视觉特征增强评分预测', 'ResNet-50 → PCA → Visual-KNN / VisSVD', '必做1a'),
    ('2.4', 'LLM 背景知识增强评分预测', 'DeepSeek API + MiniLM 句向量 → 内容残差(LightGBM)', '必做1b'),
    ('2.5', '传统 SVD 与新方案对比 + Stacking', '4 专家 × 4 场景 + Ridge 元学习器', '必做1c'),
    ('2.6', 'SVD 异常样本分析 + 异常用户画像', '残差阈值 → KMeans 画像 → 切换专家 / 定向校准', '必做2a+可选A2'),
    ('2.7', '复杂模型: 分类器 + 多专家 MOE', 'Gating MLP + softmax 动态路由', '可选3'),
    ('3.1', 'BERT/MiniLM + 微调层预测类型', 'frozen MiniLM → Linear / MLP 多标签头', '必做Task2'),
    ('3.2', '主题电影类 × 年龄相关性', 'LDA 主题 → 年龄区分度 → 交互项建模', '可选B1'),
    ('3.3', 'LLM Embedding + 微调预测类型', 'yunwu.ai embedding(1536维) → MLP-256', '可选B2'),
]
for i, (n_, ti, de, tag) in enumerate(rows):
    y = 1.45 + i * 0.66
    textcol(s, 0.6, y, 1.0, 0.5, [('k', n_)])
    textcol(s, 1.55, y, 5.0, 0.5, [('b', ti)])
    textcol(s, 6.5, y, 5.0, 0.5, [('sub', de)])
    textcol(s, 11.7, y, 1.4, 0.5, [('sub', tag)])
textcol(s, 0.6, 6.95, 12.4, 0.5, [
    ('n', '期中基线(仅作对照, 不展开): M2 加性偏置 r̂=μ+b_u+b_i ; M3 FunkSVD 加潜因子 q_i·p_u ; M2+ 再叠加类型/人口学偏置。')
])

# =================================================================
# Slide 3: 2.3 海报视觉
# =================================================================
s = slide_blank()
title_bar(s, '2.3', '海报视觉特征增强评分预测')
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 问题动机'),
    ('b', '协同过滤只看"谁打了几分", 完全没用电影画面。海报里的色调/构图/'),
    ('b', '人物排布是稳定的"风格信号", 对几乎没人评分的冷门电影尤其宝贵。'),
    ('h', '② 核心思想'),
    ('b', '把海报视觉向量作为电影 side-information 注入预测: 即使某电影评分极少,'),
    ('b', '视觉向量仍能给它一个非零的潜因子估计, 缓解冷启动。'),
    ('h', '③ 公式 (M6 VisSVD)'),
    ('f', '  r̂_ui = μ + b_u + b_i + p_uᵀ ( q_i + W·ṽ_i )'),
    ('fn', 'ṽ_i: 海报 PCA 后视觉向量; W: 视觉→潜空间投影(可学习);'),
    ('fn', 'q_i: 自由潜因子; 冷门电影 q_i 学不动时, W·ṽ_i 仍提供信号。'),
    ('h', '④ 实现步骤'),
    ('sub', 'Step1 ResNet-50/Img2Vec 抽 512维海报特征 (缓存 poster_feat.pkl)'),
    ('sub', 'Step2 PCA 降到 64维去噪; 余弦相似度建 Visual Item-KNN (M5)'),
    ('sub', 'Step3 把 ṽ_i 注入 FunkSVD 训练 W (M6 VisSVD)'),
    ('sub', 'Step4 按电影流行度分桶, 单独看冷门电影增益'),
])
img(s, '2_3_cold_movie.png', 7.0, 1.5, 6.0)
mse23 = f"全量开放 MSE:  M3={num('M3_MSE')}   M5_VisKNN={num('M5_VisKNN_MSE')}   M6_VisSVD={num('M6_VisSVD_MSE')}"
textcol(s, 7.0, 5.15, 6.0, 1.9, [
    ('h', '⑤ 评测 & ⑥ 结论'),
    ('k', mse23),
    ('b', '视觉信号在冷门电影(评分<100)上 RMSE 降低最明显;'),
    ('b', '热门电影协同信号已充足, 视觉边际贡献被稀释。'),
    ('n', '→ 典型的"side-information 只在稀疏区域有效"。'),
])

# =================================================================
# Slide 4: 2.4 LLM 内容
# =================================================================
s = slide_blank()
title_bar(s, '2.4', 'LLM 背景知识增强评分预测')
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 问题动机'),
    ('b', 'ratings 表只有行为信号, 缺少电影的"世界知识": 口碑、主题、奖项、'),
    ('b', '情绪风格。这些信息恰好存在于 LLM 与文本语料里。'),
    ('h', '② 核心思想 (双路径)'),
    ('b', 'A 在线 LLM: DeepSeek/yunwu.ai 返回 online_rating / themes /'),
    ('sub', '   award_level / sentiment, 结构化为数值特征 (带缓存+限流)。'),
    ('b', 'B 本地 MiniLM: 把 name+intro+导演+主演 编码成 384维语义向量,'),
    ('sub', '   作为 API 不可用时的 fallback, 信息互补。'),
    ('h', '③ 公式 (M7 内容残差)'),
    ('f', '  r̂_ui = r̂_ui^{M2+}  +  g_θ( c_i , u_u )'),
    ('fn', 'c_i: 电影内容特征(LLM-KB ⊕ 句向量); u_u: 用户人口学;'),
    ('fn', 'g_θ: LightGBM 学"基线没拟合到的残差", 自动捕捉交叉项。'),
    ('h', '④ 实现步骤'),
    ('sub', 'Step1 DeepSeek 取背景知识 → Step2 MiniLM 句向量 fallback'),
    ('sub', 'Step3 合成电影内容特征矩阵 → Step4 训练 LightGBM 残差器'),
])
img(s, '2_4_feature_importance.png', 7.0, 1.5, 6.0)
topf = R.get('M7_top_features', {})
topstr = ', '.join(list(topf.keys())[:6])
textcol(s, 7.0, 5.2, 6.0, 1.9, [
    ('h', '⑤ 评测 & ⑥ 结论'),
    ('k', f"M7 内容残差模型 ({R.get('M7_model','LightGBM')}) 开放 MSE = {num('M7_LLM_MSE')}"),
    ('sub', f'重要特征 Top: {topstr}'),
    ('b', 'M2_pred(协同基线)主导, occ/age/内容向量 c* 有一定贡献;'),
    ('b', '但基座 M3 训练充分后(0.714), M7 未超过纯协同——'),
    ('b', '说明该数据行为信号已足够强, 外部内容是补充而非主力。'),
])

# =================================================================
# Slide 5: 2.5 对比 + Stacking
# =================================================================
s = slide_blank()
title_bar(s, '2.5', '传统 SVD 与新方案对比 + Stacking 协同')
textcol(s, 0.55, 1.4, 6.3, 5.7, [
    ('h', '① 问题动机'),
    ('b', '四个专家各有所长, 单看一个全量 MSE 看不出差异。要按业务场景拆开,'),
    ('b', '再用"协同"把它们的长处合起来。'),
    ('h', '② 核心思想 + 公式 (Stacking)'),
    ('f', '  r̂^{Stack} = α₀ + αᵀ z ,  z = (M3, M2+, M6, M7)'),
    ('f', '  α = argmin ‖y − α₀1 − Zα‖² + λ‖α‖²   (Ridge)'),
    ('fn', 'z: 四个模型在同一样本上的预测拼成的 4维向量;'),
    ('fn', 'α: Ridge 元学习器学到的全局权重; 为防泄漏, 用训练集再切'),
    ('fn', '一折 meta-val 学 α, 不碰开放测试集。'),
    ('h', '③ 场景实测 (基座训练充分后)'),
    ('sub', '冷门电影 → M6 VisSVD 略优 (视觉 side-info)'),
    ('sub', '稀有 genre / 热门头部 → M3 最优 (协同最强)'),
    ('sub', 'M2+/M7 (人口学/内容) 全场景被压制——'),
    ('sub', '行为协同信号已足够强, 外部信息难再加分。'),
])
img(s, '2_5_stacking.png', 7.05, 1.5, 6.0)
sw = R.get('stack_weights', {})
swstr = '  '.join(f'{k}={v}' for k, v in sw.items())
seg = R.get('segment_mse', [])
seg_lines = [('h', '④⑤ 场景细分 MSE & 结论')]
for sgr in seg[:4]:
    seg_lines.append(('sub', f"{sgr.get('segment','')}: M3={sgr.get('M3 FunkSVD','?')} M6={sgr.get('M6 VisSVD','?')} M7={sgr.get('M7 LLM','?')}"))
seg_lines.append(('k', f"Stacking={num('Stack_MSE')}  SegBlend={num('SegmentBlend_MSE')}  (单模型 M3={num('M3_MSE')})"))
seg_lines.append(('n', '全局 Stacking 反而略差于 M3 单模型(meta 过拟合); 强相关专家'))
seg_lines.append(('n', '集成增益有限 → 见反思页。'))
textcol(s, 7.05, 4.95, 6.0, 2.2, seg_lines)

# =================================================================
# Slide 6: 2.6 ① 异常样本分析 + 画像 (修正版)
# =================================================================
s = slide_blank()
title_bar(s, '2.6 ①', 'SVD 异常样本分析 + 异常用户画像', color=RED)
ar = num('abnormal_rate'); ac = num('abnormal_user_count', num('abnormal_users'))
edu_a = R.get('abnormal_user_student_educator_share'); edu_all = R.get('all_user_student_educator_share')
topg = R.get('abnormal_user_top_genres', [])
occd = list(R.get('abnormal_user_occupation_dist', {}).items())
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 异常定义 (残差阈值法)'),
    ('f', '  e_ui = r_ui − r̂_ui^{M3} ,   异常 ⇔ |e_ui| > τ=1.5'),
    ('f', '  异常用户 = 评分数≥30 用户中, 平均|e_u| 排名前 5%'),
    ('fn', 'e_ui: M3 预测残差; |e_u|: 用户平均绝对残差。'),
    ('b', f'异常样本占比 ≈ {ar}% ;  异常用户 = {ac} 人。'),
    ('h', '② 真实画像 (以 notebook 结论为准, 修正旧标签)'),
    ('b', f'职业: 以 {occd[0][0] if occd else "学生"} 等为主, 学生+教育工作者'),
    ('k', f'  合计占 {round(edu_a*100) if edu_a else "—"}%  (全体仅 {round(edu_all*100) if edu_all else "—"}%) → 明显偏高'),
    ('b', '年龄: 横跨 18-24 / 25-34 / 35-44 多个区间, 并非单一 25-34;'),
    ('b', f'题材: 以 {("、".join(topg[:4])) if topg else "Comedy、Drama"} 为主——'),
    ('k', '  Comedy 各簇均居首, Romance 在偏爱爱情片的簇尤为突出。'),
    ('n', '③ 隐藏因素: 异常源于这批人评分习惯个性化(过严/过松/口味偏窄),'),
    ('n', '   全局协同的 M3 难以拟合, 故残差被放大而被识别出来。'),
])
img(s, '2_6_profile.png', 6.95, 1.45, 6.15)
img(s, '2_6_residual_hist.png', 6.95, 4.55, 3.0)
textcol(s, 10.05, 4.6, 3.05, 2.4, [
    ('h', '画像三联图'),
    ('sub', '左: 职业分布(学生/教育工作者突出)'),
    ('sub', '中: 年龄分布(跨 18-44)'),
    ('sub', '右: 题材偏好(Comedy 主导, Romance 显著)'),
])

# =================================================================
# Slide 7: 2.6 ② 聚类 + 专家切换
# =================================================================
s = slide_blank()
title_bar(s, '2.6 ②', '异常用户聚类画像 + 切换专家模型', color=RED)
textcol(s, 0.55, 1.4, 6.2, 2.2, [
    ('h', '聚类 (KMeans, 行为画像特征)'),
    ('sub', '特征: 评分均值/方差、高分%/低分%、题材熵、偏好年代'),
    ('b', '4 个异常用户簇, 各有不同评分行为 + 职业/题材画像:'),
])
clusters = R.get('abnormal_clusters', [])
cl_lines = []
for cp in clusters[:4]:
    g = '、'.join(cp.get('top3_genres', [])[:3])
    cl_lines.append(('sub', f"C{cp['cluster']} {cp.get('label','')} (n={cp['n']}): 均分{cp['mean_rate']} 高分{int(cp['pct_high']*100)}%/低分{int(cp['pct_low']*100)}% | {str(cp.get('top_occ',''))[:16]} | {cp.get('top_age','')} | {g}"))
textcol(s, 0.55, 3.4, 6.5, 2.3, cl_lines)
es = R.get('abnormal_expert_switch', {})
tab = es.get('table', [])
es_lines = [('h', '切换专家: 异常用户上谁的 MSE 最低?')]
for row in tab:
    es_lines.append(('sub', f"{row['model']}: 异常={row['abnormal_mse']}  正常={row['normal_mse']}"))
if es.get('best_model'):
    es_lines.append(('k', f"→ 本次划分最佳专家: {es['best_model']}"))
es_lines.append(('n', '异常用户误差≈正常用户的 2 倍。基座训练充分后最佳专家为 M6/M3'))
es_lines.append(('n', '(潜因子+视觉), 与 notebook 一致; M2+/M7(人口学/内容)反而更差——'))
es_lines.append(('n', '异常源于个人潜在口味, 而非缺人口学/内容特征。'))
textcol(s, 0.55, 5.35, 6.5, 1.8, es_lines)
img(s, '2_6_clusters.png', 6.95, 1.45, 6.15)
img(s, '2_6_expert_switch.png', 6.95, 4.35, 6.15)

# =================================================================
# Slide 8: 2.6 ③ 异常用户定向优化
# =================================================================
s = slide_blank()
title_bar(s, '2.6 ③', '异常用户驱动的定向优化', color=RED)
aa = R.get('abnormal_adaptive', {})
textcol(s, 0.55, 1.4, 6.4, 5.7, [
    ('h', '① 思路: 不动正常用户, 只对已识别异常用户做局部校准'),
    ('h', '② 固定物品偏置, 重估用户偏置'),
    ('f', '  b_u* = Σ_{i∈I(u)} (r_ui − μ − b_i) / (|I(u)| + λ_u)'),
    ('fn', 'b_i 固定不动, 只用用户自己的残差收缩估计 b_u*, 防止 SVD'),
    ('fn', '对极端用户过拟合。'),
    ('h', '③ 用户簇专属专家融合'),
    ('f', '  r̂_ui = Σ_k w_{g(u),k} · r̂_ui^{(k)}'),
    ('f', '  w_g = softmax( − MSE_g / τ )'),
    ('fn', 'g(u): 用户所属异常簇; w_{g,k}: 在验证集上按各专家误差学到的'),
    ('fn', '簇专属权重; 误差越小权重越大。只作用于同簇异常用户。'),
    ('h', '④ 结果'),
    ('k', f"异常用户测试 MSE: {aa.get('abnormal_user_mse_before','—')} → {aa.get('abnormal_user_mse_after','—')}"),
    ('sub', f"验证集自动选系数: α_fixed={aa.get('alpha_fixed_item_user_bias','—')}, β_cluster={aa.get('alpha_cluster_expert_weight','—')}"),
    ('n', '注: 基座训练充分后, 异常用户误差已基本是不可约噪声, 后处理'),
    ('n', '几乎持平(1.342→1.344)。价值在"识别+分流", 而非全量大跳变(见反思页)。'),
])
img(s, '2_6_abnormal_optimization.png', 7.1, 1.6, 5.9)
cw = aa.get('cluster_weights', {})
cw_lines = [('h', '各簇专家权重示例')]
for cid, info in list(cw.items())[:4]:
    ws = info.get('weights', {})
    cw_lines.append(('sub', f"C{cid} {info.get('label','')}: " + ' '.join(f'{k}={v}' for k, v in ws.items())))
textcol(s, 7.1, 5.05, 5.9, 2.0, cw_lines)

# =================================================================
# Slide 9: 2.7 MOE
# =================================================================
s = slide_blank()
title_bar(s, '2.7', '复杂模型: 分类器 + 多专家系统 (MOE)')
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 问题动机'),
    ('b', 'Stacking 给所有样本同一组权重; 但 2.5/2.6 显示不同场景、不同用户'),
    ('b', '该信的专家不同。MOE 把"挑专家"做成依赖输入的可学习路由。'),
    ('h', '② 公式'),
    ('f', '  r̂_ui = Σ_k π_k(x_ui; θ) · r̂_ui^{(k)} ,  Σ_k π_k = 1'),
    ('f', '  π = softmax( W₂·ReLU(W₁x + b₁) + b₂ )'),
    ('fn', 'x_ui: (u,i) 上下文特征; π_k: 第 k 个专家的 softmax 权重;'),
    ('fn', 'r̂^{(k)}: 第 k 个专家预测。专家参数固定, 只训练 gating。'),
    ('h', '③ 与 Stacking 的关键区别'),
    ('b', 'Stacking = 全局固定权重; MOE = 按样本动态权重 (软路由)。'),
    ('h', '④ Router 输入特征'),
    ('sub', '用户评分数/均值/方差、电影热度、冷启动标志、稀有genre标志、'),
    ('sub', '异常用户簇 one-hot → 让路由"知道"当前样本属于哪种场景。'),
])
img(s, '2_7_moe_compare.png', 7.0, 1.5, 6.1)
rw = R.get('moe_router', {})
rw_lines = [('h', '⑤⑥ MOE 路由权重 & 结论'), ('k', f"MOE 开放 MSE = {num('MOE_MSE')} (4 experts: M3/M2+/M6/M7)")]
for seg_name, weights in list(rw.items())[:3]:
    rw_lines.append(('sub', f"{seg_name}: " + ' '.join(f'{k}={v}' for k, v in weights.items())))
rw_lines.append(('n', 'M3/M6 训练充分后全面占优, router 收敛到几乎只用 M3(≈0.99),'))
rw_lines.append(('n', '故 MOE≈M3 — 当某专家全面更优时, 动态路由会自动归一到它。'))
textcol(s, 7.0, 4.9, 6.1, 2.2, rw_lines)

# =================================================================
# Slide 10: 3.1 BERT/MiniLM
# =================================================================
s = slide_blank()
title_bar(s, '3.1', 'BERT/MiniLM + 微调层 → 电影类型预测', color=TEAL)
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 问题动机'),
    ('b', '期中用 TF-IDF 词袋, 丢了词序与上下文语义 (如反讽)。改用预训练'),
    ('b', 'transformer 的语义表示来做多标签类型预测。'),
    ('h', '② 核心思想 (frozen encoder + 浅头)'),
    ('b', '冻结 MiniLM-L6 (22M, 6层) 抽 384维句向量, 只训练一个分类头。'),
    ('b', '数据仅 ~2k 部电影, 全微调易过拟合, 浅头足够且快。'),
    ('h', '③ 公式'),
    ('f', '  z_i = MiniLM(intro_i) ∈ ℝ³⁸⁴'),
    ('f', '  F(线性): ŷ = σ(W z_i + b)'),
    ('f', '  G(MLP) : ŷ = σ(W₂·ReLU(W₁ z_i) + b)'),
    ('fn', 'σ: sigmoid(逐 genre 独立 0/1); 损失 BCEWithLogitsLoss。'),
    ('h', '④ 评测指标 (多标签)'),
    ('sub', 'Hamming loss、Jaccard、F1-macro、F1-samples、Subset accuracy'),
])
img(s, '3_1_genre_compare.png', 7.0, 1.5, 6.1)
gr = R.get('genre_results', [])
gd = {r['model']: r for r in gr}
def grow(m):
    r = gd.get(m)
    return f"{m}: F1s={r['f1_samples']} Jacc={r['jaccard']} F1m={r['f1_macro']}" if r else m
gl = [('h', '⑤⑥ 结果与结论')]
for m in ['B LR-OVR', 'F MiniLM+Linear', 'G MiniLM+MLP']:
    if m in gd:
        gl.append(('sub', grow(m)))
gl.append(('k', 'MLP 头 > 线性头 > TF-IDF 基线; 语义表示带来稳定提升。'))
gl.append(('n', '期中 TF-IDF (A/B/C) 仅作对照, 不展开。'))
textcol(s, 7.0, 5.0, 6.1, 2.1, gl)

# =================================================================
# Slide 11: 3.2 主题 x 年龄
# =================================================================
s = slide_blank()
title_bar(s, '3.2', '主题电影类 × 年龄相关性建模', color=TEAL)
textcol(s, 0.55, 1.4, 5.7, 5.7, [
    ('h', '① 问题动机'),
    ('b', 'genre 是给定离散标签; 这里用无监督主题模型从 intro 重新抽"语义主题",'),
    ('b', '研究哪些主题的偏好随年龄显著变化。'),
    ('h', '② 公式'),
    ('f', '  LDA: 电影 d 的主题分布 π_d ∈ Δ^{K-1}'),
    ('f', '  区分度: discrim_k = (1/|Age|) Σ_a (r̄_ka − r̄_k)²'),
    ('fn', 'π_dk: 电影 d 属主题 k 的概率; r̄_ka: 年龄段 a 对主题 k 的'),
    ('fn', '加权平均评分。按 discrim_k 自动挑最具年龄区分度的 3 个主题。'),
    ('h', '③ 实现步骤'),
    ('sub', 'Step1 LDA(K=6) 抽主题 → Step2 选 top3 区分度主题'),
    ('sub', 'Step3 主题×年龄 热图/折线 → Step4 交互项 OLS 显著性'),
])
top3 = R.get('top3_topics', {})
tt = [('h', '④⑤⑥ Top 年龄敏感主题 & 结论')]
for t, words in list(top3.items())[:3]:
    tt.append(('sub', f"{t}: {', '.join(words[:5])}"))
tt.append(('k', '各主题平均分都随年龄升高 → 年长用户整体打分更宽容;'))
tt.append(('b', '战争/历史主题的年龄梯度最陡, 都市/爱情主题相对平缓。'))
textcol(s, 0.55, 5.55, 5.7, 1.6, tt)
img(s, '3_2_theme_age.png', 6.5, 1.5, 6.6)

# =================================================================
# Slide 12: 3.3 LLM Embedding
# =================================================================
s = slide_blank()
title_bar(s, '3.3', f"LLM Embedding ({R.get('llm_emb_model','text-embedding-3-small')}) + 微调", color=TEAL)
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '① 问题动机'),
    ('b', '3.1 用通用小模型 MiniLM(384维); 这里换成大模型句嵌入(1536维),'),
    ('b', '语料更广、语义更丰富, 看能否进一步提升。'),
    ('h', '② 核心思想 + 公式'),
    ('f', '  z_i^{LLM} = Embedding_API(intro_i) ∈ ℝ¹⁵³⁶'),
    ('f', '  H: ŷ = σ( MLP₂₅₆(z_i^{LLM}) )'),
    ('fn', '在 1536维嵌入上加 1 个 256 隐层 MLP 头; 维度高 → 用'),
    ('fn', 'Dropout=0.4 + weight decay 抑制过拟合。'),
    ('h', '③ 实现步骤'),
    ('sub', 'Step1 yunwu.ai /v1/embeddings 拉嵌入(缓存+fallback)'),
    ('sub', 'Step2 训练 MLP-256 头 → Step3 自适应阈值 → Step4 对比 3.1'),
    ('h', '④ 评测'),
    ('sub', '与 F/G 同一 train/val/test 划分、同组多标签指标横向对比。'),
])
img(s, '3_3_full_genre.png', 7.0, 1.5, 6.1)
hl = [('h', '⑤⑥ 结果与结论')]
for m in ['G MiniLM+MLP', 'H LLM-emb+MLP']:
    if m in gd:
        r = gd[m]
        hl.append(('sub', f"{m}: F1s={r['f1_samples']} Jacc={r['jaccard']} Hamming={r['hamming']}"))
hl.append(('k', 'H (LLM 1536维 + MLP-256) 在所有指标上最优;'))
hl.append(('b', '高维语义嵌入 + 适当正则, 比 MiniLM 进一步提升类型预测。'))
textcol(s, 7.0, 5.05, 6.1, 2.0, hl)

# =================================================================
# Slide 13: 优化反思 (回答: 为什么提升有限 + 更优方向)
# =================================================================
s = slide_blank()
title_bar(s, '反思', '为什么新增信息对全量 MSE 提升有限? 更优方向在哪?', color=GOLD)
oa = R.get('optimization_analysis', {})
corr = oa.get('mean_pred_correlation', '—')
spread = oa.get('single_model_mse_spread', '—')
tf_ = oa.get('test_fraction', {})
textcol(s, 0.55, 1.35, 6.25, 5.8, [
    ('h', '诊断 (三个根因, 有数据支撑)'),
    ('b', '① 新增信息与协同高度冗余'),
    ('sub', 'M3 与 M6(海报)预测相关性 0.98 → 视觉几乎没加新东西;'),
    ('sub', f"冷门电影仅占测试 {round(tf_.get('cold_movie_lt20',0)*100,1)}%、冷用户 0% —— side-info"),
    ('sub', '只在这些稀疏样本有用, 加权到全量被严重稀释。'),
    ('b', '② 误差已接近不可约噪声地板'),
    ('sub', '同一用户对同类片评分波动大; 训练好的 M3=0.714 已近该数据极限。'),
    ('b', '③ 集成 / 后处理天然增益小'),
    ('sub', f"M2+/M7 被 M3 压制; 全局 Stacking={num('Stack_MSE')} 反而 > M3; 异常用户后处理持平。"),
    ('k', '关键发现: 主瓶颈是基座是否训练充分, 不是缺信息。'),
])
textcol(s, 7.0, 1.35, 6.1, 5.8, [
    ('h', '更能提升准确率的方向 (按预期收益排序)'),
    ('k', '① 先把基座 SVD 训练充分 (最大杠杆, 本次已接入)'),
    ('sub', '原实现每 epoch 仅采样 ~32% 数据 → 欠拟合; 改为全量向量化训练:'),
    ('k', '   M3 MSE 0.823 → 0.714 (↓13.2%); 异常用户 1.69 → 1.34'),
    ('sub', '   一举超过 海报/LLM/Stacking/MOE 全部叠加(~1%)之总和。'),
    ('b', '② 升级矩阵分解模型'),
    ('sub', 'SVD++ (纳入"评过哪些片"的隐式反馈)、timeSVD++ (偏置随时间漂移)。'),
    ('b', '③ 联合建模而非"残差外挂"'),
    ('sub', '因子分解机 FM/DeepFM 把潜因子+人口学+内容放进一个模型, 直接学'),
    ('sub', '交叉项(如"学生×Comedy"), 比 M2+残差再回归更充分利用 side-info。'),
    ('b', '④ 集成要"去相关"'),
    ('sub', '加入 user/item-KNN 等误差结构不同的模型, 集成才有真增益。'),
    ('b', '⑤ 换评测目标'),
    ('sub', '推荐真正在意排序(NDCG/Recall@K), side-info 对排序帮助远大于逐点 MSE。'),
])

# =================================================================
# Slide 14: 期末总结
# =================================================================
s = slide_blank()
title_bar(s, '总结', '期末总结与关键结论')
textcol(s, 0.55, 1.4, 6.2, 5.7, [
    ('h', '评分预测 (Part 2) 全量开放 MSE'),
    ('sub', f"M3 FunkSVD (训练充分)    {num('M3_MSE')}  ← 最佳基座"),
    ('sub', f"M6 VisSVD (含海报)       {num('M6_VisSVD_MSE')}"),
    ('sub', f"M7 LLM / 内容残差        {num('M7_LLM_MSE')}"),
    ('sub', f"Stacking / SegBlend / MOE  {num('Stack_MSE')} / {num('SegmentBlend_MSE')} / {num('MOE_MSE')}"),
    ('h', '类型预测 (Part 3) F1-samples'),
    ('sub', 'TF-IDF基线 → MiniLM+MLP → LLM-emb+MLP 逐级提升,'),
    ('sub', f"最佳 H (LLM-emb+MLP) ≈ {gd.get('H LLM-emb+MLP',{}).get('f1_samples','—')}"),
    ('h', '异常用户'),
    ('sub', f"{num('abnormal_user_count', num('abnormal_users'))} 名异常用户, 学生/教育工作者居多, Comedy/Romance 偏好;"),
    ('sub', f"最佳专家 {R.get('abnormal_expert_switch',{}).get('best_model','M3/M6')}, 切换专家比统一模型更合理。"),
])
textcol(s, 7.0, 1.4, 6.1, 5.7, [
    ('h', '核心 Takeaways'),
    ('b', '① Side-information 只在稀疏区域(冷门电影/稀有题材/冷用户)有价值,'),
    ('sub', '   全量指标提升有限是结构性的, 不是方法写错了。'),
    ('b', '② 异常用户有真实的人群结构(学生/教育工作者)与题材偏好(Comedy/'),
    ('sub', '   Romance), 应"识别 + 分流到合适专家", 而非全量硬调。'),
    ('b', '③ MOE 的按样本动态路由比 Stacking 全局权重更贴合多场景。'),
    ('b', '④ 类型预测: 语义嵌入(尤其 LLM 高维) + 浅头是小数据多标签最佳实践。'),
    ('b', '⑤ LLM 适合"一次嵌入长期复用", 而非每次推理在线调用。'),
    ('k', '⑥ 已验证: 训练充分的基座 SVD 把 M3 0.82→0.71, 远超所有 side-info 叠加。'),
])

# =================================================================
# Slide 15: 谢谢
# =================================================================
s = slide_blank()
band = s.shapes.add_shape(1, Inches(0), Inches(2.7), Inches(13.333), Inches(1.5))
band.fill.solid(); band.fill.fore_color.rgb = BG2; band.line.fill.background()
t = s.shapes.add_textbox(Inches(1), Inches(2.85), Inches(11.3), Inches(1.2))
p = t.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = '谢谢！'
r.font.size = Pt(48); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
t2 = s.shapes.add_textbox(Inches(1), Inches(4.25), Inches(11.3), Inches(0.6))
p2 = t2.text_frame.paragraphs[0]; p2.alignment = PP_ALIGN.CENTER
r2 = p2.add_run(); r2.text = '蒋名仪   2500010771'
r2.font.size = Pt(22); r2.font.color.rgb = BLUE; r2.font.name = FONT

# =================================================================
def _save(prs, out):
    try:
        prs.save(out)
        return out
    except PermissionError:
        base, ext = os.path.splitext(out)
        alt = base + '_new' + ext
        prs.save(alt)
        print(f"[警告] 原文件被占用(PowerPoint 打开中?): {os.path.basename(out)}")
        print(f"       已改存为: {os.path.basename(alt)} — 请关闭 PowerPoint 后删除旧文件并改名。")
        return alt

saved = _save(prs, OUT)
print(f"PPT saved -> {saved}")
print(f"Total slides: {len(prs.slides)}")

# ---- 自检: 重新读取验证页数与文件大小 ----
chk = Presentation(saved)
size_kb = os.path.getsize(saved) / 1024
print(f"[verify] reopened OK, slides={len(chk.slides)}, size={size_kb:.0f} KB")
miss = []
for nm in ['2_3_cold_movie.png', '2_4_feature_importance.png', '2_5_stacking.png',
           '2_6_profile.png', '2_6_residual_hist.png', '2_6_clusters.png',
           '2_6_expert_switch.png', '2_6_abnormal_optimization.png', '2_7_moe_compare.png',
           '3_1_genre_compare.png', '3_2_theme_age.png', '3_3_full_genre.png']:
    if not os.path.exists(os.path.join(FIG, nm)):
        miss.append(nm)
print(f"[verify] missing figures: {miss if miss else 'none'}")
