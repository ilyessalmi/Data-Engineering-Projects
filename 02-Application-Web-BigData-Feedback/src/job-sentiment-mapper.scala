package com.lepont.sentiment

import org.apache.hadoop.io.{IntWritable, LongWritable, Text}
import org.apache.hadoop.mapreduce.Mapper
import scala.io.Source
import scala.util.Using

class SentimentMapper extends Mapper[LongWritable, Text, Text, IntWritable] {
  // Charger les listes de mots positifs et négatifs en mémoire
  val positiveWords: Set[String] = Using(Source.fromFile("positive_words.txt"))(_.getLines().toSet).getOrElse(Set.empty)
  val negativeWords: Set[String] = Using(Source.fromFile("negative_words.txt"))(_.getLines().toSet).getOrElse(Set.empty)

  override def map(key: LongWritable, value: Text, context: Mapper[LongWritable, Text, Text, IntWritable]#Context): Unit = {
    val comment = value.toString
    val words = comment.split("\\W+")

    val positiveCount = words.count(word => positiveWords.contains(word.toLowerCase))
    val negativeCount = words.count(word => negativeWords.contains(word.toLowerCase))

    if (positiveCount > negativeCount) {
      context.write(new Text("positif"), new IntWritable(1))
    } else if (negativeCount > positiveCount) {
      context.write(new Text("négatif"), new IntWritable(1))
    } else {
      context.write(new Text("neutre"), new IntWritable(1))
    }
  }
}
