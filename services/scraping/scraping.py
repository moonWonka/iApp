import requests
from bs4 import BeautifulSoup
from models.entities import Noticia


def extraer_noticias_araucaniadiario(max_articulos: int = 50) -> list[Noticia]:
    base_url: str = "https://araucaniadiario.cl/default/listar_contenido?p="
    noticias: list[Noticia] = []
    pagina: int = 1

    while len(noticias) < max_articulos:
        print(f"📄 Araucanía Diario: Extrayendo página {pagina}...")
        url: str = f"{base_url}{pagina}"
        response = requests.get(url)
        print(f"⏱️ Tiempo respuesta: {response.elapsed.total_seconds()} segundos")
        soup = BeautifulSoup(response.content, 'html.parser')

        contenedor = soup.find("div", class_="lista-contenido")
        if not contenedor:
            print(f"⚠️ No se encontró contenido en la página {pagina}")
            break

        articulos = contenedor.find_all("article", class_="post__noticia")

        for articulo in articulos:
            if len(noticias) >= max_articulos:
                break

            titulo_tag = articulo.find("h2", class_="post__titulo")
            titulo = titulo_tag.a.text.strip() if titulo_tag and titulo_tag.a else "Sin título"

            fecha_tag = articulo.find("span", class_="fecha")
            fecha = fecha_tag.text.strip() if fecha_tag else "Sin fecha"

            descripcion_tag = articulo.find("p", class_="post__detalle")
            descripcion = descripcion_tag.text.strip() if descripcion_tag else "Sin descripción"

            noticias.append(Noticia(
                titulo=titulo,
                fecha=fecha,
                url=url,
                fuente="Araucanía Diario",
                descripcion=descripcion
            ))

        pagina += 1

    return noticias

def extraer_noticias_elperiodico(max_articulos: int = 50) -> list[Noticia]:
    base_url: str = "https://www.elperiodico.cl/category/temuco/page/"
    noticias: list[Noticia] = []
    pagina: int = 1

    while len(noticias) < max_articulos:
        print(f"📄 El Periódico: Extrayendo página {pagina}...")
        url: str = f"{base_url}{pagina}"
        response = requests.get(url)
        print(f"⏱️ Tiempo respuesta: {response.elapsed.total_seconds()} segundos")
        soup = BeautifulSoup(response.content, "html.parser")

        articulos = soup.select("div.post-col")

        if not articulos:
            print("⚠️ No se encontraron artículos.")
            break

        for articulo in articulos:
            if len(noticias) >= max_articulos:
                break

            titulo_tag = articulo.select_one("h2.entry-title a")
            titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"

            fecha_tag = articulo.select_one("div.date a")
            fecha = fecha_tag.text.strip() if fecha_tag else "Sin fecha"

            desc_tag = articulo.select_one("div.entry-content p")
            descripcion = desc_tag.text.strip() if desc_tag else "Sin descripción"

            noticias.append(Noticia(
                titulo=titulo,
                fecha=fecha,
                url=url,
                fuente="El Periódico",
                descripcion=descripcion
            ))

        pagina += 1

    return noticias