import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Finansal Analiz", layout="wide")
st.title("📊 Gürsel Turizm: Hassas Veri Analizi")

uploaded_file = st.file_uploader("Finansal Raporu Yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Derin tarama yapılıyor (Bu biraz zaman alabilir)...'):
        with pdfplumber.open(uploaded_file) as pdf:
            relevant_dfs = []
            
            # İlk 25 sayfayı daha detaylı tara
            for i in range(25):
                page = pdf.pages[i]
                
                # Tablo bulma ayarlarını hassaslaştırıyoruz
                table_settings = {
                    "vertical_strategy": "lines", 
                    "horizontal_strategy": "lines",
                    "snap_tolerance": 3,
                    "join_tolerance": 3,
                }
                
                tables = page.extract_tables(table_settings=table_settings)
                
                # Eğer standart çizgilerle bulamazsa, metin hizalamasından bulmayı dene
                if not tables:
                    tables = page.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})

                for table in tables:
                    df = pd.DataFrame(table)
                    # "Nakit", "Benzerleri" veya "Yatırım" geçen tabloları filtrele
                    mask = df.astype(str).apply(lambda x: x.str.contains('Nakit|Benzerleri|Yatırım|Dönem', case=False, na=False))
                    if mask.any().any():
                        relevant_dfs.append((i+1, df))

            if relevant_dfs:
                st.success(f"{len(relevant_dfs)} adet finansal veri tablosu yakalandı!")
                for page_num, df in relevant_dfs:
                    with st.expander(f"Sayfa {page_num} üzerindeki Tablo"):
                        # Boş satır/sütun temizliği yapalım
                        df = df.dropna(how='all').dropna(axis=1, how='all')
                        st.dataframe(df, use_container_width=True)
            else:
                st.error("Hala tablo çekilemedi. Rapor taranmış bir resim (OCR gerekli) olabilir mi?")
