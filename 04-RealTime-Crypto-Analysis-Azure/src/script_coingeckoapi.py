import requests
import json
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime, timezone
import time

# Configuration de l'API CoinGecko
api_url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1,
    'sparkline': 'false'
}

# Configuration de l'Event Hub
connection_str = "Endpoint=sb://crypto-market-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ThbCJx4joW72u6EXIHJUcWhOTKYldHEF++AEhN8zrqQ="
event_hub_name = "crypto-market-data"

# Fonction pour envoyer les données à Event Hub
def send_data_to_event_hub():
    # Récupérer les données de l'API CoinGecko
    response = requests.get(api_url, params=params)
    data = response.json()

    # Ajouter un horodatage aux données
    timestamp = datetime.now(timezone.utc).isoformat()
    for coin in data:
        coin['timestamp'] = timestamp

    # Envoi des données à Event Hub
    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, eventhub_name=event_hub_name)
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(json.dumps(data)))
    producer.send_batch(event_data_batch)
    producer.close()

    print("Data sent to Event Hub successfully.")

# Boucle pour envoyer les données toutes les 2 minutes pendant 10 fois
for _ in range(10):
    send_data_to_event_hub()
    time.sleep(2 * 60)  # Temporisation de 2 minutes (120 secondes)

print("Finished sending data 10 times.")