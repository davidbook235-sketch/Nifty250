"""
Nifty 250 Swing Trading Scanner
Strategy: EMA Trend (21/50/200) + RSI Momentum + Volume Surge + Supertrend
Deploy : Streamlit Cloud (via GitHub)
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

st.set_page_config(page_title="Nifty 250 Swing Scanner", page_icon="📈", layout="wide")

# =====================================================================
# 1. NIFTY LARGEMIDCAP 250 SYMBOLS (NSE)
# =====================================================================
NIFTY250 = [
    "ABB.NS","ACC.NS","ADANIENSOL.NS","ADANIENT.NS","ADANIGREEN.NS","ADANIPORTS.NS",
    "ABCAPITAL.NS","ABFRL.NS","ALKEM.NS","AMBUJACEM.NS","APLAPOLLO.NS","APOLLOHOSP.NS",
    "APOLLOTYRE.NS","ASHOKLEY.NS","ASIANPAINT.NS","ASTRAL.NS","ATGL.NS","AUBANK.NS",
    "AUROPHARMA.NS","AXISBANK.NS","BAJAJ-AUTO.NS","BAJAJFINSV.NS","BAJFINANCE.NS",
    "BALKRISIND.NS","BALRAMCHIN.NS","BANDHANBNK.NS","BANKBARODA.NS","BATAINDIA.NS",
    "BEL.NS","BERGEPAINT.NS","BHARATFORG.NS","BHARTIARTL.NS","BHEL.NS","BIOCON.NS",
    "BOSCHLTD.NS","BPCL.NS","BRITANNIA.NS","BSOFT.NS","CANBK.NS","CANFINHOME.NS",
    "CHAMBLFERT.NS","CHOLAFIN.NS","CIPLA.NS","COALINDIA.NS","COFORGE.NS","COLPAL.NS",
    "CONCOR.NS","COROMANDEL.NS","CROMPTON.NS","CUMMINSIND.NS","DABUR.NS","DALBHARAT.NS",
    "DEEPAKNTR.NS","DIVISLAB.NS","DIXON.NS","DLF.NS","DMART.NS","DRREDDY.NS",
    "EICHERMOT.NS","ESCORTS.NS","EXIDEIND.NS","FEDERALBNK.NS","GAIL.NS","GLENMARK.NS",
    "GMRINFRA.NS","GNFC.NS","GODREJCP.NS","GODREJPROP.NS","GRANULES.NS","GRASIM.NS",
    "GUJGASLTD.NS","HAL.NS","HAVELLS.NS","HCLTECH.NS","HDFCAMC.NS","HDFCBANK.NS",
    "HDFCLIFE.NS","HEROMOTOCO.NS","HINDALCO.NS","HINDCOPPER.NS","HINDPETRO.NS",
    "HINDUNILVR.NS","ICICIBANK.NS","ICICIGI.NS","ICICIPRULI.NS","IDFCFIRSTB.NS",
    "IEX.NS","IGL.NS","INDHOTEL.NS","INDIAMART.NS","INDIANB.NS","INDIGO.NS",
    "INDUSINDBK.NS","INDUSTOWER.NS","INFY.NS","IOC.NS","IPCALAB.NS","IRCTC.NS",
    "ITC.NS","JINDALSTEL.NS","JKCEMENT.NS","JSWENERGY.NS","JSWSTEEL.NS","JUBLFOOD.NS",
    "KOTAKBANK.NS","KPITTECH.NS","LT.NS","LALPATHLAB.NS","LAURUSLABS.NS","LICHSGFIN.NS",
    "LTIM.NS","LTTS.NS","LUPIN.NS","M&M.NS","M&MFIN.NS","MANAPPURAM.NS","MARICO.NS",
    "MARUTI.NS","MCX.NS","METROPOLIS.NS","MFSL.NS","MGL.NS","MOTHERSON.NS","MPHASIS.NS",
    "MRF.NS","MUTHOOTFIN.NS","NAVINFLUOR.NS","NESTLEIND.NS","NHPC.NS","NMDC.NS",
    "NTPC.NS","OBEROIRLTY.NS","OFSS.NS","ONGC.NS","PAGEIND.NS","PEL.NS","PERSISTENT.NS",
    "PETRONET.NS","PFC.NS","PIDILITIND.NS","PIIND.NS","PNB.NS","POLYCAB.NS",
    "POWERGRID.NS","PVRINOX.NS","RAMCOCEM.NS","RBLBANK.NS","RECLTD.NS","RELIANCE.NS",
    "SBICARD.NS","SBILIFE.NS","SBIN.NS","SHREECEM.NS","SHRIRAMFIN.NS","SIEMENS.NS",
    "SRF.NS","SUNPHARMA.NS","SUNTV.NS","SYNGENE.NS","TATACHEM.NS","TATACOMM.NS",
    "TATACONSUM.NS","TATAMOTORS.NS","TATAPOWER.NS","TATASTEEL.NS","TCS.NS","TECHM.NS",
    "TITAN.NS","TORNTPHARM.NS","TORNTPOWER.NS","TRENT.NS","TVSMOTOR.NS","UBL.NS",
    "ULTRACEMCO.NS","UNIONBANK.NS","UNITDSPR.NS","UPL.NS","VEDL.NS","VOLTAS.NS",
    "WIPRO.NS","ZOMATO.NS","ZYDUSLIFE.NS","AARTIIND.NS","AEGISLOG.NS","AFFLE.NS",
    "ANGELONE.NS","APLLTD.NS","ATUL.NS","BSE.NS","CAMS.NS","CASTROLIND.NS","CEATLTD.NS",
    "CESC.NS","CHOLAHLDNG.NS","COCHINSHIP.NS","CREDITACC.NS","CYIENT.NS","DELHIVERY.NS",
    "DEVYANI.NS","EMAMILTD.NS","ENDURANCE.NS","FACT.NS","FINCABLES.NS","FSL.NS",
    "GILLETTE.NS","GLAXO.NS","GODREJIND.NS","HAPPSTMNDS.NS","HONAUT.NS","HUDCO.NS",
    "IDEA.NS","INDIGOPNTS.NS","INOXWIND.NS","IRB.NS","IRFC.NS","JBCHEPHARM.NS",
    "JSL.NS","JYOTHYLAB.NS","KAJARIACER.NS","KANSAINER.NS","KEC.NS","KIMS.NS",
    "KPRMILL.NS","L&TFH.NS","LATENTVIEW.NS","LICI.NS","LINDEINDIA.NS","LLOYDSME.NS",
    "MAHABANK.NS","MASTEK.NS","MAXHEALTH.NS","MEDANTA.NS","MINDACORP.NS","NATCOPHARM.NS",
    "NAUKRI.NS","NAVA.NS","NLCINDIA.NS","OLECTRA.NS","PATANJALI.NS","PFIZER.NS",
    "PHOENIXLTD.NS","PNBHOUSING.NS","PRESTIGE.NS","RADICO.NS","RAIN.NS","RAJESHEXPO.NS",
    "RCF.NS","REDINGTON.NS","SCHAEFFLER.NS","SJVN.NS","SKFINDIA.NS","SONACOMS.NS",
    "STARHEALTH.NS","SUMICHEM.NS","SUNDARMFIN.NS","SUPREMEIND.NS","TATACHEM.NS",
    "TATAELXSI.NS","TATATECH.NS","TIINDIA.NS","TIMKEN.NS","TRIDENT.NS","TTKPRESTIG.NS",
    "UCOBANK.NS","UJJIVANSFB.NS","VINATIORGA.NS","WHIRLPOOL.NS","YESBANK.NS","ZEEL.NS"
]

# =====================================================================
# 2. TECHNICAL INDICATORS
# =====================================================================
def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0.0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def atr(df, period=14):
    h, l, c = df['High'], df['Low'], df['Close']
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def supertrend(df, period=10, multiplier=3):
    hl2 = (df['High'] + df['Low']) / 2
    a = atr(df, period)
    ub = hl2 + multiplier * a
    lb = hl2 - multiplier * a
    fu, fl = ub.copy(), lb.copy()
    for i in range(1, len(df)):
        fu.iloc[i] = ub.iloc[i] if (ub.iloc[i] < fu.iloc[i-1] or df['Close'].iloc[i-1] > fu.iloc[i-1]) else fu.iloc[i-1]
        fl.iloc[i] = lb.iloc[i] if (lb.iloc[i] > fl.iloc[i-1] or df['Close'].iloc[i-1] < fl.iloc[i-1]) else fl.iloc[i-1]
    st = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(index=df.index, dtype=int)
    st.iloc[0], direction.iloc[0] = fu.iloc[0], -1
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > fu.iloc[i-1]:
            direction.iloc[i] = 1
        elif df['Close'].iloc[i] < fl.iloc[i-1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i-1]
        st.iloc[i] = fl.iloc[i] if direction.iloc[i] == 1 else fu.iloc[i]
    return st, direction

# =====================================================================
# 3. DATA FETCH + CACHE
# =====================================================================
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_one(symbol, period="1y"):
    try:
        df = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=False)
        if df is None or len(df) < 210:
            return None
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        return df
    except Exception:
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_nifty(period="1y"):
    return yf.Ticker("^NSEI").history(period=period, interval="1d")['Close']

def batch_fetch(symbols, progress_cb=None):
    out = {}
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(fetch_one, s): s for s in symbols}
        for i, fut in enumerate(as_completed(futures)):
            s = futures[fut]
            df = fut.result()
            if df is not None:
                out[s] = df
            if progress_cb:
                progress_cb((i + 1) / len(symbols))
    return out

# =====================================================================
# 4. STRATEGY SCORING ENGINE
# =====================================================================
def score_stock(symbol, df, nifty_close):
    df = df.copy()
    df['EMA21'] = ema(df['Close'], 21)
    df['EMA50'] = ema(df['Close'], 50)
    df['EMA200'] = ema(df['Close'], 200)
    df['RSI'] = rsi(df['Close'], 14)
    df['VolAvg5'] = df['Volume'].rolling(5).mean()
    df['ATR'] = atr(df, 14)
    _, df['ST_Dir'] = supertrend(df, 10, 3)

    last = df.iloc[-1]
    price = float(last['Close'])
    if np.isnan(last['EMA200']) or np.isnan(last['ATR']) or last['VolAvg5'] == 0:
        return None

    # --- 6 Core Conditions ---
    c1 = price > last['EMA21']
    c2 = price > last['EMA50']
    c3 = price > last['EMA200']
    c4 = 45 <= last['RSI'] <= 65
    c5 = last['Volume'] > 1.25 * last['VolAvg5']
    c6 = last['ST_Dir'] == 1
    score = sum([c1, c2, c3, c4, c5, c6])

    # --- Relative Strength vs Nifty (3-month) ---
    try:
        stock_3m = (price / df['Close'].iloc[-63] - 1) * 100
        nifty_3m = (float(nifty_close.iloc[-1]) / float(nifty_close.iloc[-63]) - 1) * 100
        rs = round(stock_3m - nifty_3m, 2)
    except Exception:
        rs = 0.0

    # --- Risk / Targets ---
    swing_low_10 = float(df['Low'].iloc[-10:].min())
    sl_atr = price - 2 * float(last['ATR'])
    stop_loss = round(max(swing_low_10, sl_atr), 2)
    risk = price - stop_loss
    if risk <= 0:
        return None
    t1 = round(price + 1.5 * risk, 2)
    t2 = round(price + 3.0 * risk, 2)
    rr = round((t1 - price) / risk, 2)

    # --- 52-week proximity ---
    hi52 = float(df['High'].iloc[-252:].max())
    from_high = round((price / hi52 - 1) * 100, 2)

    return {
        "Symbol": symbol.replace(".NS", ""),
        "Price": round(price, 2),
        "Score": score,
        "RSI": round(float(last['RSI']), 1),
        "Vol×5d": round(float(last['Volume'] / last['VolAvg5']), 2),
        "ST": "🟢 Bull" if c6 else "🔴 Bear",
        "RS_3M": rs,
        "From52W_High%": from_high,
        "Entry": round(price, 2),
        "SL": stop_loss,
        "T1": t1,
        "T2": t2,
        "R:R": rr,
        "EMA21✓": "✅" if c1 else "❌",
        "EMA50✓": "✅" if c2 else "❌",
        "EMA200✓": "✅" if c3 else "❌",
        "_df": df,
    }

# =====================================================================
# 5. UI
# =====================================================================
st.title("📈 Nifty 250 Swing Trading Scanner")
st.caption(
    "**Strategy:** Price > EMA21/50/200 + RSI 45–65 + Volume Surge (1.25×) + Supertrend Bullish  "
    "→ **Score ≥ 4** = Trade Signal"
)

with st.sidebar:
    st.header("⚙️ Settings")
    min_score = st.slider("Minimum Score", 3, 6, 4)
    require_ema200 = st.checkbox("Require Price > EMA200 (Strict)", value=True)
    top_n = st.slider("Show Top N", 10, 100, 30)
    force_refresh = st.button("🔄 Force Refresh Data")

if force_refresh:
    st.cache_data.clear()

# --- Fetch data ---
with st.spinner("📥 Nifty 250 data fetch हो रहा है... (पहली बार 1-2 मिनट)"):
    progress = st.progress(0.0, text="Loading...")
    stock_data = batch_fetch(NIFTY250, progress_cb=lambda p: progress.progress(p, text=f"Fetched {int(p*len(NIFTY250))}/{len(NIFTY250)}"))
    nifty_close = fetch_nifty()
    progress.empty()

# --- Analyze ---
rows = []
for sym, df in stock_data.items():
    res = score_stock(sym, df, nifty_close)
    if res:
        if require_ema200 and res["EMA200✓"] != "✅":
            continue
        if res["Score"] >= min_score:
            rows.append(res)

if not rows:
    st.warning("⚠️ कोई stock filter पास नहीं कर रहा। Minimum Score कम करें या EMA200 filter बंद करें।")
    st.stop()

results = pd.DataFrame(rows).sort_values(
    ["Score", "RS_3M"], ascending=[False, False]
).reset_index(drop=True)
results.index += 1

# --- Top metrics ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Signals Found", len(results))
c2.metric("Score = 6 (Perfect)", int((results["Score"] == 6).sum()))
c3.metric("ST Bullish", int((results["ST"] == "🟢 Bull").sum()))
c4.metric("Updated", datetime.now().strftime("%d-%b %H:%M"))

st.markdown("---")

# --- Main table ---
display_cols = [
    "Symbol", "Price", "Score", "RSI", "Vol×5d", "ST", "RS_3M",
    "EMA21✓", "EMA50✓", "EMA200✓", "From52W_High%",
    "Entry", "SL", "T1", "T2", "R:R"
]
st.subheader(f"🎯 Top {min(top_n, len(results))} Swing Trade Candidates")
st.dataframe(
    results[display_cols].head(top_n),
    use_container_width=True,
    height=600,
    column_config={
        "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=6),
        "R:R": st.column_config.NumberColumn("R:R", format="%.2f"),
        "RS_3M": st.column_config.NumberColumn("RS vs Nifty (3M %)", format="%.2f"),
        "From52W_High%": st.column_config.NumberColumn("52W High से %", format="%.2f"),
    }
)

# --- CSV download ---
csv = results[display_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Signals CSV (Next Day Watchlist)",
    csv, f"nifty250_swing_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    "text/csv"
)

# --- Detail chart view ---
st.markdown("---")
st.subheader("📊 Stock Chart & Levels")

sel = st.selectbox("Stock चुनें", results["Symbol"].tolist())
row = results[results["Symbol"] == sel].iloc[0]
df = row["_df"]

fig = make_subplots(
    rows=3, cols=1, shared_xaxes=True,
    row_heights=[0.6, 0.2, 0.2], vertical_spacing=0.03,
    subplot_titles=(f"{sel} — Daily", "RSI (14)", "Volume")
)

fig.add_trace(go.Candlestick(
    x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
    name="Price", increasing_line_color='#26a69a', decreasing_line_color='#ef5350'
), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['EMA21'], name="EMA21", line=dict(color='#ff9800', width=1.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name="EMA50", line=dict(color='#2196f3', width=1.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['EMA200'], name="EMA200", line=dict(color='#9c27b0', width=1.5)), row=1, col=1)

# Entry/SL/T1/T2 lines (last 90 days only)
last_90 = df.index[-90:]
for level, color, label in [
    (row["Entry"], "#000000", "Entry"),
    (row["SL"], "#ef5350", "SL"),
    (row["T1"], "#4caf50", "T1"),
    (row["T2"], "#2e7d32", "T2"),
]:
    fig.add_trace(go.Scatter(
        x=last_90, y=[level] * len(last_90), mode="lines",
        name=label, line=dict(color=color, dash="dash", width=1.2)
    ), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name="RSI", line=dict(color='#673ab7')), row=2, col=1)
fig.add_hline(y=65, line_dash="dot", line_color="red", row=2, col=1)
fig.add_hline(y=45, line_dash="dot", line_color="green", row=2, col=1)

colors = ['#26a69a' if c >= o else '#ef5350' for o, c in zip(df['Open'], df['Close'])]
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name="Vol", marker_color=colors), row=3, col=1)

fig.update_layout(
    height=800, showlegend=True, xaxis_rangeslider_visible=False,
    template="plotly_white", margin=dict(l=10, r=10, t=40, b=10)
)
st.plotly_chart(fig, use_container_width=True)

# --- Trade Plan Card ---
st.markdown("### 📋 Trade Plan")
p1, p2, p3, p4, p5 = st.columns(5)
p1.metric("Entry", f"₹{row['Entry']}")
p2.metric("Stop Loss", f"₹{row['SL']}", delta=f"-{(row['Entry']-row['SL'])/row['Entry']*100:.1f}%")
p3.metric("Target 1", f"₹{row['T1']}", delta=f"+{(row['T1']-row['Entry'])/row['Entry']*100:.1f}%")
p4.metric("Target 2", f"₹{row['T2']}", delta=f"+{(row['T2']-row['Entry'])/row['Entry']*100:.1f}%")
p5.metric("R:R", f"1:{row['R:R']}")

st.info(
    f"**Position Sizing:** मान लीजिए capital ₹1,00,000 है और risk 1% = ₹1,000. "
    f"Entry-SL = ₹{row['Entry']-row['SL']:.2f} → **Quantity = {int(1000/(row['Entry']-row['SL']))} shares**"
)

st.markdown("---")
st.caption("⚠️ Disclaimer: यह educational tool है। Live trades से पहले अपना backtest और risk management ज़रूर करें।")
