import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Gemini Radar Testi")
st.title("🔍 Google Gemini Sistem Testi")

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    
    st.info("Google sunucularına bağlanılıyor ve hesabınıza açık modeller listeleniyor...")
    
    modeller = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if modeller:
        st.success("Bağlantı Başarılı! İşte kullanabileceğimiz modeller:")
        for model_adi in modeller:
            st.code(model_adi.replace("models/", ""))
    else:
        st.warning("Bu API anahtarına açık metin modeli bulunamadı.")
        
except Exception as e:
    st.error(f"Sistem Hatası: {e}")
