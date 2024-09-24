import folium

# Coordonées des salles
coords = {
    "Hall rez-de-chaussée / Accueil": [43.6012547, 3.9122047],
    # Ajoutez les autres salles ici...
}

def student_map(incidents):
    mymap = folium.Map(location=[43.6012547, 3.9122047], zoom_start=18)
    for salle, coord in coords.items():
        folium.Marker(
            coord, 
            popup=f"<a href='/report?salle={salle}'>Signaler un incident</a><br><a href='/regleur'>Voir la carte du régleur</a>", 
            icon=folium.Icon(color='blue')
        ).add_to(mymap)

    return mymap._repr_html_()
