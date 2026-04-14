import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Finansal Analiz", layout="wide")
st.title("📊 Gürsel Turizm Finansal Tablo Analizi")

uploaded_file = st.file_uploader("PDF Raporunu Yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Tablolar taranıyor...'):
        with pdfplumber.open(uploaded_file) as pdf:
            found_tables = []
            
            # İlk 30 sayfadaki tabloları kontrol et (Finansal durum tabloları buradadır)
            for i in range(30):
                page = pdf.pages[i]
                tables = page.extract_tables()
                
                for table in tables:
                    df = pd.DataFrame(table)
                    # Tablo içinde "Nakit" veya "Yatırım" kelimesi geçiyor mu?
                    if df.astype(str).apply(lambda x: x.str.contains('Nakit|Yatırım', case=False)).any().any():
                        found_tables.append(df)

            if found_tables:
                st.success(f"{len(found_tables)} adet ilgili tablo bulundu!")
                for idx, df in enumerate(found_tables):
                    with st.expander(f"Tablo {idx+1}"):
                        st.table(df) # Rakamları sütun sütun görmeni sağlar
            else:
                st.warning("Rakam içeren tablolar bu yöntemle çekilemedi. Sayfayı manuel inceleyelim.")
