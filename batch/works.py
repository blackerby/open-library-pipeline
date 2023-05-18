from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("Works Batch").getOrCreate()
# https://stackoverflow.com/a/75921500
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED")

to_array_udf = F.udf(lambda s: s if (s is None or s.startswith("[")) else "[" + s + "]")

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
    .schema(schema)
    .csv("gs://olp_data_lake_open-library-pipeline/ol_dump_works_latest.txt")
)

df = df.repartition(24)
df.write.parquet(
    "gs://olp_data_lake_open-library-pipeline/ol/works/raw/", mode="overwrite"
)
df = spark.read.parquet("gs://olp_data_lake_open-library-pipeline/ol/works/raw/")

df = df.select(F.col("json"))
df = df.select(
    F.get_json_object(F.col("json"), "$.key").alias("key"),
    F.get_json_object(F.col("json"), "$.title").alias("title"),
    F.get_json_object(F.col("json"), "$.type.key").alias("type"),
    F.get_json_object(F.col("json"), "$.revision").alias("revision"),
    F.get_json_object(F.col("json"), "$.created.value").alias("created"),
    F.get_json_object(F.col("json"), "$.last_modified.value").alias("last_modified"),
    F.get_json_object(F.col("json"), "$.subjects").alias("subjects"),
    F.get_json_object(F.col("json"), "$.authors[*].author.key").alias("authors"),
)

df = df.withColumn(
    "subjects", F.from_json("subjects", T.ArrayType(T.StringType()))
).select(
    "key",
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    F.explode("subjects").alias("subject"),
    "authors",
)

df = df.select(
    "key",
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    "subject",
    to_array_udf(F.col("authors")).alias("authors"),
)

df = df.withColumn(
    "authors", F.from_json("authors", T.ArrayType(T.StringType()))
).select(
    "key",
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    "subject",
    F.explode("authors").alias("author"),
)

df.write.parquet(
    "gs://olp_data_lake_open-library-pipeline/ol/works/clean/", mode="overwrite"
)
