import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from datetime import date

st.set_page_config(page_title="Riset Produk TikTok", layout="wide")

st.title("🔥 Riset Produk TikTok + Google Trends + Viral Score")

# ================= INPUT =================
keywords = st.text_input(
    "Masukkan keyword (pisahkan koma):",
    "kipas leher, blender portable"
)

# Mode waktu
mode_waktu = st.radio(
    "Pilih Mode Waktu:",
    ["Cepat (Preset)", "Custom Tanggal"]
)

if mode_waktu == "Cepat (Preset)":
    timeframe = st.selectbox(
        "Pilih rentang waktu:",
        ["now 7-d", "today 1-m", "today 3-m", "today 12-m"]
    )
else:
    start_date = st.date_input("Tanggal mulai", date(2024, 1, 1))
    end_date = st.date_input("Tanggal akhir", date.today())
    timeframe = f"{start_date} {end_date}"

# ================= FUNCTION =================
def analisa_tren(series):
    first = series.iloc[0]
    last = series.iloc[-1]

    if last > first * 1.2:
        return "🔥 NAIK"
    elif last < first * 0.8:
        return "⚠️ TURUN"
    else:
        return "😐 STABIL"

def hitung_viral_score(series):
    max_val = series.max()
    mean_val = series.mean()

    growth = (series.iloc[-1] - series.iloc[0]) / (series.iloc[0] + 1)
    spike = max_val - mean_val

    score = (growth * 50) + (spike * 0.5)

    score = max(0, min(100, score))
    return round(score, 2)

# ================= BUTTON =================
if st.button("🔍 MULAI RISET"):
    try:
        pytrends = TrendReq(hl='id-ID', tz=360)

        kw_list = [k.strip() for k in keywords.split(",")]

        pytrends.build_payload(kw_list, timeframe=timeframe, geo='ID')

        data = pytrends.interest_over_time()

        if not data.empty:
            st.subheader("📈 Grafik Tren")
            st.line_chart(data[kw_list])

            st.subheader("📊 Analisa + Viral Score")

            result = []
            for kw in kw_list:
                status = analisa_tren(data[kw])
                score = hitung_viral_score(data[kw])

                result.append({
                    "Keyword": kw,
                    "Status": status,
                    "Viral Score": score
                })

            df = pd.DataFrame(result).sort_values(by="Viral Score", ascending=False)
            st.dataframe(df)

        # ================= RELATED =================
        st.subheader("🔑 Keyword Viral (Rising)")
        related = pytrends.related_queries()

        for kw in kw_list:
            st.markdown(f"### {kw}")

            if kw in related:
                rising = related[kw]['rising']
                if rising is not None:
                    st.dataframe(rising.head(5))

    except Exception as e:
        st.error(f"Error: {e}")
