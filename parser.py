from bs4 import BeautifulSoup
import logging

def parse_publication(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    publications = []

    for pub in soup.select(".ar-list-item"):
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

            publications.append({
                "Title": title,
                "Authors": authors,
                "Publication": pub_details,
                "Year": year,
                "Citations": citations,
                "Google Scholar Link": gs_link
            })
        except Exception as e:
            logging.error(f"❌ Error parsing publication: {str(e)}")
    
    return publications
