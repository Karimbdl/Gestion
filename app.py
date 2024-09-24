import folium
from flask import Flask, render_template, redirect, url_for, request
from geopy.distance import geodesic
import random
import networkx as nx
import json
import os
from datetime import datetime
from student_map import student_map

app = Flask(__name__)

# Coordonnées des salles
coords = {
    "Hall rez-de-chaussée / Accueil": [43.6012547, 3.9122047],
    "Salle 105": [43.6011629, 3.9121272],
    "Salle 103": [43.6011629, 3.9121250],
    "Salle 108": [43.6011794, 3.9121655],
    # Ajoutez d'autres salles ici...
}

# Créer un graphe
graph = nx.Graph()
graph.add_edges_from([
    ("Hall rez-de-chaussée / Accueil", "Salle 105"),
    ("Salle 105", "Salle 103"),
    ("Hall rez-de-chaussée / Accueil", "Salle 108"),
    # Ajoutez d'autres connexions ici...
])

# Liste des incidents
incidents = []

def get_current_position():
    # Simule une position aléatoire proche de la salle
    lat_offset = random.uniform(-0.0001, 0.0001)
    lon_offset = random.uniform(-0.0001, 0.0001)
    return [43.6012547 + lat_offset, 3.9122047 + lon_offset]

def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

def find_path(start, end):
    # Trouver le chemin le plus court dans le graphe
    return nx.shortest_path(graph, source=start, target=end)

def regleur_map():
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

    # Exemple d'affichage du chemin entre deux salles
    if len(incidents) > 0:
        start_salle = incidents[0]['salle']
        end_salle = "Salle 105"  # Choisissez la salle de destination
        path = find_path(start_salle, end_salle)
        
        path_coords = [coords[salle] for salle in path]
        folium.PolyLine(locations=path_coords, color='blue', weight=5, opacity=0.7).add_to(mymap)

    return mymap._repr_html_()

@app.route('/')
def home():
    return student_map()

@app.route('/report', methods=['GET', 'POST'])
def report_issue():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        probleme = request.form['probleme']
        urgence = request.form['urgence']
        
        incident = {
            'etudiant': {'nom': nom, 'prenom': prenom, 'date_naissance': date_naissance},
            'salle': request.form['salle'],
            'probleme': probleme,
            'urgence': urgence,
            'date_signalement': datetime.now().isoformat()
        }
        incidents.append(incident)

        # Enregistrer l'incident dans un fichier JSON
        with open('incidents.json', 'w') as f:
            json.dump(incidents, f)

        return redirect(url_for('home'))  # Redirige vers la page d'accueil après le signalement
    
    salle = request.args.get('salle')
    return render_template('report.html', salle=salle)

@app.route('/regleur', methods=['GET', 'POST'])
def regleur_view():
    if request.method == 'POST':
        # Authentification du régleur
        nom = request.form['nom']
        prenom = request.form['prenom']
        poste = request.form['poste']
        date_naissance = request.form['date_naissance']
        
        # Vous pouvez stocker ces informations si nécessaire

        return regleur_map()  # Afficher la carte du régleur
    
    return render_template('regleur_auth.html')  # Formulaire d'authentification

if __name__ == '__main__':
    app.run(debug=True)
