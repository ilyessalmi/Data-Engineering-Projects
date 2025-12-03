# Ce fichier contiendra les routes et les vues de notre application Flask
"""
Ce code définit un blueprint nommé "bp" et une route pour la page d'accueil ("/"). 
La route gère à la fois les requêtes GET et POST.

Lorsqu'un formulaire est soumis (requête POST), nous extrayons les données du formulaire,
créons une instance de la classe Feedback (que nous définirons dans "models.py")
et renvoyons un message de succès
Pour les requêtes GET, nous rendons simplement le modèle "index.html"
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, g 
from .models import Feedback
import csv
from pywebhdfs.webhdfs import PyWebHdfsClient
from pyhive import hive


bp = Blueprint('routes', __name__)

# '/' : Route pour la page d'accueil qui affiche le formulaire de retour et 
#       gère la soumission des nouveaux retours.
@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Lire le dernier ID du fichier CSV:
        last_id = get_last_id_from_csv()
        new_id = last_id + 1

        # Collecter les données du formulaire 
        bootcamp = request.form['formation']
        feedback_type = request.form['typeRetour']
        date = request.form['date']
        rating = int(request.form['rating'])
        comment = request.form['comments']
        consent = 'consentement' in request.form
        
        if consent:
            feedback = Feedback(bootcamp, feedback_type, date, rating, comment)

            # Créer la ligne de données avec le nouvel ID
            data_to_append = f"\n{new_id},{bootcamp},{feedback_type},{date},{rating},{comment}"

            # Écrire les données de feedback directement dans le fichier CSV dans HDFS
            try:                
                hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='hdfs')
                hdfs.append_file('/user/hdfs/feedbacks.csv', data_to_append.encode('utf-8'))
                
                # créer un message Flash 
                flash("Merci pour votre contribution ! votre retour a été enregistré.", "success")  

                return redirect(url_for('routes.home'))                           
            except Exception as e:
                print(f"Erreur lors de l'enregistrement du feedback : {str(e)}")
                flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")   
                return redirect(url_for('routes.home'))

        else:
            flash("Veuillez donner votre consentement pour enregistrer votre retour.", "warning")
            return redirect(url_for('routes.home'))
    
    return render_template('index.html')

def get_last_id_from_csv():
    """ Cette fonction lit le dernier ID utilisé dans le fichier CSV stocké sur HDFS """
    try:
        hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='hdfs')
        # Obrenir le contenu du fichier
        file = hdfs.read_file('user/hdfs/feedbacks.csv')  
        # Supposons que le file est de type object, decode it to a string
        file_str = file.decode('utf-8')
        # Split the file into lines and get last_line and last_id      
        last_line = file_str.strip().split('\n')[-1]
        last_id = int(last_line.split(',')[0])
        
        return last_id
        
    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {str(e)}")
        return 0



# '/feedbacks' : Route pour récupérer tous les retours (opération Read).
@bp.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    search = request.args.get('search', '').strip()
    filter_type = request.args.get('filter', '').strip()
    
    try:
        conn = hive.Connection(host="localhost", port=10000, database="lplearning")
        cursor = conn.cursor()

        query = "SELECT * FROM feedbacks"
        conditions = []

        if search:
            conditions.append(f"(bootcamp LIKE '%{search}%' OR comment LIKE '%{search}%')")

        if filter_type == 'positive':
            conditions.append("rating > 5")
        elif filter_type == 'negative':
            conditions.append("rating < 5")
        elif filter_type == 'neutral':
            conditions.append("rating = 5")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query)
        feedbacks = cursor.fetchall()
        conn.close()

        return render_template('feedbacks.html', feedbacks=feedbacks, search=search, filter=filter_type)
    
    except Exception as e:
        print(f"Erreur lors de la récupération des feedbacks depuis Hive : {str(e)}")
        flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")
        return render_template('feedbacks.html', feedbacks=[])
    

    
# '/feedbacks/<id> (GET)' : Route pour récupérer un retour spécifique (opération Read).
@bp.route('/feedbacks/<int:id>', methods=['GET'])
def get_feedback(id):
    # Récupérer un retour spécifique depuis HDFS
    try:
        conn = hive.Connection(host="localhost", port=10000, database="lplearning")
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM feedbacks WHERE id = {id}")
        feedback = cursor.fetchone()
        conn.close()
        if feedback:
            return render_template('feedback.html', feedback=feedback)
        else:
            flash(f"Le feedback avec l'ID {id} n'a pas été trouvé.", "warning")
            return redirect(url_for('routes.get_feedbacks'))
        
    except Exception as e:
        print(f"Erreur lors de la récupération du feedback depuis Hive : {str(e)}")
        flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")
        return redirect(url_for('routes.get_feedbacks'))
    


# '/feedbacks/<feedback_id> (POST)' : Route pour mettre à jour un retour spécifique (opération Update).
@bp.route('/feedbacks/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        bootcamp = request.form['formation']
        feedback_type = request.form['typeRetour']
        date = request.form['date']
        rating = int(request.form['rating'])
        comment = request.form['comments']

        try:                 
      
                   ## Mettre à jour le fichier CSV sur HDFS ##

            # Créer une instance du client PyWebHdfs
            hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='hdfs')
            
            # Utiliser la méthode read_file pour lire le contenu du fichier CSV depuis HDFS
            content = hdfs.read_file('/user/hdfs/feedbacks.csv')

            # Décoder le contenu du fichier en String
            content = content.decode('utf-8')

            # Diviser le contenu en lignes
            lines = content.split('\n')

            # Parcourir les lignes pour trouver le retour correspondant à l'ID
            updated_lines = []
            for line in lines:
                if line.strip():  # Ignorer les lignes vides
                    feedback_id, *fields = line.split(',')
                    if int(feedback_id) == id:
                        # Mettre à jour les champs du retour
                        updated_line = f"{id},{bootcamp},{feedback_type},{date},{rating},{comment}"
                        updated_lines.append(updated_line)
                    else:
                        updated_lines.append(line)

            # Joindre les lignes mises à jour en une seule chaîne
            updated_content = '\n'.join(updated_lines)

            # Écrire le contenu mis à jour dans le fichier CSV sur HDFS
            hdfs.create_file('/user/hdfs/feedbacks.csv', updated_content.encode('utf-8'), overwrite=True)
                
            # Rediriger vers la page de détails du retour avec un message de succès
            flash(f"Le feedback avec l'ID {id} a été mis à jour.", "success")
            return redirect(url_for('routes.get_feedback', id=id))

        except Exception as e:
            # Gérer les erreurs et afficher un message d'erreur
            print(f"Erreur lors de la mise à jour du feedback dans Hive : {str(e)}")
            flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")
            return redirect(url_for('routes.update_feedback', id=id))
    
    else:
        try:
            conn = hive.Connection(host="localhost", port=10000, database="lplearning")
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM feedbacks WHERE id = {id}")
            feedback = cursor.fetchone()
            conn.close()
            if feedback:
                return render_template('feedback_update.html', feedback=feedback)
            else:
                flash(f"Le feedback avec l'ID {id} n'a pas été trouvé.", "warning")
                return redirect(url_for('routes.get_feedbacks'))
        except Exception as e:
            print(f"Erreur lors de la récupération du feedback depuis Hive : {str(e)}")
            flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")
            return redirect(url_for('routes.get_feedbacks'))

        

    

# '/feedbacks/<id> (DELETE)' : Route pour supprimer un retour spécifique (opération Delete).
@bp.route('/feedbacks/<int:id>', methods=['DELETE'])
def delete_feedback(id):
    # Supprimer un retour spécifique de la base de données (HDFS)
    try:
         ## Mettre à jour le fichier CSV dans HDFS ##
        # Créer une instance du client PyWebHdfs
        hdfs = PyWebHdfsClient(host='localhost', port='9870', user_name='hdfs')
        
        # Utiliser la méthode read_file pour lire le contenu du fichier CSV depuis HDFS
        content = hdfs.read_file('/user/hdfs/feedbacks.csv')
        
        # Décoder le contenu du fichier en une chaîne de caractères
        content = content.decode('utf-8')
        
        # Diviser le contenu en lignes
        lines = content.split('\n')
        
        # Filtrer les lignes pour exclure le retour correspondant à l'ID
        updated_lines = [line for line in lines if line.strip() and int(line.split(',')[0]) != id]
        
        # Joindre les lignes restantes en une seule chaîne
        updated_content = '\n'.join(updated_lines)
        
        # Écrire le contenu mis à jour dans le fichier CSV sur HDFS
        hdfs.create_file('/user/hdfs/feedbacks.csv', updated_content.encode('utf-8'), overwrite=True)
            

        flash(f"Le feedback avec l'ID {id} a été supprimé.", "success")

    except Exception as e:
        print(f"Erreur lors de la suppression du feedback dans Hive : {str(e)}")
        flash("Une erreur est survenue. Veuillez réessayer plus tard.", "danger")

    return '', 204