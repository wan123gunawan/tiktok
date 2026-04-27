import streamlit as st

st.set_page_config(page_title="TikTok Product Analyzer", layout="centered")

st.title("🔥 TikTok Product Analyzer")
st.write("Analisa apakah produk layak dijual atau tidak")

# =========================
# INPUT PRODUK
# =========================
st.markdown("### 📦 Input Produk")

produk = st.text_input("Nama Produk")
view = st.number_input("Jumlah View Video", min_value=0)
komentar = st.number_input("Jumlah Komentar", min_value=0)
harga = st.number_input("Harga Produk (Rp)", min_value=0)

# =========================
# SETTING FILTER
# =========================
st.markdown("### ⚙️ Setting Filter")

min_view = st.number_input("Minimal View", value=50000)

min_komentar = st.number_input("Minimal Komentar", value=50)
max_komentar = st.number_input("Maksimal Komentar", value=10000)

min_harga = st.number_input("Harga Minimal (Rp)", value=10000)
max_harga = st.number_input("Harga Maksimal (Rp)", value=100000)

# =========================
# FUNGSI ANALISA
# =========================
def analisa(view, komentar, harga):
    skor = 0
    gagal = []

    # VIEW
    if view >= min_view:
        skor += 2
    else:
        gagal.append("View kurang")

    # KOMENTAR MIN & MAX
    if komentar < min_komentar:
        gagal.append("Komentar terlalu sedikit")
    elif komentar > max_komentar:
        gagal.append("Komentar terlalu banyak (kemungkinan tidak natural)")
    else:
        skor += 2

    # HARGA RANGE
    if harga < min_harga:
        gagal.append("Harga terlalu murah (margin kecil)")
    elif harga > max_harga:
        gagal.append("Harga terlalu mahal")
    else:
        skor += 1

    return skor, gagal

# =========================
# TOMBOL ANALISA
# =========================
if st.button("Analisa Sekarang"):
    skor, gagal = analisa(view, komentar, harga)

    # HASIL
    if skor >= 4:
        st.success("🔥 Produk Berpotensi Viral!")
    elif skor >= 2:
        st.warning("⚠️ Lumayan, perlu testing")
    else:
        st.error("❌ Tidak memenuhi kriteria")

    st.subheader(f"Skor: {skor}/5")

    # MASALAH
    if gagal:
        st.markdown("### ❌ Masalah:")
        for g in gagal:
            st.write(f"- {g}")

    # ANALISA KOMENTAR
    st.markdown("### 💬 Analisa Komentar:")

    if komentar < min_komentar:
        st.write("❌ Terlalu sedikit → minat beli rendah")
    elif komentar > max_komentar:
        st.write("⚠️ Terlalu banyak → bisa jadi spam / tidak natural")
    else:
        st.write("✅ Ideal → tanda produk diminati")

    # REKOMENDASI
    st.markdown("### 💡 Rekomendasi:")

    if skor >= 4:
        st.write("👉 GAS! Langsung jual + bikin banyak konten")
    elif skor >= 2:
        st.write("👉 Test dulu dengan beberapa variasi video")
    else:
        st.write("👉 SKIP, cari produk lain")
