import sqlite3
from urllib.parse import urlencode

import requests


def create_table():
    """Créer la table de localisation si elle n'existe pas."""
    conn = sqlite3.connect("geo.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS locations
                 (city TEXT PRIMARY KEY, location TEXT)"""
    )
    conn.commit()
    conn.close()


def find_addresses(city):
    """

    :param city:

    """
    # Encoder les paramètres de la requête
    params = urlencode({"q": f"{city}, Benin", "format": "json"})

    # Construire l'URL de la requête
    base_url = "https://nominatim.openstreetmap.org/search"
    complete_url = f"{base_url}?{params}"

    # Définir les en-têtes pour respecter la politique d'utilisation de Nominatim
    headers = {"User-Agent": "MarketReal. Email: jonathan_suru@proton.me"}

    # Envoyer la requête et récupérer la réponse
    response = requests.get(complete_url, headers=headers)

    # Convertir la réponse en JSON
    results = response.json()

    return [result["display_name"] for result in results]


def get_location_details(city_name):
    """

    :param city_name:

    """
    create_table()  # Assurez-vous que la table existe
    conn = sqlite3.connect("geo.db")
    c = conn.cursor()

    # Vérifier si la ville existe déjà dans la base de données
    c.execute("SELECT location FROM locations WHERE city = ?", (city_name,))
    if row := c.fetchone():
        conn.close()
        return row[0]  # Retourner les informations de localisation

    if address := find_addresses(city_name):
        address_str = "\n".join(
            address
        )  # Utilisez "\n" pour séparer les adresses par des lignes
        print(address_str)
        # Enregistrer les détails de localisation dans la base de données
        c.execute(
            "INSERT INTO locations (city, location) VALUES (?, ?)",
            (city_name, address_str),
        )
        conn.commit()
        conn.close()
        return str(address)
    else:
        conn.close()
        return None


# Tester la fonction
print(get_location_details("Ouesse"))
