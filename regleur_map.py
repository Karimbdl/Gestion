import folium
from geopy.distance import geodesic
import json

# Coordonées des salles
coords = {
    "Hall rez-de-chaussée / Accueil": [43.6012547, 3.9122047],
    # Ajoute les autres salles ici...
}

def load_incidents():
    try:
        with open('incidents.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def regleur_map(current_location):
    mymap = folium.Map(location=current_location, zoom_start=18)

    # Marqueur pour la position actuelle du régleur
    folium.Marker(
        current_location,
        popup="Vous êtes ici",
        icon=folium.Icon(color='blue')
    ).add_to(mymap)

    incidents = load_incidents()
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
        dist = calculate_distance(current_location, coord)  # Distance à la salle

        folium.Marker(
            coord,
            popup=f"{salle} - Urgence: {urgence}, Distance: {dist:.2f} m",
            icon=folium.Icon(color=color)
        ).add_to(mymap)

    return mymap._repr_html_()
