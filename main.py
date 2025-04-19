from scraper import scrape_sinta
import logging
import argparse
import asyncio

# Konfigurasi logging
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - %(message)s")

async def main_async(start_page, end_page, output_csv):
    logging.info("Memulai scraping publikasi dari SINTA...")
    try:
        await scrape_sinta(start_page, end_page, output_csv)
    except Exception as e:
        logging.error(f"❌ Error during scraping: {str(e)}")
    logging.info("Scraping selesai! Data tersimpan di {}".format(output_csv))

def main(start_page, end_page, output_csv):
    asyncio.run(main_async(start_page, end_page, output_csv))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape publications from SINTA.")
    parser.add_argument("--start_page", type=int, default=2503, help="Starting page number")
    parser.add_argument("--end_page", type=int, default=3337, help="Ending page number")
    parser.add_argument("--output_csv", type=str, default="data/data_sinta.csv", help="Output CSV file path")
    args = parser.parse_args()

    main(args.start_page, args.end_page, args.output_csv)
