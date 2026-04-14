import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="PDF → Excel (Cloud Uyumlu)", layout="wide")
st.title("📄 PDF → Excel (Streamlit Cloud Uyumlu)")

st.warning(
    "ℹ️ Streamlit Cloud kısıtları nedeniyle tablolar satır bazlı çıkarılır. "
    "Finansal PDF'ler için bu en stabil yöntemdir."
)

uploaded_file = st.file_uploader("PDF Dosyasını Yükleyin", type="pdf")

if uploaded_file and st.button("Excel'e Dönüştür"):
    with st.spinner("PDF işleniyor..."):
        rows = []

        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages[:30]:
                text = page.extract_text()

                if not text:
                    continue

                for line in text.split("\n"):
                    rows.append([line])

        df = pd.DataFrame(rows, columns=["PDF Metni"])

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Metin")

        st.success("✅ Dönüştürme tamamlandı")
        st.download_button(
            "📥 Excel'i İndir",
            data=output.getvalue(),
            file_name="pdf_metin_ciktisi.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
