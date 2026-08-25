import streamlit as st

# Inisialisasi daftar barang yang lebih banyak
BARANG = {
    # Makanan & Bahan Pokok
    "1": ("Mie Instan", 3500, "Makanan"),
    "2": ("Roti Tawar", 15000, "Makanan"),
    "3": ("Nasi Goreng Instant", 8500, "Makanan"),
    "4": ("Telur Ayam (1/2 kg)", 16000, "Makanan"),
    "5": ("Minyak Goreng 1L", 18000, "Makanan"),
    
    # Minuman
    "6": ("Air Mineral 600ml", 3000, "Minuman"),
    "7": ("Susu UHT 250ml", 7000, "Minuman"),
    "8": ("Kopi Kemasan", 4500, "Minuman"),
    "9": ("Teh Botol 450ml", 4000, "Minuman"),
    "10": ("Jus Buah 300ml", 8000, "Minuman"),

    # Snack & Camilan
    "11": ("Keripik Kentang", 10000, "Snack"),
    "12": ("Biskuit Cokelat", 8500, "Snack"),
    "13": ("Cokelat Batangan", 12500, "Snack"),
    "14": ("Kacang Atom", 6000, "Snack"),

    # Perawatan Diri & Kebersihan
    "15": ("Sabun Mandi", 4500, "Perawatan"),
    "16": ("Sampo Botol", 18500, "Perawatan"),
    "17": ("Pasta Gigi", 12000, "Perawatan"),
    "18": ("Tisu Wajah", 9000, "Perawatan")
}

# Inisialisasi session state untuk keranjang belanja
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

st.set_page_config(page_title="Kasir Minimarket", page_icon="🛒", layout="centered")

st.title("🛒 Kasir Minimarket")

# Filter Berdasarkan Kategori
st.header("1. Pilih Barang")
kategori_list = ["Semua Kategori"] + sorted(list(set(v[2] for v in BARANG.values())))
kategori_terpilih = st.selectbox("Filter Kategori:", kategori_list)

# Filter opsi produk berdasarkan kategori
opsi_barang = {}
for k, v in BARANG.items():
    nama, harga, kat = v
    if kategori_terpilih == "Semua Kategori" or kat == kategori_terpilih:
        opsi_barang[f"[{kat}] {nama} - Rp{harga:,}"] = k

pilihan = st.selectbox("Pilih Produk:", list(opsi_barang.keys()))
jumlah = st.number_input("Jumlah Beli:", min_value=1, value=1, step=1)

if st.button("➕ Tambah ke Keranjang", use_container_width=True):
    kode = opsi_barang[pilihan]
    nama, harga, _ = BARANG[kode]
    subtotal = harga * jumlah
    
    st.session_state.keranjang.append({
        "Nama": nama,
        "Harga (Rp)": harga,
        "Jumlah": jumlah,
        "Subtotal (Rp)": subtotal
    })
    st.toast(f"Ditambahkan: {jumlah}x {nama}", icon="✅")

# Displays Struk & Checkout
if st.session_state.keranjang:
    st.divider()
    st.header("2. 🧾 Struk Belanja")
    
    # Tampilkan tabel keranjang
    st.dataframe(st.session_state.keranjang, use_container_width=True)
    
    total = sum(item["Subtotal (Rp)"] for item in st.session_state.keranjang)
    st.subheader(f"Total Belanja: Rp{total:,}")
    
    # Input Pembayaran
    bayar = st.number_input("Jumlah Uang Bayar (Rp):", min_value=0, step=1000)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💳 Proses Pembayaran", type="primary", use_container_width=True):
            if bayar >= total:
                kembalian = bayar - total
                st.balloons()
                st.success(f"**Pembayaran Berhasil!**\n\nKembalian: **Rp{kembalian:,}**")
            else:
                st.error(f"Uang kurang **Rp{total - bayar:,}**!")

    with col2:
        if st.button("🗑️ Transaksi Baru / Reset", use_container_width=True):
            st.session_state.keranjang = []
            st.rerun()