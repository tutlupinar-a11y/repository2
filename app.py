import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import tempfile
import os

st.set_page_config(page_title="PDF to Excel Converter", layout="wide")
st.title("📊 Finansal PDF → Excel Dönüştürücü")

uploaded_file = st.file_uploader("📄 PDF Dosyasını Yükleyin", type="pdf")

if uploaded_file and st.button("Excel'e Dönüştür"):
    with st.spinner("PDF analiz ediliyor..."):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        output = BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

            sheet_no = 1

            # 1️⃣ Önce lattice (çizgili tablo)
            tables = camelot.read_pdf(
                pdf_path,
                pages="1-30",
                flavor="lattice"
            )

            # 2️⃣ Eğer lattice boşsa stream dene
            if tables.n == 0:
                tables = camelot.read_pdf(
                    pdf_path,
                    pages="1-30",
                    flavor="stream"
                )

            for table in tables:
                df = table.df
                df.replace("", pd.NA, inplace=True)
                df.dropna(how="all", inplace=True)

                if df.shape[0] < 2 or df.shape[1] < 2:
                    continue

                df.columns = df.iloc[0]
                df = df[1:].reset_index(drop=True)

                df.to_excel(
                    writer,
                    sheet_name=f"Tablo_{sheet_no}",
                    index=False
                )
                sheet_no += 1

        os.unlink(pdf_path)

        st.success("✅ Excel hazır!")
        st.download_button(
            "📥 Excel'i İndir",
            data=output.getvalue(),
            file_name="finansal_rapor.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
