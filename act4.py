import requests, pyperclip,  os,  time, validators
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def main():
    prev_content = pyperclip.paste()
    while True:
        clipboard_content = pyperclip.paste()
        
        if clipboard_content != prev_content:
            prev_content = clipboard_content
            if validators.url(clipboard_content):
                print("El contenido del portapapeles es un enlace válido")
                url = clipboard_content
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    pdf_links = soup.find_all("a", href=lambda href: href and href.lower().endswith(".pdf"))
                    
                    if not pdf_links:
                        print("No se encontraron PDFs en el sitio web.")
                        continue
                    folder = urlparse(url).netloc.replace("www.", "")
                    if not os.path.exists(folder):
                        print("Creando carpeta...")
                        time.sleep(1)
                        print("Descargando...")
                        os.makedirs(folder)

                    for link in pdf_links:
                        pdf_url = urljoin(url, link.get("href"))
                        try:
                            pdf_response = requests.get(pdf_url)
                            pdf_response.raise_for_status()
                            filename = os.path.join(folder, os.path.basename(pdf_url))
                            with open(filename, "wb") as pdf_file:
                                pdf_file.write(pdf_response.content)
                            
                            print(f"PDF guardado como '{filename}' ")
                        except requests.exceptions.RequestException as e:
                            print(f"Error al descargar el PDF: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Error al obtener los datos del sitio: {e}")
            else:
                print("Error de navegación: el contenido del portapapeles no es un enlace.")
        
        time.sleep(1)

if __name__ == "__main__":
    main()