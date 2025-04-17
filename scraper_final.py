import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import os  # Import os for directory handling
from config import BASE_URL, HEADERS, START_PAGE, END_PAGE, OUTPUT_CSV

# List untuk menyimpan hasil scraping
data_list = []

async def fetch(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url, headers=random.choice(HEADERS), timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logging.warning(f"⚠️ Gagal mengakses {url}, status: {response.status}")
                    return None
        except Exception as e:
            logging.error(f"❌ Error fetching {url}: {str(e)}")
            if attempt < retries - 1:
                logging.info(f"🔄 Retrying {url} (Attempt {attempt + 2}/{retries})...")
                await asyncio.sleep(2)  # Wait before retrying
            else:
                logging.error(f"❌ Failed to fetch {url} after {retries} attempts.")
                return None

async def scrape_sinta():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(START_PAGE, END_PAGE + 1):
            url = BASE_URL.format(page)
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for page, html_content in zip(range(START_PAGE, END_PAGE + 1), responses):
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                publications = soup.select(".ar-list-item")  # Selector publikasi

                if not publications:
                    logging.warning(f"⚠️ Tidak ada publikasi ditemukan di halaman {page}")
                    continue  # Skip to the next page if no publications are found

                for pub in publications:
                    title = pub.select_one(".title").text.strip() if pub.select_one(".title") else "N/A"
                    authors = pub.select_one(".authors").text.strip() if pub.select_one(".authors") else "N/A"
                    year = pub.select_one(".year").text.strip() if pub.select_one(".year") else "N/A"
                    citations = pub.select_one(".citations").text.strip() if pub.select_one(".citations") else "0"
                    
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
                logging.error(f"❌ No content returned for page {page}.")

        # Check if the data directory exists, if not create it
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

        # Simpan ke CSV
        df = pd.DataFrame(data_list)
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
        logging.info(f"🎉 Scraping selesai! Data tersimpan di {OUTPUT_CSV}")

def main():
    logging.info("Memulai scraping publikasi dari SINTA...")
    asyncio.run(scrape_sinta())  # Ensure correct call to the async function
    logging.info("Scraping selesai! Data tersimpan di data/data_sinta.csv")

if __name__ == "__main__":
    main()
