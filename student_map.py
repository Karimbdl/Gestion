import folium

# Coordonnées des salles
coords = {
    "Hall rez-de-chaussée / Accueil": [43.6012547, 3.9122047],
    # Ajoutez les autres salles ici...
}

def student_map():
    mymap = folium.Map(location=[43.6012547, 3.9122047], zoom_start=18)
    for salle, coord in coords.items():
        folium.Marker(
            coord, 
            popup=f"<a href='/report?salle={salle}'>Signaler un incident</a>", 
            icon=folium.Icon(color='blue')
        ).add_to(mymap)
    return mymap._repr_html_()
