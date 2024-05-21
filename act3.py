import requests, pyperclip,  time, validators
from bs4 import BeautifulSoup

def scrape_articles(url, limit=None):
    articles_list = []
    page_number = 1

    while True:
        try:
            response = requests.get(url.format(page_number))
            response.raise_for_status()
            html_content = response.text
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página web: {e}")
            return articles_list
        
        soup = BeautifulSoup(html_content, "html.parser")
        articles = soup.find_all("article")

        if not articles:
            print("No se encontraron más artículos en la página.")
            break
        for article in articles:
            articles_list.append(article.get_text())
            if limit is not None and len(articles_list) >= limit:
                return articles_list

        page_number += 1
    return articles_list

def main():
    prev_content = None
    while True:
        clipboard_content = pyperclip.paste()

        if clipboard_content != prev_content:
            prev_content = clipboard_content
            if validators.url(clipboard_content):
                articles = scrape_articles(clipboard_content, limit=10)
                if articles:
                    print("Contenido de los artículos obtenidos:")
                    for i, article in enumerate(articles, start=1):
                        print(f"Artículo {i}:")
                        print(article)
                        print("")
                else:
                    print("No se obtuvieron artículos.")
            else:
                print("La URL en el portapapeles no es válida.")

        time.sleep(1)

if __name__ == "__main__":
    main()
