import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# --- GÜVENLİK AYARLARI (Şifreleme) ---
def sifre_olustur(sifre):
    return hashlib.sha256(str.encode(sifre)).hexdigest()

# Varsayılan Kullanıcılar (Normalde DB'de saklanır)
KULLANICILAR = {
    "admin": {"sifre": sifre_olustur("admin123"), "rol": "Yönetici"},
    "ali": {"sifre": sifre_olustur("ali2026"), "rol": "Personel"},
    "ayse": {"sifre": sifre_olustur("ayse2026"), "rol": "Personel"}
}

# --- OTURUM YÖNETİMİ ---
if 'giris_yapildi' not in st.session_state:
    st.session_state.giris_yapildi = False

def login_ekrani():
    st.title("🔐 Proje Yönetim Merkezi - Giriş")
    with st.form("Giriş Formu"):
        k_adi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        if st.form_submit_button("Giriş Yap"):
            if k_adi in KULLANICILAR and KULLANICILAR[k_adi]["sifre"] == sifre_olustur(sifre):
                st.session_state.giris_yapildi = True
                st.session_state.kullanici = k_adi
                st.session_state.rol = KULLANICILAR[k_adi]["rol"]
                st.rerun()
            else:
                st.error("Hatalı kullanıcı adı veya şifre!")

# --- ANA UYGULAMA ---
if not st.session_state.giris_yapildi:
    login_ekrani()
else:
    # Sayfa Başlığı ve Çıkış Butonu
    st.set_page_config(page_title="SafeAI Project", layout="wide")
    col_head, col_out = st.columns([9, 1])
    col_head.title(f"🚀 Hoş Geldin, {st.session_state.kullanici.capitalize()} ({st.session_state.rol})")
    if col_out.button("Çıkış Yap"):
        st.session_state.giris_yapildi = False
        st.rerun()

    # --- VERİ SETİ ---
    if 'is_akisi' not in st.session_state:
        st.session_state.is_akisi = [
            {"id": 1, "baslik": "Sistem Altyapısı", "sorumlular": ["ali"], "baslangic": "2026-04-01", "bitis": "2026-04-10", "durum": "Devam Ediyor"},
            {"id": 2, "baslik": "Yazılım Testi", "sorumlular": ["ayse"], "baslangic": "2026-04-11", "bitis": "2026-04-20", "durum": "Beklemede"},
        ]

    # --- ROL BAZLI EKRANLAR ---
    if st.session_state.rol == "Yönetici":
        st.header("📊 Yönetici Paneli: Tüm İş Akışı")
        # Yönetici her şeyi düzenleyebilir
        df = pd.DataFrame(st.session_state.is_akisi)
        st.data_editor(df, use_container_width=True)
        
        st.subheader("🤖 AI Risk Analizi (Sadece Yönetici)")
        if st.button("Tüm Sistemi Denetle"):
            st.warning("AI: Ali'nin işi gecikirse Ayşe'nin takvimi bozulacaktır.")

    elif st.session_state.rol == "Personel":
        st.header("📋 Görevlerim")
        # Personel sadece kendi isminin olduğu işleri görür
        kendi_isleri = [g for g in st.session_state.is_akisi if st.session_state.kullanici in g["sorumlular"]]
        
        if kendi_isleri:
            for is_ in kendi_isleri:
                with st.container(border=True):
                    st.write(f"**Görev:** {is_['baslik']}")
                    st.write(f"**Bitiş:** {is_['bitis']}")
                    if st.button(f"Görevi Tamamla ✅", key=is_['id']):
                        st.success("Tebrikler! Durum güncellendi.")
        else:
            st.info("Şu an size atanmış aktif bir görev bulunmuyor.")
