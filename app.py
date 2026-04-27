import streamlit as st

st.set_page_config(page_title="TikTok Product Analyzer", layout="centered")

st.title("🔥 TikTok Product Analyzer")
st.write("Analisa apakah produk layak dijual atau tidak")

# Input user
produk = st.text_input("Nama Produk")
view = st.number_input("Jumlah View Video", min_value=0)
komentar = st.slider("Minat Komentar (1-10)", 1, 10)
harga = st.number_input("Harga Produk (Rp)", min_value=0)

# Fungsi analisa
def analisa(view, komentar, harga):
    skor = 0
    
    if view > 100000:
        skor += 2
    elif view > 50000:
        skor += 1
        
    if komentar >= 6:
        skor += 2
    elif komentar >= 3:
        skor += 1
        
    if harga < 100000:
        skor += 1

    return skor

# Tombol analisa
if st.button("Analisa Sekarang"):
    skor = analisa(view, komentar, harga)

    if skor >= 4:
        st.success("🔥 Produk Berpotensi Viral!")
    elif skor >= 2:
        st.warning("⚠️ Lumayan, perlu testing")
    else:
        st.error("❌ Kurang direkomendasikan")

    st.subheader(f"Skor: {skor}/5")

    # Insight tambahan
    if view < 50000:
        st.write("👉 View masih rendah, cari produk lain atau konten lebih bagus")
    if komentar < 5:
        st.write("👉 Engagement kurang, kurang menarik minat beli")
    if harga > 100000:
        st.write("👉 Harga agak tinggi untuk impulse buying")
