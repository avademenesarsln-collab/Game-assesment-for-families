import streamlit as st
import requests
from groq import Groq

st.set_page_config(page_title="Oyun Güvenlik Radarı", page_icon="🛡️")

st.title("🛡️ Dijital Oyun Güvenlik Radarı")
st.write("Çocuğunuzun oynadığı oyunu aratın, pedagojik ve hukuki risk raporunu anında görün.")

# Şifreler Streamlit Secrets üzerinden çekiliyor
RAWG_API_KEY = st.secrets["RAWG_API_KEY"]

# 403 Hatasını aşmak için eklediğimiz tarayıcı kimliği (User-Agent) hilesi
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
    default_headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
)

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
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Sen ebeveynleri dijital oyun risklerine karşı bilgilendiren bir asistansın."},
                            {"role": "user", "content": prompt}
                        ],
                        model="qwen/qwen3.8-27b",
                        temperature=0.3,
                        max_tokens=2048,
                    )
                    
                    st.success(f"{tam_isim} ({yas_siniri}) için rapor başarıyla oluşturuldu!")
                    st.markdown(chat_completion.choices[0].message.content)
                
                # Eğer Groq API yine bir güvenlik duvarına takılırsa hatayı ekrana basacak
                except Exception as e:
                    st.error(f"Yapay Zeka API Hatası: {e}")
                    
    else:
        st.warning("Lütfen aramak istediğiniz oyunun adını yazın.")
