from flask import Flask, render_template, redirect, url_for, request
from student_map import student_map
from regleur_map import regleur_map

app = Flask(__name__)

# Liste des incidents (stockée en mémoire pour cet exemple)
incidents = []

@app.route('/')
def home():
    return student_map(incidents)  # Carte des étudiants

@app.route('/report', methods=['GET', 'POST'])
def report_issue():  # Renommé pour éviter la confusion
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        probleme = request.form['probleme']
        urgence = request.form['urgence']
        salle = request.form['salle']
        
        # Ajoute l'incident à la liste
        incidents.append({
            'nom': nom,
            'prenom': prenom,
            'date_naissance': date_naissance,
            'probleme': probleme,
            'urgence': urgence,
            'salle': salle
        })
        
        return redirect(url_for('home'))  # Redirige vers la page d'accueil après le signalement
    
    # Si c'est une requête GET, affiche le formulaire
    salle = request.args.get('salle')
    return render_template('report.html', salle=salle)

@app.route('/regleur')
def regleur_view():
    return regleur_map(incidents)  # Carte du régleur

if __name__ == '__main__':
    app.run(debug=True)
