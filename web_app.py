import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import hashlib

# --- 1. VERİTABANI VE GÜVENLİK ---
def vt_baglan():
    return sqlite3.connect('kurumsal_is_plani_final.db', check_same_thread=False)

def tablo_olustur():
    conn = vt_baglan()
    c = conn.cursor()
    # Çoklu sorumlu ve bağımlılık (onceki_id) destekli tablo
    c.execute('''CREATE TABLE IF NOT EXISTS gorevler 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  baslik TEXT, sorumlu TEXT, baslangic TEXT, bitis TEXT, 
                  durum TEXT, ilerleme INTEGER, onceki_id INTEGER)''')
    conn.commit()
    conn.close()

tablo_olustur()

def sifre_hashle(sifre):
    return hashlib.sha256(str.encode(sifre)).hexdigest()

# --- 2. OTURUM YÖNETİMİ ---
if 'giris' not in st.session_state: st.session_state.giris = False

if not st.session_state.giris:
    st.title("🔐 Kurumsal AI Panel Girişi")
    k_adi = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Sisteme Eriş"):
        if k_adi == "admin" and sifre_hashle(sifre) == sifre_hashle("admin123"):
            st.session_state.giris = True
            st.rerun()
        else: st.error("Hatalı Giriş Denemesi!")
else:
    st.set_page_config(page_title="AI Project Master", layout="wide")
    st.title("🚀 Kurumsal AI Proje ve Ekip Yönetimi")

    # --- 3. VERİ ÇEKME ---
    conn = vt_baglan()
    df = pd.read_sql_query("SELECT * FROM gorevler", conn)
    conn.close()

    # --- 4. YAN MENÜ: GELİŞMİŞ GÖREV TANIMLAMA ---
    with st.sidebar:
        st.header("➕ Yeni Görev Tanımla")
        y_baslik = st.text_input("Görevin Adı")
        
        # ÇOKLU SORUMLU SEÇİMİ (İstediğiniz Özellik)
        y_ekip = st.multiselect("Sorumlu Ekip Üyeleri", ["Ali", "Ayşe", "Caner", "Müdür", "Zeynep"])
        y_sorumlu_str = ", ".join(y_ekip)
        
        y_bitis = st.date_input("Teslim Tarihi", min_value=date.today())
        
        # BAĞIMLILIK (Önceki İş Seçimi)
        onceki_isler = ["Yok"] + df['baslik'].tolist() if not df.empty else ["Yok"]
        y_onceki_ad = st.selectbox("Bu işten önce hangisi bitmeli?", onceki_isler)
        
        y_onceki_id = None
        if y_onceki_ad != "Yok" and not df.empty:
            y_onceki_id = int(df[df['baslik'] == y_onceki_ad]['id'].values[0])

        if st.button("Veritabanına Kaydet"):
            if y_baslik and y_ekip:
                conn = vt_baglan()
                c = conn.cursor()
                c.execute("""INSERT INTO gorevler (baslik, sorumlu, baslangic, bitis, durum, ilerleme, onceki_id) 
                             VALUES (?,?,?,?,?,?,?)""",
                          (y_baslik, y_sorumlu_str, str(date.today()), str(y_bitis), "Devam Ediyor", 0, y_onceki_id))
                conn.commit()
                conn.close()
                st.success("Görev başarıyla eklendi!")
                st.rerun()
            else:
                st.error("Lütfen başlık ve en az bir sorumlu seçin!")

    # --- 5. ANA EKRAN: TABLO VE ANALİZ ---
    if not df.empty:
        st.subheader("📊 Canlı İş Akışı ve Bağımlılık Analizi")
        
        # TABLO DÜZENLEME VE SİLME DESTEĞİ
        # Kullanıcı tabloda değişiklik yapabilir
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="data_editor")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        if col_btn1.button("💾 Değişiklikleri Kaydet"):
            conn = vt_baglan()
            edited_df.to_sql('gorevler', conn, if_exists='replace', index=False)
            conn.close()
            st.success("Veritabanı güncellendi!")
            st.rerun()

        # --- 6. 🤖 AI ASİSTAN VE TAHMİNLEME ---
        st.divider()
        st.subheader("🧠 Gemini AI Proje Analizi")
        
        riskli_isler = []
        bugun = date.today()
        
        for idx, row in df.iterrows():
            bitis_dt = datetime.strptime(row['bitis'], "%Y-%m-%d").date()
            kalan_gun = (bitis_dt - bugun).days
            
            # Risk Analizi 1: Tarih Sıkışması
            if kalan_gun <= 2 and row['durum'] != 'Tamamlandı':
                riskli_isler.append(f"🔴 {row['baslik']} ({row['sorumlu']}) - Teslimat çok yakın!")
            
            # Risk Analizi 2: Bağımlılık Kontrolü
            if row['onceki_id']:
                onceki = df[df['id'] == row['onceki_id']]
                if not onceki.empty:
                    o_bitis = datetime.strptime(onceki.iloc[0]['bitis'], "%Y-%m-%d").date()
                    m_baslangic = datetime.strptime(row['baslangic'], "%Y-%m-%d").date()
                    if m_baslangic < o_bitis:
                        riskli_isler.append(f"⚠️ {row['baslik']}, {onceki.iloc[0]['baslik']} bitmeden başlamış görünüyor!")

        if riskli_isler:
            for r in riskli_isler: st.warning(r)
            st.chat_message("assistant").write(f"Yönetici, şu an {len(riskli_isler)} kritik uyarı tespit ettim. Özellikle zaman çakışmalarını düzeltmenizi öneririm.")
        else:
            st.success("Harika! AI denetimine göre akışta hiçbir bağımlılık veya zaman hatası bulunmuyor.")

    else:
        st.info("Sistem şu an boş. Lütfen sol taraftan ilk görevinizi tanımlayın.")
