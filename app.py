import streamlit as st
import pandas as pd

# Konfigurasi judul utama aplikasi
st.set_page_config(page_title="Aplikasi Stunting", layout="wide")
st.title("Prediksi Prevalensi Stunting")

# Menu navigasi horizontal
selected = option_menu(
    menu_title=None,  # Tidak ada judul di atas menu
    options=["Prediksi Prevalensi", "Catatan Pembuat"],  # Pilihan menu
    icons=["calculator", "info-circle"],  # Ikon untuk setiap pilihan
    menu_icon="cast",  # Ikon menu utama
    default_index=0,  # Indeks default
    orientation="horizontal",  # Orientasi horizontal
)

# Halaman 1: Prediksi Prevalensi
if selected == "Prediksi Prevalensi":
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
        st.subheader("Input Data")
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

        # Validasi input: semua input harus diisi dengan nilai lebih besar dari 0
        if any(val <= 0.0 for val in [BayiBBLR, IbuNifasVitA, K4, IPM, MinumLayak, SanitasiLayak]):
            return None  # Hentikan jika input tidak valid

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
        if input_data is None:
            st.error("Harap isi semua input dengan nilai yang valid sebelum melanjutkan.")
        else:
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

# Halaman 2: Catatan Pembuat
elif selected == "Catatan Pembuat":
    # Judul Halaman
    st.title("Catatan Pembuat")
    st.markdown("---")

    # Ringkasan Penelitian dalam Kolom
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8AGXA0AjbfuyQqtfot7BTNnjUBolQJbn9yw&s", caption="Vinny Ramayani Saragih", use_container_width=True)

    with col2:
        st.markdown("### 📚 **Penelitian ini adalah bagian dari Skripsi**")
        st.markdown(
            """
            Penelitian ini berjudul **"Perbandingan Metode Supervised Machine Learning dalam Prediksi Prevalensi Stunting di Provinsi Sumatera Utara"** 
            oleh **Vinny Ramayani Saragih (NIM 4203250007)** untuk memenuhi syarat kelulusan Program Studi Ilmu Komputer, Jurusan Matematika, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Negeri Medan.
            """
        )

    st.markdown("---")

    # Latar Belakang
    st.markdown("### 🌟 **Latar Belakang**")
    st.markdown(
        """
        **Stunting** adalah gangguan tumbuh kembang akibat kekurangan gizi kronis dan infeksi berulang, 
        yang berdampak pada fisik, kognisi, dan produktivitas jangka panjang. Berikut adalah data penting terkait prevalensi stunting:
        - 📉 **Indonesia**: Turun dari **27,7% (2019)** menjadi **21,6% (2022)**, tetapi masih di atas target WHO (<20%).
        - 📍 **Sumatera Utara**: Turun dari **25,8% (2021)** menjadi **18,9% (2023)** dengan target **14% pada 2024**.

        Metode **machine learning** seperti **SVR**, **Decision Tree**, dan **Random Forest** dapat membantu memprediksi prevalensi stunting 
        serta menganalisis faktor-faktor utama penyebabnya.
        """
    )

    st.markdown("---")

    # Tujuan Penelitian dalam Format Kartu
    st.markdown("### 🎯 **Tujuan Penelitian**")
    with st.container():
        st.markdown(
            """
            - 🔍 **Identifikasi Model Terbaik**: Menentukan algoritma yang paling akurat dan efisien dalam memprediksi prevalensi stunting.
            - 📊 **Analisis Indikator**: Memahami indikator-indikator utama yang memengaruhi prevalensi stunting untuk mendukung pengambilan keputusan.
            """
        )

    st.markdown("---")

    # Hasil Penelitian dalam Kolom
    st.markdown("### 📈 **Hasil Penelitian**")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            **Model dan Kinerja**:
            - SVR:
              - **MSE**: 396,357
              - **MAPE**: 76,17
            - Decision Tree:
              - **MSE**: 396,357
              - **MAPE**: 76,54
            - Random Forest:
              - **MSE**: 396,772
              - **MAPE**: 76,899
            """
        )

    with col2:
        st.markdown(
            """
            **Kesimpulan**:
            - **SVR** adalah model terbaik untuk memprediksi prevalensi stunting di Sumatera Utara karena memiliki **MSE** dan **MAPE** yang paling rendah dibandingkan Random Forest dan Decision Tree.
            """
        )

    st.markdown("---")

    # Kesimpulan
    st.markdown("### 🏆 **Kesimpulan**")
    st.markdown(
        """
        Dari analisis data, diperoleh **6 variabel signifikan** yang memengaruhi prevalensi stunting di Sumatera Utara:
        - 💧 **Minum Layak** (-0.4364)
        - 📈 **IPM** (-0.4313)
        - 🚽 **Sanitasi Layak** (-0.3064)
        - 🩺 **K4** (-0.2299)
        - 👶 **Bayi BBLR** (0.2262)
        - 🍼 **Ibu Nifas Vit A** (0.2091)

        🔑 **Faktor dengan dampak terbesar**: 
        **Minum Layak** memiliki pengaruh negatif tertinggi terhadap prevalensi stunting, menunjukkan pentingnya akses air bersih dalam mengurangi stunting.
        """
    )

