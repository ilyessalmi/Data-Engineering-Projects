import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# Télécharger les ressources nécessaires de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Fonction pour nettoyer les tweets
def clean_tweet(tweet):
    # Suppression des URL
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    # Suppression des mentions et hashtags
    tweet = re.sub(r'@\w+|#', '', tweet)
    # Suppression des caractères spéciaux
    tweet = re.sub(r'[^A-Za-z0-9\s]+', '', tweet)
    return tweet

# Fonction pour tokeniser les tweets
def tokenize_tweet(tweet):
    return word_tokenize(tweet)

# Combiner les stop-words en français et en anglais
stop_words_fr = set(stopwords.words('french'))
stop_words_en = set(stopwords.words('english'))
combined_stop_words = stop_words_fr.union(stop_words_en)

# Fonction pour filtrer les stop-words des tweets
def filter_stopwords(words):
    return [word for word in words if word.lower() not in combined_stop_words]

if __name__ == "__main__":
    # Lire les tweets depuis le fichier CSV
    df = pd.read_csv('tweets.csv')

    # Nettoyer les tweets
    df['Cleaned_Tweet'] = df['Tweet'].apply(clean_tweet)

    # Tokeniser les tweets nettoyés
    df['Tokenized_Tweet'] = df['Cleaned_Tweet'].apply(tokenize_tweet)

    # Filtrer les stop-words des tweets tokenisés
    df['Filtered_Tweet'] = df['Tokenized_Tweet'].apply(filter_stopwords)

    # Sauvegarder les tweets nettoyés, tokenisés et filtrés dans un nouveau fichier CSV
    df.to_csv('filtered_tweets.csv', index=False, columns=['Keyword', 'Filtered_Tweet'])

    print("Les tweets nettoyés, tokenisés et filtrés ont été sauvegardés dans le fichier filtered_tweets.csv")