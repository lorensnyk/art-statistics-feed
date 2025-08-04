import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_sothebys():
    url = "https://www.sothebys.com/en/press"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select("article.teaser-card")[:5]
    current_month = datetime.now().strftime("%B")
    html = f'<section id="auction-highlights">\n<h2>Sotheby’s {current_month} Auction Highlights</h2>\n'
    for item in items:
        title = item.select_one(".teaser-card__title").text.strip()
        link = "https://www.sothebys.com" + item.select_one("a")["href"]
        date = item.select_one(".teaser-card__date")
        date_text = date.text.strip() if date else "No date listed"
        html += f'''
<article class="auction-highlight">
  <h3>{title}</h3>
  <p>{date_text}</p>
  <a href="{link}" target="_blank" rel="noopener">Read More</a>
</article>
'''
    html += "\n</section>"
    return html

def fetch_tate():
    url = "https://www.tate.org.uk/tate-etc"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.select("div.card--content")[:5]
    html = '<section id="tate-highlights">\n<h2>Tate Etc. Highlights</h2>\n'
    for art in articles:
        title = art.select_one("a").text.strip()
        link = "https://www.tate.org.uk" + art.select_one("a")["href"]
        html += f'''
<article class="tate-highlight">
  <h3>{title}</h3>
  <a href="{link}" target="_blank" rel="noopener">Read More</a>
</article>
'''
    html += "\n</section>"
    return html

def fetch_va():
    url = "https://www.vam.ac.uk/articles/v-and-a-magazine"
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")

    articles = soup.select("div.teaser__content")[:5]
    html = '<section id="va-highlights">\n<h2>V&A Magazine Reflections</h2>\n'
    for art in articles:
        title = art.select_one("h3").text.strip()
        link = "https://www.vam.ac.uk" + art.find("a")["href"]
        summary = art.select_one("p").text.strip() if art.select_one("p") else ""
        html += f'''
<article class="va-highlight">
  <h3>{title}</h3>
  <p>{summary}</p>
  <a href="{link}" target="_blank" rel="noopener">Read More</a>
</article>
'''
    html += "\n</section>"
    return html

if __name__ == "__main__":
    sothebys = fetch_sothebys()
    tate = fetch_tate()
    va = fetch_va()

    final_html = f"{sothebys}\n\n{tate}\n\n{va}"
    with open("art_statistics_snippet.html", "w", encoding="utf-8") as f:
        f.write(final_html)
