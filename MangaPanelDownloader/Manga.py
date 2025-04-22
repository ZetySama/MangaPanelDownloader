# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from selenium import webdriver
import time
import tkinter as tk
from tkinter import messagebox

# Resimleri indirme fonksiyonu
def resimleri_indir(site_url, cikis_klasoru, baslangic_bolum, bitis_bolum):
    os.makedirs(cikis_klasoru, exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    try:
        for bolum_no in range(baslangic_bolum, bitis_bolum + 1):
            url = site_url.format(bolum_no)
            driver.get(url)
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            img_etiketleri = soup.find_all("img", class_="ts-main-image")
            
            if not img_etiketleri:
                print(f"{bolum_no} numaralı bölümde img etiketleri bulunamadı.")
                continue
            
            for img in img_etiketleri:
                img_url = img.get("src") or img.get("data-src")
                if not img_url:
                    continue
                
                img_url = urljoin(url, img_url)
                img_adi = f"bolum_{bolum_no}_" + os.path.basename(img_url)
                
                try:
                    img_data = requests.get(img_url).content
                    img_yolu = os.path.join(cikis_klasoru, img_adi)
                    with open(img_yolu, "wb") as img_dosyasi:
                        img_dosyasi.write(img_data)
                    print(f"{img_adi} indirildi.")
                
                except Exception as e:
                    print(f"{img_adi} indirilemedi: {e}")
            print(f"{bolum_no}. Bölüm Bitti !!")
             
        messagebox.showinfo("Tamamlandı", "Resimler başarıyla indirildi!")
    
    finally:
        driver.quit()

# Tkinter arayüzü
def baslat():
    site_url = url_giris.get()
    cikis_klasoru = klasor_giris.get()
    baslangic_bolum = int(baslangic_bolum_giris.get())
    bitis_bolum = int(bitis_bolum_giris.get())
    
    resimleri_indir(site_url, cikis_klasoru, baslangic_bolum, bitis_bolum)

# Tkinter ana pencere
pencere = tk.Tk()
pencere.title("Resim İndirici")
pencere.geometry("400x300")

# URL Girişi
tk.Label(pencere, text="Site URL'si:").pack()
url_giris = tk.Entry(pencere, width=50)
url_giris.insert(0, "https://adumanga.com/blue-lock-bolum-{}/")
url_giris.pack()

# Başlangıç Bölüm Girişi
tk.Label(pencere, text="Başlangıç Bölümü:").pack()
baslangic_bolum_giris = tk.Entry(pencere, width=10)
baslangic_bolum_giris.insert(0, "247")
baslangic_bolum_giris.pack()

# Bitiş Bölüm Girişi
tk.Label(pencere, text="Bitiş Bölümü:").pack()
bitis_bolum_giris = tk.Entry(pencere, width=10)
bitis_bolum_giris.insert(0, "250")
bitis_bolum_giris.pack()

# Çıkış Klasörü Girişi
tk.Label(pencere, text="Çıkış Klasörü:").pack()
klasor_giris = tk.Entry(pencere, width=30)
klasor_giris.insert(0, "indirilen_gorseller")
klasor_giris.pack()

# Başlat Butonu
baslat_butonu = tk.Button(pencere, text="İndirmeyi Başlat", command=baslat)
baslat_butonu.pack(pady=20)

# Tkinter döngüsünü başlat
pencere.mainloop()

