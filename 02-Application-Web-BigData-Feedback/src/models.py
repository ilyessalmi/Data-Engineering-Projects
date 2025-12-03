# Ce fichier contiendra les modèles de données de notre application.

# Ce code définit une classe Feedback qui représente un retour d'apprenant

class Feedback:
    def __init__(self, bootcamp, feedback_type, date, rating, comment):
        self.bootcamp = bootcamp
        self.feedback_type = feedback_type
        self.date = date
        self.rating = rating
        self.comment = comment      