import requests, pyperclip,  time, validators
from bs4 import BeautifulSoup

def main():
    prev_content = pyperclip.paste()
    while True:
        clipboard_content = pyperclip.paste()

        if clipboard_content != prev_content:
            prev_content = clipboard_content
            if validators.url(clipboard_content):
                print("Trabajando...")
                try:
                    response = requests.get(clipboard_content)
                    response.raise_for_status()
                    html_content = response.text
                except requests.exceptions.RequestException as e:
                    print(f"Error al obtener la página web: {e}")
                    time.sleep(1)
                    continue
                soup = BeautifulSoup(html_content, "html.parser")
                articles = soup.find_all("article")
                for i, article in enumerate(articles, start=1):
                    print(f"Artículo {i}:")
                    print(article.get_text())
                    print("")

            else:
                print("Trabajando...")
                time.sleep(0.5)
                print("Hmm, no veo ningún enlace aquí. ¿Qué has copiado?")

        time.sleep(1)

if __name__ == "__main__":
    main()
