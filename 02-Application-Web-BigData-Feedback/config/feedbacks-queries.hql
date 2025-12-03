
-- Créer une table externe Hive pour les retours de formation
CREATE EXTERNAL TABLE feedbacks (
  id INT,
  bootcamp STRING,
  feedback_type STRING,
  `date` STRING,
  rating INT,
  comment STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
STORED AS TEXTFILE
LOCATION '/user/hdfs/feedbacks/';

-- Charger les données depuis HDFS dans la table feedbacks
-- Exécuter cette commande dans la CLI Hive après avoir uploadé votre fichier CSV
-- LOAD DATA INPATH '/feedbacks/temp_feedback.csv' INTO TABLE feedbacks;

----------------------------------------------------------------------------------

-- Calculer la note moyenne par bootcamp
SELECT bootcamp, AVG(rating) AS moyenne
FROM feedbacks
GROUP BY bootcamp;

-- Trouver le commentaire le plus long pour chaque type de feedback
SELECT feedback_type, MAX(LENGTH(comment)) AS longueur_max_commentaire
FROM feedbacks
GROUP BY feedback_type;

-- Compter le nombre de feedbacks par bootcamp et par mois
SELECT bootcamp, MONTH(date) AS mois, COUNT(*) AS nombre_feedbacks
FROM feedbacks
GROUP BY bootcamp, MONTH(date);

-- Trouver les bootcamps ayant une note moyenne inférieure à 5
SELECT bootcamp, AVG(rating) AS moyenne
FROM feedbacks
GROUP BY bootcamp
HAVING AVG(rating) < 5;

-- Récupérer les feedbacks ayant les 5 notes les plus élevées
SELECT *
FROM feedbacks
ORDER BY rating DESC
LIMIT 5;

-- Trouver le feedback le plus récent pour chaque combinaison de bootcamp et de type de feedback
SELECT f.bootcamp, f.feedback_type, f.date, f.rating, f.comment
FROM feedbacks f
JOIN (
  SELECT bootcamp, feedback_type, MAX(date) AS max_date
  FROM feedbacks
  GROUP BY bootcamp, feedback_type
) m 
ON f.bootcamp = m.bootcamp AND f.feedback_type = m.feedback_type AND f.date = m.max_date;

-- Calculer la répartition des notes par type de feedback
SELECT feedback_type, 
       COUNT(CASE WHEN rating = 1 THEN 1 END) AS note_1,
       COUNT(CASE WHEN rating = 2 THEN 1 END) AS note_2,
       COUNT(CASE WHEN rating = 3 THEN 1 END) AS note_3,
       COUNT(CASE WHEN rating = 4 THEN 1 END) AS note_4,
       COUNT(CASE WHEN rating = 5 THEN 1 END) AS note_5,
       COUNT(CASE WHEN rating = 6 THEN 1 END) AS note_6,
       COUNT(CASE WHEN rating = 7 THEN 1 END) AS note_7
FROM feedbacks
GROUP BY feedback_type;
