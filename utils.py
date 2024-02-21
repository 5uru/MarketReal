from geopy.geocoders import Nominatim
import sqlite3


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


def get_location_details(city_name):
    create_table()  # Assurez-vous que la table existe
    conn = sqlite3.connect("geo.db")
    c = conn.cursor()

    # Vérifier si la ville existe déjà dans la base de données
    c.execute("SELECT location FROM locations WHERE city = ?", (city_name,))
    row = c.fetchone()
    if row:
        conn.close()
        return row[0]  # Retourner les informations de localisation

    # Initialiser l'API Nominatim
    geolocator = Nominatim(user_agent="geoapiExercises")
    location_query = f"{city_name}, Benin"

    if location := geolocator.geocode(location_query):
        location_details = geolocator.reverse(
            [location.latitude, location.longitude], language="fr"
        )
        address = location_details.address

        # Enregistrer les détails de localisation dans la base de données
        c.execute(
            "INSERT INTO locations (city, location) VALUES (?, ?)", (city_name, address)
        )
        conn.commit()
        conn.close()
        return address
    else:
        conn.close()
        return None


# Tester la fonction
print(get_location_details("Ouesse"))
