import requests
import time
from bs4 import BeautifulSoup

base_url = 'https://sinta.kemdikbud.go.id/affiliations/profile/398/?view=googlescholar'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for page in range(2503, 3337):
  url = base_url.format(page)
  print(f"Scraping halaman {page}...")

  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      articles = soup.find_all('div', class_='ar-list-item mb-5')

      for article in articles:

          title_tag = article.find('div', class_='ar-title').find('a')
          title = title_tag.text.strip() if title_tag else "Tidak ditemukan"
          gs_link = title_tag['href'] if title_tag else "Tidak ditemukan"

          author_tag = article.find('div', class_='ar-meta').find('a', text=lambda x: x and "Authors" in x)
          author = author_tag.text.replace("Authors :", "").strip() if author_tag else "Tidak ditemukan"

          year_tag = article.find('a', class_='ar-year')
          year = year_tag.text.strip() if year_tag else "Tidak ditemukan"

          cited_tag = article.find('a', class_='ar-cited')
          cited = cited_tag.text.strip() if cited_tag else "0 cited"

          print(f"Judul: {title}")
          print(f"Penulis: {author}")
          print(f"Tahun: {year}")
          print(f"Sitasi: {cited}")
          print(f"Link Google Scholar: {gs_link}")
          print("-" * 50)

      time.sleep(2)

  else:
      print(f"Gagal mengakses halaman {page}. Status code: {response.status_code}")
      time.sleep(5)