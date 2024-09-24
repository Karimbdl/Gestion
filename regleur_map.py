import folium
from geopy.distance import geodesic
import random

# Coordonées des salles
coords = {
    "Hall rez-de-chaussée / Accueil": [43.6012547, 3.9122047],
    # Ajoutez les autres salles ici...
}

def get_current_position():
    # Simule une position aléatoire proche de la salle
    lat_offset = random.uniform(-0.0001, 0.0001)
    lon_offset = random.uniform(-0.0001, 0.0001)
    return [43.6012547 + lat_offset, 3.9122047 + lon_offset]

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def regleur_map(incidents):
    mymap = folium.Map(location=[43.6012547, 3.9122047], zoom_start=18)
    current_position = get_current_position()  # Position actuelle du régleur
    for incident in incidents:
        salle = incident['salle']
        urgence = incident['urgence']
        color = 'green'  # Couleur par défaut

        # Changez la couleur en fonction de l'urgence
        if urgence == 'haute':
            color = 'red'
        elif urgence == 'moyenne':
            color = 'orange'

        coord = coords[salle]
        dist = calculate_distance(current_position, coord)

        folium.Marker(
            coord,
            popup=f"{salle} - Urgence: {urgence}, Distance: {dist:.2f} m",
            icon=folium.Icon(color=color)
        ).add_to(mymap)

    return mymap._repr_html_()
