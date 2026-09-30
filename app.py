import streamlit as st
import requests
import google.generativeai as genai

st.set_page_config(page_title="Oyun Güvenlik Radarı", page_icon="🛡️")

st.title("🛡️ Dijital Oyun Güvenlik Radarı")
st.write("Çocuğunuzun oynadığı oyunu aratın, pedagojik ve hukuki risk raporunu anında görün.")

# Şifreler Streamlit Secrets üzerinden çekiliyor
RAWG_API_KEY = st.secrets["RAWG_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Yapay Zeka Motorunu (Gemini) Başlatma
genai.configure(api_key=GEMINI_API_KEY)

# Listenden aldığımız en güncel ve süper hızlı model!
model = genai.GenerativeModel('gemini-3.5-flash')

oyun_adi = st.text_input("Oyun Adı (Örn: Minecraft, Roblox, Valorant, Chivalry 2):")

if st.button("Risk Raporu Oluştur"):
    if oyun_adi:
        with st.spinner(f"{oyun_adi} için küresel veritabanları taranıyor ve yapay zeka analiz yapıyor..."):
            url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={oyun_adi}"
            cevap = requests.get(url).json()

            if not cevap.get('results'):
                st.error("Oyun bulunamadı. Lütfen ismini doğru yazdığınızdan emin olun.")
            else:
                ilk_sonuc = cevap['results'][0]
                tam_isim = ilk_sonuc.get('name')
                yas_siniri_verisi = ilk_sonuc.get('esrb_rating')
                yas_siniri = yas_siniri_verisi['name'] if yas_siniri_verisi else "Belirtilmemiş"

                prompt = f"""
                Sen bir Çocuk Psikoloğu, Dijital Güvenlik Uzmanı ve Hukukçusun.
                Oyun Adı: {tam_isim}
                Resmi Yaş Sınırı: {yas_siniri}
                Ebeveynler için OYUNUN İÇERİĞİ, KÜRESEL İDDİALAR ve EBEVEYN TAVSİYESİ başlıklarında net, anlaşılır ve Türkçe bir rapor hazırla.
                """

                # Hata yakalama bloğu
                try:
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=4096,
                        )
                    )
                    
                    st.success(f"{tam_isim} ({yas_siniri}) için rapor başarıyla oluşturuldu!")
                    st.markdown(response.text)
                
                except Exception as e:
                    st.error(f"Yapay Zeka API Hatası: {e}")
                    
    else:
        st.warning("Lütfen aramak istediğiniz oyunun adını yazın.")
