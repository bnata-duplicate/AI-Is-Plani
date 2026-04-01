import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# --- 1. VERİTABANI: AI ATLAS MASTER MİMARİSİ ---
def vt_kur():
    conn = sqlite3.connect('ai_atlas_final.db', check_same_thread=False)
    c = conn.cursor()
    # MODÜL 1: Operasyonel İş Planı (PDF Belgelerinden Gelen Gerçek Sütunlar)
    c.execute('''CREATE TABLE IF NOT EXISTS is_plani 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, departman TEXT, ana_gorev TEXT, 
                  gorev_adi TEXT, sorumlu TEXT, baslangic TEXT, bitis TEXT, durum TEXT)''')
    
    # MODÜL 2: KPI & Veri Dönüşümü (Onay ve Güven Skoru Odaklı)
    c.execute('''CREATE TABLE IF NOT EXISTS kpi_sistemi 
                 (id INTEGER PRIMARY KEY, kpi_adi TEXT, kaynak_turu TEXT, hedef REAL, gercek REAL, 
                  onay_kademesi TEXT, guven_skoru INTEGER)''')
    conn.commit()
    conn.close()

vt_kur()

# --- 🤖 AI ATLAS DÖNÜŞÜM VE DOĞRULAMA AJANI ---
def ai_atlas_dogrulayici(kpi_degeri, kaynak, ilgili_is_durumu):
    # Veri Kaynağı Güven Analizi: Sistem (ERP) verisi manuelden üstündür.
    skor = 100 if kaynak == "Sistem (ERP/Bordro)" else 60
    
    # Operasyonel Tutarlılık Kontrolü (İş Planı Entegrasyonu)
    # İş planındaki görev tamamlanmadan (Örn: Stajyer Görüşmeleri) KPI başarısı yüksekse AI uyarır.
    if kpi_degeri > 85 and ilgili_is_durumu != "Tamamlandı":
        skor -= 45
        return skor, "🛑 TUTARSIZLIK: İş planındaki operasyonel süreçler (Stajyer/Terfi vb.) bu başarıyı doğrulamıyor!"
    return skor, "✅ Veri Kaynağı ve Operasyonel Akış Uyumlu."

# --- 🖥️ AI ATLAS STRATEJİK KONTROL PANELİ ---
st.set_page_config(page_title="AI Atlas Strategic OS", layout="wide")
st.title("🧬 AI Atlas: Kurumsal Dönüşüm ve Strateji Paneli")

tab1, tab2, tab3 = st.tabs(["📋 İş Planlama", "🎯 KPI & Veri Dönüşümü", "📈 OKR Hazırlık & Analiz"])

# --- MODÜL 1: İŞ PLANLAMA (PDF Verileriyle Senkronize) ---
with tab1:
    st.subheader("Operasyonel İş Planı (Sezon ve Faaliyet Yönetimi)")
    # PDF belgenizdeki gerçek veriler 
    is_verisi = {
        "Departman": ["İK", "İK", "İK"],
        "Ana Görev Grubu": ["Sezon Açılış İşlemleri", "Sezon Faaliyetleri", "Sezon Faaliyetleri"],
        "Görev Adı": ["Stajyer Seçimi Yazışmaları", "Lise Stajyer Görüşmeleri", "Terfi Kurulunun Toplanması"],
        "Sorumlu": ["Ezgi KIZILKAYA", "Ezgi KIZILKAYA; Yesim AKBALIK", "Ezgi KIZILKAYA; Yesim AKBALIK"],
        "Süre (Gün)": [72, 149, 7],
        "Bitiş": ["2023-02-01", "2023-06-30", "2023-02-28"]
    }
    df_is = pd.DataFrame(is_verisi)
    st.dataframe(df_is, use_container_width=True)
    st.info("💡 Ezgi KIZILKAYA ve Yeşim AKBALIK için atanan görevler AI Atlas tarafından takip edilmektedir. ")

# --- MODÜL 2: KPI & VERİ DÖNÜŞÜMÜ (RACI ONAY ZİNCİRİ) ---
with tab2:
    st.subheader("Veri Kaynağı Tanımlama ve Hesap Verebilirlik (RACI)")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # KPI belgenizdeki gerçek metrikler 
        k_metrik = st.selectbox("Ölçülecek KPI", ["Personel Devir Oranı", "Eğitim Verimliliği", "Çalışan Bağlılığı Skoru"])
        k_kaynak = st.radio("Veri Kaynağı Tipi", ["Sistem (ERP/Bordro)", "İş Planı (Otomatik)", "Manuel Beyan"])
        k_gercek = st.slider("Gerçekleşen Başarı (%)", 0, 100, 70)
        
    with c2:
        st.write("### ⛓️ RACI Hiyerarşisi")
        st.write("**Sorumlu (R):** Ezgi KIZILKAYA ")
        st.write("**Onaycı (A):** Birim / Departman Yöneticisi")
        st.write("**Danışman (C):** AI Atlas Strateji Ajanı")
        
        # AI AJANI ÇALIŞTIRMA (Örnek: İş planındaki görev durumu 'Devam Ediyor' ise)
        skor, mesaj = ai_atlas_dogrulayici(k_gercek, k_kaynak, "Devam Ediyor")
        
        if st.button("Veriyi Sisteme Kilitle (Mühürle)"):
            st.metric("AI Güven Skoru", f"{skor}/100")
            if skor < 60: st.error(mesaj)
            else: st.success(mesaj)

# --- MODÜL 3: OKR DÖNÜŞÜMÜNE HAZIRLIK ---
with tab3:
    st.subheader("Değer, Yetkinlik ve Kültür Odaklı Dönüşüm")
    st.write("İş planı ve KPI'dan süzülen verilerin 'Liderlik' ve 'Kültür' OKR'lerine etkisi:")
    
    # Stratejik Gelişim Grafiği
    chart_data = pd.DataFrame({"OKR Boyutu": ["Liderlik", "Kurumsal Kültür", "Yetkinlik"], "Gelişim %": [65, 80, 55]})
    st.bar_chart(chart_data.set_index("OKR Boyutu"))
    st.markdown("> **AI Atlas Notu:** Ezgi K. ve Yeşim A.'nın operasyonel hızı, 'Yetkinlik' OKR'sine pozitif katkı sağlıyor. ")
