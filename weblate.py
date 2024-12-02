import requests
import os

def fetch_weblate_languages(project_slug):
    """
    Obtiene los idiomas y sus porcentajes de traducción de un proyecto en Weblate.
    
    :param project_slug: Identificador del proyecto en Weblate.
    :return: Lista de diccionarios con la información procesada.
    """
    api_token = os.getenv("WEBLATE_API_TOKEN")
    if not api_token:
        raise ValueError("El token de la API (WEBLATE_API_TOKEN) no está configurado en las variables de entorno.")
    
    headers = {
        'Authorization': f'Token {api_token}'
    }
    url = f"https://hosted.weblate.org/api/projects/{project_slug}/languages/"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Procesar, filtrar y ordenar los idiomas
        languages = sorted(
            [
                {
                    "code": language["code"],
                    "name": language["name"],
                    "translated_percent": language["translated_percent"],
                    "weblate_url": language["url"],
                    "docs_url": f"https://flask.palletsprojects.com/{language['code']}/latest/"
                }
                for language in data if language["code"] != "en"  # Excluir el inglés
            ],
            key=lambda lang: lang["translated_percent"],  # Ordenar por porcentaje traducido
            reverse=True  # Orden descendente
        )
        
        return languages
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al conectarse a Weblate: {e}")

# Ejemplo de uso independiente
if __name__ == "__main__":
    PROJECT_SLUG = "flask"
    
    try:
        languages = fetch_weblate_languages(PROJECT_SLUG)
        for lang in languages:
            print(lang)
    except Exception as e:
        print(str(e))
