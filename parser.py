from bs4 import BeautifulSoup

def parse_publication(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    publications = []

    for pub in soup.select(".ar-list-item"):
        title = pub.select_one(".title").text.strip() if pub.select_one(".title") else "N/A"
        authors = pub.select_one(".authors").text.strip() if pub.select_one(".authors") else "N/A"
        year = pub.select_one(".year").text.strip() if pub.select_one(".year") else "N/A"
        citations = pub.select_one(".citations").text.strip() if pub.select_one(".citations") else "0"
        
        gs_link_element = pub.select_one("a[href*='scholar.google.com']")
        gs_link = gs_link_element["href"] if gs_link_element else "N/A"

        publications.append({
            "Title": title,
            "Authors": authors,
            "Year": year,
            "Citations": citations,
            "Google Scholar Link": gs_link
        })
    
    return publications
