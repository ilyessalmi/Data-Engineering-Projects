import tweepy
import csv
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Clés d'API obtenues de Twitter Developer Platform
api_key = os.getenv('API_KEY')
api_key_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

# Utilisation de l'API v2 de Twitter
client = tweepy.Client(bearer_token=bearer_token)


def get_tweets(keyword, max_results=10, lang='en', seen_ids=set()):
    try:
        # Utilisation de l'API v2 de Twitter pour rechercher des tweets en langue spécifique
        response = client.search_recent_tweets(
            query=f"{keyword} lang:{lang}",
            max_results=max_results,
            tweet_fields=['context_annotations', 'created_at'],
            expansions=['author_id']
        )
        tweets = response.data
        new_tweets = []
        if tweets is not None:
            for tweet in tweets:
                if tweet.id not in seen_ids:
                    seen_ids.add(tweet.id)
                    new_tweets.append(tweet)
                else:
                    print(f"Duplicate tweet found: {tweet.id}")
            return new_tweets
        else:
            print(f"Aucun tweet trouvé pour le mot-clé : {keyword}")
            return []
    except tweepy.TweepyException as e:
        print(f"Erreur lors de la récupération des tweets : {e}")
        return []


if __name__ == "__main__":
    # Mots-clés pour la recherche
    keywords = ["#JO2024", "#Macron", "#Inflation", "#NBAFinals", "#UCLfinal", "#Bitcoin", "#dataengineering"]
    all_tweets = []
    seen_ids = set()

    # Fetch tweets in French
    for keyword in keywords:
        print(f"Fetching tweets for keyword: {keyword} in French")
        tweets = get_tweets(keyword, lang="fr", seen_ids=seen_ids)
        for tweet in tweets:
            all_tweets.append([keyword, tweet.text])

    # Fetch tweets in English
    for keyword in keywords:
        print(f"Fetching tweets for keyword: {keyword} in English")
        tweets = get_tweets(keyword, lang="en", seen_ids=seen_ids)
        for tweet in tweets:
            all_tweets.append([keyword, tweet.text])

    # Sauvegarder les tweets dans un fichier CSV
    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Keyword", "Tweet"])
        writer.writerows(all_tweets)

    print("Les tweets ont été sauvegardés dans le fichier tweets.csv")