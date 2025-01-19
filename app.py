import streamlit as st
import pandas as pd

# Judul aplikasi web
st.title("Prediksi Stunting")

# Membaca file CSV
try:
    data = pd.read_csv('stunting.csv')  # Pastikan file CSV tersedia
except FileNotFoundError:
    st.error("File 'stunting.csv' tidak ditemukan. Harap pastikan file tersedia di folder yang sesuai.")
    st.stop()

# Ambil daftar unik kabupaten dan tahun
kabupaten_list = ['Semua Kabupaten/Kota'] + list(data['Kabupaten'].dropna().unique())
tahun_list = ['Semua Tahun'] + list(sorted(data['Tahun'].dropna().unique()))

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
selected_kabupaten = st.sidebar.selectbox("Pilih Kabupaten/Kota", kabupaten_list)
selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)

# Filter data berdasarkan pilihan
filtered_data = data.copy()
if selected_kabupaten != 'Semua Kabupaten/Kota':
    filtered_data = filtered_data[filtered_data['Kabupaten'] == selected_kabupaten]
if selected_tahun != 'Semua Tahun':
    filtered_data = filtered_data[filtered_data['Tahun'] == selected_tahun]

# Hapus kolom 'PrevalensiStunting' dari tampilan dan reset indeks
filtered_data_no_prevalensi = filtered_data.drop(columns=['PrevalensiStunting']).reset_index(drop=True)

if filtered_data.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
else:
    # Tampilkan tabel tanpa kolom 'PrevalensiStunting' dan indeks
    st.subheader(f"Hasil Filter Data")
    st.write(filtered_data_no_prevalensi)

# Input fields for prediction
def user_input_features():
    st.subheader("Input Data Prediksi")
    try:
        BayiBBLR = float(st.text_input("Bayi BBLR (%):", "0"))
        IbuNifasVitA = float(st.text_input("Ibu Nifas Mendapatkan Vitamin A (%):", "0"))
        K4 = float(st.text_input("Cakupan K4 (%):", "0"))
        IPM = float(st.text_input("Indeks Pembangunan Manusia (IPM):", "0"))
        MinumLayak = float(st.text_input("Persentase Rumah Tangga dengan Akses Minimum Layak (%):", "0"))
        SanitasiLayak = float(st.text_input("Persentase Rumah Tangga dengan Sanitasi Layak (%):", "0"))
    except ValueError:
        st.error("Masukkan angka yang valid untuk semua input.")
        st.stop()

    return pd.DataFrame([{
        'BayiBBLR': BayiBBLR,
        'IbuNifasVitA': IbuNifasVitA,
        'K4': K4,
        'IPM': IPM,
        'MinumLayak': MinumLayak,
        'SanitasiLayak': SanitasiLayak
    }])

input_data = user_input_features()

# Tombol untuk menampilkan hasil prediksi
if st.button('Check Stunting'):
    if filtered_data.empty:
        st.warning(f"Tidak ada data untuk {selected_kabupaten} pada tahun {selected_tahun}.")
    else:
        # Ambil nilai PrevalensiStunting
        prevalensi = filtered_data['PrevalensiStunting'].values[0]
        st.subheader("Hasil Prediksi")
        st.success(f"Prevalensi Stunting untuk {selected_kabupaten} pada tahun {selected_tahun}: **{prevalensi:.2f}%**")