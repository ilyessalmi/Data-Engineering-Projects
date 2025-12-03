package com.lepont.sentiment

import org.apache.hadoop.io.{IntWritable, Text}
import org.apache.hadoop.mapreduce.Reducer
import scala.jdk.CollectionConverters._

class SentimentReducer extends Reducer[Text, IntWritable, Text, IntWritable] {
  override def reduce(key: Text, values: java.lang.Iterable[IntWritable], context: Reducer[Text, IntWritable, Text, IntWritable]#Context): Unit = {
    // Somme des valeurs pour chaque clé (positif, négatif, neutre)
    val sum = values.asScala.foldLeft(0)(_ + _.get)
    context.write(key, new IntWritable(sum))
  }
}


