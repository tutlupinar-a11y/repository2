import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="wide")
st.title("📂 Finansal Rapor Excel Dönüştürücü")

st.info("Bu araç, Gürsel Turizm raporu gibi karmaşık PDF'lerdeki tabloları ayıklayıp Excel formatına çevirir.")

uploaded_file = st.file_uploader("PDF Dosyasını Yükleyin", type="pdf")

if uploaded_file is not None:
    if st.button("Excel'e Dönüştür ve İndir"):
        with st.spinner('Tablolar ayıklanıyor... Bu işlem doküman boyutuna göre vakit alabilir.'):
            output = BytesIO()
            # Excel yazıcısını hazırla
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                with pdfplumber.open(uploaded_file) as pdf:
                    for i, page in enumerate(pdf.pages[:30]): # İlk 30 sayfayı işle
                        tables = page.extract_tables()
                        for j, table in enumerate(tables):
                            df = pd.DataFrame(table)
                            # Tabloyu temizle (boş satır/sütunları at)
                            df = df.dropna(how='all').dropna(axis=1, how='all')
                            
                            if not df.empty:
                                # Her tabloyu ayrı bir sayfaya veya isimlendirerek yaz
                                sheet_name = f"Sayfa_{i+1}_Tablo_{j+1}"
                                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            
            processed_data = output.getvalue()
            st.success("Dönüştürme tamamlandı!")
            st.download_button(
                label="📥 Excel Dosyasını İndir",
                data=processed_data,
                file_name="finansal_rapor_analiz.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
