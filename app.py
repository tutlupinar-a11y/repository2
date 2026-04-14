import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF to Excel Converter", layout="wide")
st.title("📂 Finansal Rapor Excel Dönüştürücü")

st.info(
    "Bu araç, finansal rapor PDF'lerindeki tabloları daha düzgün şekilde ayıklayıp Excel formatına çevirir."
)

uploaded_file = st.file_uploader("📄 PDF Dosyasını Yükleyin", type="pdf")

if uploaded_file is not None:
    if st.button("✅ Excel'e Dönüştür ve İndir"):
        with st.spinner("PDF tabloları işleniyor..."):
            output = BytesIO()

            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                with pdfplumber.open(uploaded_file) as pdf:

                    sheet_counter = 1

                    for page_number, page in enumerate(pdf.pages[:30], start=1):

                        table_settings = {
                            "vertical_strategy": "lines",
                            "horizontal_strategy": "lines",
                            "snap_tolerance": 3,
                            "intersection_tolerance": 5,
                            "edge_min_length": 3,
                        }

                        table = page.extract_table(table_settings)

                        if table:
                            df = pd.DataFrame(table)

                            # Tamamen boş satır/sütunları at
                            df.dropna(how="all", inplace=True)
                            df.dropna(axis=1, how="all", inplace=True)

                            # Çok küçük / anlamsız tabloları ele
                            if df.shape[0] < 2 or df.shape[1] < 2:
                                continue

                            # İlk satırı başlık yap
                            df.columns = df.iloc[0]
                            df = df[1:].reset_index(drop=True)

                            sheet_name = f"Tablo_{sheet_counter}"
                            df.to_excel(
                                writer,
                                sheet_name=sheet_name[:31],
                                index=False
                            )

                            sheet_counter += 1

            st.success("🎉 Dönüştürme başarıyla tamamlandı!")

            st.download_button(
                label="📥 Excel Dosyasını İndir",
                data=output.getvalue(),
                file_name="finansal_rapor.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
