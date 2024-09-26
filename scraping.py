from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

# ChromeDriver'ı başlat
#service = Service(ChromeDriverManager().install())
service = Service('C:/Users/ryntm/Desktop/chromedriver.exe')  # Chromedriver'ın yolu 
driver = webdriver.Chrome(service=service)
url = 'https://www.sikayetvar.com/teksut'  # Yorumların bulunduğu sayfanın URL'si
driver.get(url)
time.sleep(20)

# Yorumları içeren elementleri bulmak için
#comments = driver.find_elements(By.CSS_SELECTOR, 'div.comment-text p') # html'deki div adı neyse onu yazıyoruz (burda comment-text), sonra p de türü. 
#comments = driver.find_elements(By.CSS_SELECTOR, 'div.hermes-Comments-module-kV6VmHxTOAz2NZN1JIxw span') # türü span 
comments = driver.find_elements(By.CSS_SELECTOR, 'a.complaint-description') # türü a
comments_list = [comment.text for comment in comments]
driver.quit()
new_df = pd.DataFrame(comments_list, columns=['text'])
file_path = 'Yorumlar.xlsx'
if os.path.exists(file_path):
    # Var olan dosyayı oku
    existing_df = pd.read_excel(file_path)
    # Yeni verilerle birleştir
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    # Dosya yoksa sadece yeni verileri kullan
    combined_df = new_df

# Birleştirilmiş DataFrame'i Excel dosyasına kaydedin
combined_df.to_excel(file_path, index=False)

print("Yorumlar başarıyla '{}' dosyasına kaydedildi.".format(file_path))
