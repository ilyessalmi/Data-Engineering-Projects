##  Hive table creation and data loading scripts ##

-- Create external Hive table for feedbacks
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

-- Load data from HDFS into the feedbacks table
-- Run this command in Hive CLI after uploading your CSV file
-- LOAD DATA INPATH '/feedbacks/temp_feedback.csv' INTO TABLE feedbacks;

----------------------------------------------------------------------------------

## Analytical queries for feedback analysis ##
  
-- Calculate average rating per bootcamp
SELECT bootcamp, AVG(rating) AS moyenne
FROM feedbacks
GROUP BY bootcamp;

-- Find the longest comment for each feedback type
SELECT feedback_type, MAX(LENGTH(comment)) AS longueur_max_commentaire
FROM feedbacks
GROUP BY feedback_type;

-- Count feedbacks per bootcamp and per month
SELECT bootcamp, MONTH(date) AS mois, COUNT(*) AS nombre_feedbacks
FROM feedbacks
GROUP BY bootcamp, MONTH(date);

-- Find bootcamps with average rating below 5
SELECT bootcamp, AVG(rating) AS moyenne
FROM feedbacks
GROUP BY bootcamp
HAVING AVG(rating) < 5;

-- Get the 5 feedbacks with the highest ratings
SELECT *
FROM feedbacks
ORDER BY rating DESC
LIMIT 5;

-- Find the most recent feedback for each bootcamp and feedback type combination
SELECT f.bootcamp, f.feedback_type, f.date, f.rating, f.comment
FROM feedbacks f
JOIN (
  SELECT bootcamp, feedback_type, MAX(date) AS max_date
  FROM feedbacks
  GROUP BY bootcamp, feedback_type
) m 
ON f.bootcamp = m.bootcamp AND f.feedback_type = m.feedback_type AND f.date = m.max_date;

-- Calculate rating distribution by feedback type
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
