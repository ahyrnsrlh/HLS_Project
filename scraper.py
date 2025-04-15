import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from config import BASE_URL, HEADERS, START_PAGE, END_PAGE, OUTPUT_CSV

# List untuk menyimpan hasil scraping
data_list = []

def scrape_sinta():
    for page in range(START_PAGE, END_PAGE + 1):
        url = BASE_URL.format(page)
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Ambil semua publikasi dari halaman
                publications = soup.select(".ar-list-item")  # Selector publikasi

                for pub in publications:
                    title = pub.select_one(".title").text.strip() if pub.select_one(".title") else "N/A"
                    authors = pub.select_one(".authors").text.strip() if pub.select_one(".authors") else "N/A"
                    year = pub.select_one(".year").text.strip() if pub.select_one(".year") else "N/A"
                    citations = pub.select_one(".citations").text.strip() if pub.select_one(".citations") else "0"
                    
                    # Link ke Google Scholar
                    gs_link_element = pub.select_one("a[href*='scholar.google.com']")
                    gs_link = gs_link_element["href"] if gs_link_element else "N/A"

                    data_list.append({
                        "Page": page,
                        "Title": title,
                        "Authors": authors,
                        "Year": year,
                        "Citations": citations,
                        "Google Scholar Link": gs_link
                    })

                logging.info(f"✅ {page} - {len(publications)} publikasi berhasil di-scrape")
            else:
                logging.warning(f"⚠️ {page} - Gagal mengakses halaman, status: {response.status_code}")

        except Exception as e:
            logging.error(f"❌ Error scraping {page}: {str(e)}")

        # Delay untuk menghindari pemblokiran
        time.sleep(random.uniform(1, 3))

    # Simpan ke CSV
    df = pd.DataFrame(data_list)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f"🎉 Scraping selesai! Data tersimpan di {OUTPUT_CSV}")
