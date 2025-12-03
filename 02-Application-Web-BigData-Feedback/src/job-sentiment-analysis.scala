package com.lepont.sentiment

import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.io.{IntWritable, Text}
import org.apache.hadoop.mapreduce.Job
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat

object SentimentAnalysis {
  def main(args: Array[String]): Unit = {
    val conf = new Configuration()
    val fs = FileSystem.get(conf)
    val outputPath = new Path(args(1))

    // Supprimer le répertoire de sortie s'il existe
    if (fs.exists(outputPath)) {
      fs.delete(outputPath, true)
    }

    val job = Job.getInstance(conf, "Sentiment Analysis")
    job.setJarByClass(this.getClass)
    job.setMapperClass(classOf[SentimentMapper])
    job.setReducerClass(classOf[SentimentReducer])
    job.setOutputKeyClass(classOf[Text])
    job.setOutputValueClass(classOf[IntWritable])
    FileInputFormat.addInputPath(job, new Path(args(0)))
    FileOutputFormat.setOutputPath(job, outputPath)
    System.exit(if (job.waitForCompletion(true)) 0 else 1)
  }
}
