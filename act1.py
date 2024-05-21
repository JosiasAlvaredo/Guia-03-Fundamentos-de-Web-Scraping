import requests, pyperclip,  os,  time, validators
from bs4 import BeautifulSoup

def main():
    prev_content = pyperclip.paste()
    accum = 0
    while True:
        clipboard_content = pyperclip.paste()

        if clipboard_content != prev_content:
            prev_content = clipboard_content
            
            if validators.url(clipboard_content):
                print("Descargando...")
                try:
                    data = requests.get(clipboard_content)
                    data.raise_for_status()
                    soup = BeautifulSoup(data.text, "html.parser")
                    soup_encoded = soup.encode()

                    while os.path.exists(f"codigo {accum}.txt"):
                        accum += 1
                    with open(f"codigo {accum}.txt", "wb") as file:
                        file.write(soup_encoded)

                    print(f"Datos guardados exitosamente en codigo {accum}.txt")
                except requests.exceptions.RequestException as e:
                    print(f"Error al obtener los datos: {e}")
            else:
                print("Hmm, no veo ningún enlace aquí. ¿Qué has copiado?")
        
        time.sleep(1)

if __name__ == "__main__":
    main()