import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Finansal Analiz Paneli", layout="wide")
st.title("📊 Gürsel Turizm Finansal Veri Çıkarıcı")

uploaded_file = st.file_uploader("PDF Raporunu Buraya Yükleyin", type="pdf")

if uploaded_file is not None:
    with st.spinner('Rapor analiz ediliyor...'):
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = ""
            # İlk 20 sayfayı tarayalım (Genelde özet tablolar buralardadır)
            for page in pdf.pages[:20]:
                all_text += page.extract_text() + "\n"

            st.success("Analiz Tamamlandı!")
            
            # --- VERİ ÇEKME MANTIĞI ---
            st.subheader("💰 Nakit Durumu ve Yatırımlar")
            
            # Basit bir arama yapalım
            satirlar = all_text.split('\n')
            
            bulunan_veriler = []
            for satir in satirlar:
                # Aradığımız anahtar kelimeler
                if "Nakit ve Nakit Benzerleri" in satir or "Finansal Yatırımlar" in satir:
                    bulunan_veriler.append(satir)

            if bulunan_veriler:
                for veri in bulunan_veriler:
                    st.info(veri)
            else:
                st.warning("Aranan başlıklar metin içinde tam eşleşme ile bulunamadı. Tablo yapısı karmaşık olabilir.")

            # Test için tüm metni aşağıya ekleyelim
            with st.expander("Rapor Metnini Gör"):
                st.text(all_text)
