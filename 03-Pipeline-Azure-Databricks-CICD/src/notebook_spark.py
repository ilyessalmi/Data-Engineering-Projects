# Databricks notebook source
## Chargement des données dans un DataFrame Spark et effectuer l'analyse de sentiments

from pyspark.sql import SparkSession

# Initialiser une session Spark
spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()

# Chemin vers le fichier CSV
file_path = "/FileStore/tables/filtered_tweets.csv"

# Charger le fichier CSV dans un DataFrame Spark
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Afficher le schéma du DataFrame
df.printSchema()

# Afficher les premières lignes du DataFrame
df.show()

# COMMAND ----------

# Installer TextBlob
%pip install textblob

# COMMAND ----------

# Redémarrer le kernel
dbutils.library.restartPython()

# COMMAND ----------

## Définir la fonction d'analyse de sentiments et la UDF
from textblob import TextBlob
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Définir une fonction pour analyser les sentiments
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Enregistrer la fonction comme une UDF
sentiment_udf = udf(analyze_sentiment, StringType())

# Appliquer la UDF à la colonne 'Filtered_Tweet'
df_with_sentiment = df.withColumn("Sentiment", sentiment_udf(df["Filtered_Tweet"]))

# Afficher les résultats
df_with_sentiment.show()

# COMMAND ----------

## Analyser les résultats de sentiment

# Afficher quelques exemples de tweets avec leurs sentiments
df_with_sentiment.select("Keyword", "Filtered_Tweet", "Sentiment").show(10, truncate=False)

# Compter le nombre de tweets par sentiment
df_with_sentiment.groupBy("Sentiment").count().show()

# Compter le nombre de tweets par mot-clé et par sentiment
df_with_sentiment.groupBy("Keyword", "Sentiment").count().show()

# COMMAND ----------

## Sauvegarder les résultats dans un fichier CSV

# Chemin où sauvegarder le fichier CSV
output_path = "/FileStore/tables/sentiment_analysis_results.csv"

df_with_sentiment.show()

# Sauvegarder le DataFrame avec les sentiments dans un fichier CSV
# df_with_sentiment.select("Keyword", "Filtered_Tweet", "Sentiment").write.mode("overwrite").csv(output_path, header=True)
df_with_sentiment.coalesce(1).write.mode("overwrite").csv(output_path, header=True)

print(f"Les résultats de l'analyse de sentiments ont été sauvegardés dans {output_path}")

# COMMAND ----------

# Lire le fichier CSV "sentiment_analysis_results.csv" 

file_path = "/FileStore/tables/sentiment_analysis_results.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
df.show()
