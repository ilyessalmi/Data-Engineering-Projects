#il est nécessaire pour que Python traite le dossier "app" comme un package  

from flask import Flask

def create_app():
    # création de l'objet app
    app = Flask(__name__)

    #Configurer Flask pour servir les fichiers statiques
    app.static_folder = 'static'

    # La clé secrète est utilisée par Flask pour crypter les données de session 
    # et les jetons CSRF (Cross-Site Request Forgery)
    app.secret_key = 'B2D!orzKuSVd$nA4&V6j26%&h8^3'
    
    # Cette ligne ci-dessous désactive les sessions dans Flask, ce qui permettra à l'application
    # de fonctionner sans clé secrète définie. déconséillé car pas une bonne pratique!!!
    """ app.config['SESSION_TYPE'] = 'null'  """
    
    # Importation du blueprint à l'intérieur de la fonction
    from .routes import bp
    app.register_blueprint(bp)

    return app