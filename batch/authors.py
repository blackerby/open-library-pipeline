from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("Authors Batch").getOrCreate()
# https://stackoverflow.com/a/75921500
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED")

schema = T.StructType(
    [
        T.StructField("type", T.StringType(), True),
        T.StructField("key", T.StringType(), True),
        T.StructField("revision", T.IntegerType(), True),
        T.StructField("last_modified", T.TimestampType(), True),
        T.StructField("json", T.StringType(), True),
    ]
)

df = (
    spark.read.option("sep", "\t")
    .option("header", "true")
    .schema(schema)
    .csv("gs://olp_data_lake_open-library-pipeline/ol_dump_authors_latest.txt")
)

df = df.repartition(24)
df.write.parquet(
    "gs://olp_data_lake_open-library-pipeline/ol/authors/raw/", mode="overwrite"
)
df = spark.read.parquet("gs://olp_data_lake_open-library-pipeline/ol/authors/raw/")

json_schema = T.StructType([T.StructField("name", T.StringType(), True)])


df = df.withColumn("json", F.from_json("json", json_schema)).select(
    "type", "key", "json.name", "revision", "last_modified"
)

df.write.format("bigquery").option("writeMethod", "direct").save("open_library.authors")
