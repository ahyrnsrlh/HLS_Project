from scraper import scrape_sinta
import logging

# Konfigurasi logging
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

if __name__ == "__main__":
    logging.info("Memulai scraping publikasi dari SINTA...")
    scrape_sinta()
    logging.info("Scraping selesai! Data tersimpan di data/data_sinta.csv")
