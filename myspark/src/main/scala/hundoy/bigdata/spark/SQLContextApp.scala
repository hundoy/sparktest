package hundoy.bigdata.spark

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SQLContext

/**
  * Created by zohar on 2018/1/28.
  */
object SQLContextApp {
  def main(args: Array[String]): Unit = {
    val path = args(0)

    // 1. CCC -> Spark Conf  -> Spark Context -> SQLContext
    val conf = new SparkConf()
    conf.setAppName("SQLContextApp").setMaster("local[2]")
    val sc = new SparkContext(conf)
    val sqlContext = new SQLContext(sc)

    // 2. process
//    val path = "D:\\work\\lib\\spark-2.2.1-bin-2.6.0-cdh5.7.0\\examples\\src\\main\\resources\\people.json"
    val df = sqlContext.read.format("json").load(path)
    df.printSchema()
    df.show()

    // 3. close
    sc.stop()
  }

}
