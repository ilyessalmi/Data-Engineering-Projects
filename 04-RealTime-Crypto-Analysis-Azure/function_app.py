import logging
import azure.functions as func
import requests
import json
import os
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime

# Initialisation de l'application Azure Functions
app = func.FunctionApp()

# Fonction pour ingérer les données historiques (exécutée manuellement ou très rarement)
@app.function_name(name="IngestHistoricalCryptoData")
@app.route(route="ingest-historical-crypto-data", auth_level=func.AuthLevel.FUNCTION)
def ingest_historical_crypto_data(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fonction déclenchée pour l\'ingestion des données historiques de crypto-monnaies.')

    # Liste des crypto-monnaies à traiter
    coins = ['bitcoin', 'ethereum']
    
    for coin in coins:
        try:
            # Construction de l'URL pour récupérer les données historiques
            url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=90&interval=daily'
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Ajout de métadonnées aux données historiques
            data['type'] = 'historical'
            data['coin'] = coin
            data['timestamp'] = datetime.utcnow().isoformat()
            
            # Récupération de la chaîne de connexion Event Hub depuis les variables d'environnement
            event_hub_connection_string = os.environ["EventHubConnectionString"]
            event_hub_name = "crypto-market-data"
            
            # Envoi des données à Event Hub
            send_to_event_hub(data, event_hub_connection_string, event_hub_name)
            
            logging.info(f"Données historiques envoyées à Event Hub pour {coin}")
        except Exception as e:
            logging.error(f"Erreur lors du traitement des données historiques de {coin}: {str(e)}")

    return func.HttpResponse("Ingestion des données historiques de crypto-monnaies terminée.", status_code=200)

# Fonction pour ingérer les données actuelles (exécutée toutes les 5 minutes)
@app.function_name(name="IngestCurrentCryptoData")
@app.schedule(schedule="0 */5 * * * *", arg_name="mytimer", run_on_startup=True, use_monitor=False)
def ingest_current_crypto_data(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.info('Le minuteur est en retard!')
    
    logging.info('Fonction exécutée pour l\'ingestion des données actuelles de crypto-monnaies.')

    # Liste des crypto-monnaies à traiter
    coins = ['bitcoin', 'ethereum']
    
    for coin in coins:
        try:
            # Construction de l'URL pour récupérer les données actuelles
            url = f'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}&order=market_cap_desc&per_page=1&page=1&sparkline=false'
            response = requests.get(url)
            response.raise_for_status()
            
            data = response.json()[0]  # Prise du premier (et unique) élément du tableau

            # Ajout de métadonnées aux données actuelles
            data['type'] = 'current'
            data['timestamp'] = datetime.utcnow().isoformat()

            # Récupération de la chaîne de connexion Event Hub depuis les variables d'environnement
            event_hub_connection_string = os.environ["EventHubConnectionString"]
            event_hub_name = "crypto-market-data"
            
            # Envoi des données à Event Hub
            send_to_event_hub(data, event_hub_connection_string, event_hub_name)
            
            logging.info(f"Données actuelles envoyées à Event Hub pour {coin}")

        except Exception as e:
            logging.error(f"Erreur lors du traitement des données actuelles de {coin}: {str(e)}")

# Fonction pour envoyer les données à Event Hub
def send_to_event_hub(data, connection_string, event_hub_name):
    try:
        # Création d'un producteur Event Hub
        producer = EventHubProducerClient.from_connection_string(connection_string, eventhub_name=event_hub_name)
        with producer:
            # Création d'un lot d'événements
            batch = producer.create_batch()
            # Ajout des données au lot
            batch.add(EventData(json.dumps(data)))
            # Envoi du lot à Event Hub
            producer.send_batch(batch)
        logging.info(f"Données envoyées à Event Hub pour {data.get('coin', 'unknown')}")
    except Exception as e:
        logging.error(f"Erreur lors de l'envoi des données à Event Hub : {str(e)}")