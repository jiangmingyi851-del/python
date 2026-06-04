
# ====================== 逆向策略可视化（分批次下载 + 向量化 + 维度修复） ======================
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

# 解决中文/负号显示
plt.rcParams["font.family"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ====================== 1. 分批次下载函数 ======================
def download_batch(ticker, start_date, end_date, retry=3):
    for attempt in range(1, retry+1):
        try:
            data = yf.download(
                ticker, start=start_date, end=end_date,
                interval="1d", auto_adjust=False, progress=False, threads=False
            )
            if not data.empty:
                return data
            else:
                print(f"   ⚠️ {start_date.date()} ~ {end_date.date()} 数据为空")
                return pd.DataFrame()
        except Exception as e:
            print(f"   ❌ 下载失败 (尝试 {attempt}/{retry}): {e}")
            if attempt < retry:
                time.sleep(5 * attempt)
    return pd.DataFrame()

def download_by_chunks(ticker, years=5, chunk_months=6, sleep_sec=10):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365*years)
    
    chunks = []
    current_start = start_date
    while current_start < end_date:
        current_end = min(current_start + timedelta(days=30*chunk_months), end_date)
        print(f"📥 下载 {ticker} 数据: {current_start.date()} -> {current_end.date()}")
        
        df_chunk = download_batch(ticker, current_start, current_end)
        if not df_chunk.empty:
            chunks.append(df_chunk)
        
        print(f"⏳ 等待 {sleep_sec} 秒后继续...")
        time.sleep(sleep_sec)
        current_start = current_end
    
    if not chunks:
        raise ValueError("未下载到任何数据")
    
    full_data = pd.concat(chunks)
    full_data = full_data[~full_data.index.duplicated(keep='first')].sort_index()
    print(f"✅ 数据合并完成，总天数: {len(full_data)}")
    return full_data

# ====================== 2. 核心参数 ======================
ticker = "SPY"
lookback_window = 20
trade_cost = 0.0003
over_buy_threshold = 0.05
over_sell_threshold = -0.05

# ====================== 3. 分批次下载数据 ======================
print("开始分批次下载（每块后等待10秒，避免限流）...")
data = download_by_chunks(ticker, years=5, chunk_months=6, sleep_sec=10)

# 确保收盘价为 Series（一维）
price = data['Close'].squeeze()
daily_ret = price.pct_change().dropna()

# ====================== 4. 向量化策略计算（维度完全一维） ======================
rolling_sum = daily_ret.rolling(window=lookback_window).sum()
signal = rolling_sum.shift(1)   # 昨日信号 -> 今日仓位

# 有效索引范围
valid_idx = signal.index[lookback_window+1:]

# 对齐信号和收益率（都是 Series）
signal_aligned = signal.loc[valid_idx]
ret_aligned = daily_ret.loc[valid_idx]

# 确保为一维数组（如果上述步骤返回的是 DataFrame，则取第0列）
if isinstance(signal_aligned, pd.DataFrame):
    signal_aligned = signal_aligned.iloc[:, 0]
if isinstance(ret_aligned, pd.DataFrame):
    ret_aligned = ret_aligned.iloc[:, 0]

# 生成仓位：1=做多，-1=做空，0=空仓
position = np.where(signal_aligned < over_sell_threshold, 1,
                    np.where(signal_aligned > over_buy_threshold, -1, 0))

# 扣除手续费：只要当天有仓位（非0）就扣一次
cost = trade_cost * (position != 0).astype(float)

# 策略日收益 = 仓位 * 当日收益 - 手续费
strategy_ret = position * ret_aligned.values - cost
benchmark_ret = ret_aligned.values

# 转为 Series（保持索引）
strategy_ret = pd.Series(strategy_ret, index=valid_idx)
benchmark_ret = pd.Series(benchmark_ret, index=valid_idx)

# ====================== 5. 净值与回撤 ======================
strategy_nav = (1 + strategy_ret).cumprod()
benchmark_nav = (1 + benchmark_ret).cumprod()

def calc_drawdown(nav):
    roll_max = nav.cummax()
    dd = (nav - roll_max) / roll_max
    return dd, dd.min()

strategy_dd, strategy_maxdd = calc_drawdown(strategy_nav)
benchmark_dd, benchmark_maxdd = calc_drawdown(benchmark_nav)

# ====================== 6. 可视化 ======================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

ax1.plot(strategy_nav, linewidth=2.5, color="#FF4500", label="逆向策略（无前视偏差）")
ax1.plot(benchmark_nav, linewidth=2.5, color="#1E90FF", label=f"{ticker} 基准")
ax1.set_title("5年期 逆向策略 vs 基准 净值对比", fontsize=16)
ax1.set_ylabel("累计净值", fontsize=12)
ax1.legend()
ax1.grid(alpha=0.3)

ax2.plot(strategy_dd, linewidth=2, color="#FF4500", label="策略回撤")
ax2.plot(benchmark_dd, linewidth=2, color="#1E90FF", label="基准回撤")
ax2.set_title("最大回撤对比", fontsize=16)
ax2.set_ylabel("回撤比例", fontsize=12)
ax2.set_xlabel("日期", fontsize=12)
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# ====================== 7. 绩效输出 ======================
print("\n" + "="*55)
print("        逆向策略绩效指标（分批次下载 + 向量化）")
print("="*55)
print(f"逆向策略累计收益：{(strategy_nav.iloc[-1]-1)*100:.2f}%")
print(f"{ticker} 基准收益：{(benchmark_nav.iloc[-1]-1)*100:.2f}%")
print(f"逆向策略年化波动率：{strategy_ret.std() * np.sqrt(252):.2%}")
print(f"基准年化波动率：{benchmark_ret.std() * np.sqrt(252):.2%}")
print(f"逆向策略最大回撤：{strategy_maxdd*100:.2f}%")
print(f"基准最大回撤：{benchmark_maxdd*100:.2f}%")
print("="*55)