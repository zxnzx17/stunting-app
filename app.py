import streamlit as st
import pandas as pd

# Judul aplikasi web
st.title("Prediksi Stunting")

# Membaca file CSV
try:
    stunting_data = pd.read_csv('stunting.csv')  # File untuk data input
    results_data = pd.read_csv('final_results.csv')  # File untuk hasil prediksi
except FileNotFoundError as e:
    st.error(f"File tidak ditemukan: {e.filename}. Harap pastikan file tersedia di folder yang sesuai.")
    st.stop()

# Ambil daftar unik kabupaten, tahun, dan metode
kabupaten_list = ['Semua Kabupaten/Kota'] + list(results_data['Kabupaten'].dropna().unique())
tahun_list = ['Semua Tahun'] + list(sorted(results_data['Tahun'].dropna().unique()))
metode_list = ['Semua Metode'] + list(results_data['Metode'].dropna().unique())

# Sidebar untuk filter data
st.sidebar.header("Filter Data")
selected_kabupaten = st.sidebar.selectbox("Pilih Kabupaten/Kota", kabupaten_list)
selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_list)
selected_metode = st.sidebar.selectbox("Pilih Metode", metode_list)

# Input fields untuk data prediksi dari stunting.csv
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

# Ambil input pengguna
input_data = user_input_features()

# Tombol untuk menampilkan hasil prediksi
if st.button('Check Stunting'):
    # Filter data dari final_results.csv
    filtered_results = results_data.copy()
    if selected_kabupaten != 'Semua Kabupaten/Kota':
        filtered_results = filtered_results[filtered_results['Kabupaten'] == selected_kabupaten]
    if selected_tahun != 'Semua Tahun':
        filtered_results = filtered_results[filtered_results['Tahun'] == selected_tahun]
    if selected_metode != 'Semua Metode':
        filtered_results = filtered_results[filtered_results['Metode'] == selected_metode]

    # Tampilkan hasil prediksi jika data tersedia
    st.subheader("Hasil Prediksi")
    if filtered_results.empty:
        st.warning(f"Tidak ada data prediksi yang cocok untuk filter {selected_kabupaten}, {selected_tahun}, dan {selected_metode}.")
    else:
        prediksi = filtered_results['Prediksi'].values[0]  # Ambil prediksi pertama
        st.success(f"Prediksi Prevalensi Stunting untuk {selected_kabupaten} pada tahun {selected_tahun} dengan metode {selected_metode}: **{prediksi:.2f}%**")
