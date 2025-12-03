## Flask application for feedback submission 

from flask import Blueprint, request, render_template, redirect, url_for, flash
from subprocess import Popen, PIPE
import csv

bp = Blueprint('routes', __name__)

class Feedback:
    def __init__(self, bootcamp, feedback_type, date, rating, comment):
        self.bootcamp = bootcamp
        self.feedback_type = feedback_type
        self.date = date
        self.rating = rating
        self.comment = comment


@bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page route that displays the feedback form and handles new feedback submissions.
    Saves feedback to HDFS via Hadoop and loads it into Hive.
    """
    if request.method == 'POST':
        bootcamp = request.form['formation']
        feedback_type = request.form['typeRetour']
        date = request.form['date']
        rating = int(request.form['rating'])
        comment = request.form['comments']
        consent = 'consentement' in request.form
        
        if consent:
            feedback = Feedback(bootcamp, feedback_type, date, rating, comment)

            try:
                # Save feedback to temporary CSV file
                with open('temp_feedback.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([1, bootcamp, feedback_type, date, rating, comment])

                # Upload CSV file to HDFS
                put = Popen(
                    ["hadoop", "fs", "-put", "temp_feedback.csv", "/feedbacks"],
                    stdin=PIPE,
                    bufsize=-1,
                    shell=True
                )
                put.communicate()

                # Create success flash message
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
