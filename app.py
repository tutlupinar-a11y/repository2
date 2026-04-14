import streamlit as st
import pdfplumber

st.set_page_config(page_title="Finansal Analiz", layout="wide")
st.title("📊 Finansal Rapor Analiz Paneli")

# 1. Dosya Yükleme Alanı
uploaded_file = st.file_uploader("Gürsel Turizm PDF Raporunu Yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Rapor okunuyor, lütfen bekleyin...'):
        with pdfplumber.open(uploaded_file) as pdf:
            # Şimdilik sadece ilk sayfayı kontrol edelim
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            st.subheader("📄 Raporun İlk Sayfa Özeti")
            st.text(text) # PDF'in içindeki metni ham olarak görürüz
