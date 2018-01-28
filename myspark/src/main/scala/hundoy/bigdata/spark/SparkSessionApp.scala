package hundoy.bigdata.spark

import org.apache.spark.sql.SparkSession

/**
  * Created by zohar on 2018/1/28.
  */
object SparkSessionApp {
  def main(args: Array[String]): Unit = {
    val path = args(0)

    // 1.create
    val ss = SparkSession.builder().appName("SparkSessionApp").master("local[2]").getOrCreate()

    // 2.process
    val df = ss.read.json(path)
    df.show()

    // 3.close
    ss.close()
  }

}
