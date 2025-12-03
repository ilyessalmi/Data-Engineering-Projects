from azure.eventhub import EventHubConsumerClient

# Configuration de l'Event Hub
connection_str = "Endpoint=sb://crypto-market-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ThbCJx4joW72u6EXIHJUcWhOTKYldHEF++AEhN8zrqQ="
event_hub_name = "crypto-market-data"
consumer_group = "$Default"

def on_event(partition_context, event):
    # Imprimer les données de l'événement
    print("Received event: {}".format(event.body_as_str()))
    # Mettre à jour le point de contrôle pour le partition context
    partition_context.update_checkpoint(event)

# Créer un client Event Hub Consumer
client = EventHubConsumerClient.from_connection_string(
    conn_str=connection_str,
    consumer_group=consumer_group,
    eventhub_name=event_hub_name
)

try:
    # Commencer à recevoir les événements
    with client:
        client.receive(
            on_event=on_event,
            starting_position="-1"  # "-1" pour commencer à lire depuis le début
        )
except KeyboardInterrupt:
    print("Stopped receiving.")
finally:
    # Fermer le client
    client.close()