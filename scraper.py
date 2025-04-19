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

async def scrape_sinta(start_page=START_PAGE, end_page=END_PAGE, output_csv=OUTPUT_CSV):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(start_page, end_page + 1):
            url = BASE_URL.format(page)
            tasks.append(fetch(session, url))

        responses = await asyncio.gather(*tasks)

        for page, html_content in zip(range(start_page, end_page + 1), responses):
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                publications = soup.select(".ar-list-item")  # Selector publikasi

                if not publications:
                    logging.warning(f"⚠️ Tidak ada publikasi ditemukan di halaman {page}")
                    continue  # Skip to the next page if no publications are found

                for pub in publications:
                    try:
                        # Extract title properly
                        title_element = pub.select_one(".ar-title a")
                        title = title_element.text.strip() if title_element else "N/A"
                        
                        # Extract authors - fixed selector based on actual HTML structure
                        authors_text = ""
                        for meta_div in pub.select(".ar-meta"):
                            for link in meta_div.select("a"):
                                if "Authors :" in link.text:
                                    authors_text = link.text.strip()
                                    break
                            if authors_text:
                                break
                        
                        # Process authors text to remove the prefix
                        if authors_text and "Authors :" in authors_text:
                            authors = authors_text.replace("Authors :", "").strip()
                        else:
                            authors = "N/A"
                        
                        # Extract publication details
                        pub_details = ""
                        pub_element = pub.select_one(".ar-meta .ar-pub")
                        if pub_element:
                            pub_details = pub_element.text.strip()
                        
                        # Extract year properly 
                        year_element = pub.select_one(".ar-year")
                        year = year_element.text.strip() if year_element else "N/A"
                        
                        # Extract citations properly
                        citations_element = pub.select_one(".ar-cited")
                        citations = "0"
                        if citations_element:
                            citations_text = citations_element.text.strip()
                            # Extract just the number from "X cited"
                            if "cited" in citations_text:
                                citations = citations_text.split("cited")[0].strip()
                        
                        # Extract Google Scholar link
                        gs_link_element = pub.select_one("a[href*='scholar.google.com']")
                        gs_link = gs_link_element["href"] if gs_link_element else "N/A"

                        data_list.append({
                            "Page": page,
                            "Title": title,
                            "Authors": authors,
                            "Publication": pub_details,
                            "Year": year,
                            "Citations": citations,
                            "Google Scholar Link": gs_link
                        })
                    except Exception as e:
                        logging.error(f"❌ Error parsing publication on page {page}: {str(e)}")
                        # Add the problematic item with error information
                        data_list.append({
                            "Page": page,
                            "Title": f"Error: {str(e)}",
                            "Authors": "N/A",
                            "Publication": "N/A",
                            "Year": "N/A",
                            "Citations": "0",
                            "Google Scholar Link": "N/A"
                        })

                logging.info(f"✅ {page} - {len(publications)} publikasi berhasil di-scrape")
            else:
                logging.error(f"❌ No content returned for page {page}.")

        # Check if the data directory exists, if not create it
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        # Simpan ke CSV
        df = pd.DataFrame(data_list)
        df.to_csv(output_csv, index=False, encoding="utf-8")
        logging.info(f"🎉 Scraping selesai! Data tersimpan di {output_csv}")

def main():
    logging.info("Memulai scraping publikasi dari SINTA...")
    asyncio.run(scrape_sinta())  # Ensure correct call to the async function
    logging.info("Scraping selesai! Data tersimpan di data/data_sinta.csv")

if __name__ == "__main__":
    main()
