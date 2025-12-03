from flask import Blueprint, request, render_template, redirect, url_for, flash
from subprocess import Popen, PIPE
import csv

# Créer un blueprint pour les routes de l'application
bp = Blueprint('routes', __name__)


class Feedback:
    """
    Classe pour représenter un retour de formation.
    Stocke les informations du retour utilisateur.
    """
    def __init__(self, bootcamp, feedback_type, date, rating, comment):
        self.bootcamp = bootcamp
        self.feedback_type = feedback_type
        self.date = date
        self.rating = rating
        self.comment = comment


@bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Route pour la page d'accueil qui affiche le formulaire de retour et 
    gère la soumission des nouveaux retours.
    
    Méthode GET : Affiche le formulaire de feedback
    Méthode POST : Traite la soumission du formulaire et enregistre le feedback
    
    Processus :
    1. Récupère les données du formulaire
    2. Crée un objet Feedback
    3. Sauvegarde les données dans un fichier CSV temporaire
    4. Upload le fichier CSV dans HDFS via Hadoop
    5. Le fichier est ensuite chargé dans la table Hive
    """
    
    if request.method == 'POST':
        # Récupérer les données du formulaire
        bootcamp = request.form['formation']
        feedback_type = request.form['typeRetour']
        date = request.form['date']
        rating = int(request.form['rating'])
        comment = request.form['comments']
        
        # Vérifier que l'utilisateur a donné son consentement
        consent = 'consentement' in request.form
        
        if consent:
            # Créer un objet Feedback avec les données du formulaire
            feedback = Feedback(bootcamp, feedback_type, date, rating, comment)

            try:
                # Enregistrer le retour dans un fichier CSV temporaire
                with open('temp_feedback.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    # Écrire une ligne avec l'ID et les données du feedback
                    writer.writerow([1, bootcamp, feedback_type, date, rating, comment])

                # Charger le fichier CSV dans HDFS via la commande Hadoop
                # Utiliser Popen pour exécuter la commande Hadoop en arrière-plan
                put = Popen(
                    ["hadoop", "fs", "-put", "temp_feedback.csv", "/feedbacks"],
                    stdin=PIPE,
                    bufsize=-1,
                    shell=True
                )
                # Attendre la fin de l'exécution de la commande Hadoop
                put.communicate()

                # Créer un message Flash pour confirmer l'enregistrement du retour
                flash("Merci pour votre contribution ! votre retour a été enregistré.", "success")
                return redirect(url_for('routes.home'))
                
            except Exception as e:
                # Afficher un message d'erreur en cas de problème
                print(f"Erreur lors de l'enregistrement du feedback : {str(e)}")
                flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")
                return redirect(url_for('routes.home'))

        else:
            # Afficher un message d'avertissement si l'utilisateur n'a pas donné son consentement
            flash("Veuillez donner votre consentement pour enregistrer votre retour.", "warning")
            return redirect(url_for('routes.home'))
    
    # Afficher le template HTML du formulaire pour une requête GET
    return render_template('index.html')
