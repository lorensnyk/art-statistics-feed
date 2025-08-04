import requests
from bs4 import BeautifulSoup

def fetch_tate():
    url = "https://www.tate.org.uk/tate-etc"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tate_html = "<h2>Tate Etc. Highlights</h2>\n"
    cards = soup.select("div.card__content")[:5]  # ← LIMIT TO 5

    for card in cards:
        title_tag = card.select_one("h2.card__title")
        summary_tag = card.select_one("p.card__description")

        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.find("a")
            href = link["href"] if link and link.has_attr("href") else "#"
            full_url = f"https://www.tate.org.uk{href}" if href.startswith("/") else href
            tate_html += f'<p><strong><a href="{full_url}" target="_blank">{title}</a></strong></p>\n'
        if summary_tag:
            summary = summary_tag.get_text(strip=True)
            tate_html += f"<p>{summary}</p>\n"

    return tate_html


def generate_html():
    html_content = "<html><body>\n"
    html_content += fetch_tate()
    html_content += "</body></html>"

    with open("art_statistics_snippet.html", "w", encoding="utf-8") as f:
        f.write(html_content)


if __name__ == "__main__":
    generate_html()
