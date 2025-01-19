import pandas as pd

def preprocess_input(data: pd.DataFrame) -> pd.DataFrame:
    # Lakukan preprocessing, seperti normalisasi atau encoding jika diperlukan.
    # Contoh: Pastikan data numerik terisi dengan benar.
    return data.drop(columns=['kab_kota', 'tahun'])  # Hapus kolom non-numerik (jika model tidak membutuhkan)
