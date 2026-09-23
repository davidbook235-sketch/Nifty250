# 📈 Nifty 250 Swing Trading Scanner

Streamlit app जो Nifty LargeMidcap 250 stocks को scan करता है और 6-point strategy पर swing trade signals देता है।

## 🎯 Strategy
- Price > EMA 21 ✓
- Price > EMA 50 ✓
- Price > EMA 200 ✓
- RSI (14) between 45–65 ✓
- Volume > 1.25 × 5-day avg ✓
- Supertrend (10,3) Bullish ✓

**Score ≥ 4 = Trade Signal**

हर signal के साथ: Entry, Stop Loss (ATR-based), Target 1 (1.5R), Target 2 (3R)

## 🚀 Deploy on Streamlit Cloud (Free)

### Step 1 — GitHub पर push करें
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/nifty250-swing-scanner.git
git push -u origin main
