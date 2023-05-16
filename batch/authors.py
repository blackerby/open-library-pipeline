import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types

# stub to avoid warnings
record_type = "author"

# might not use all of these
from pyspark.sql.functions import col, explode, from_json, explode_outer

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

schema = types.StructType(
    [
        types.StructField("type", types.StringType(), True),
        types.StructField("key", types.StringType(), True),
        types.StructField("revision", types.IntegerType(), True),
        types.StructField("last_modified", types.TimestampType(), True),
        types.StructField("json", types.StringType(), True),
    ]
)

df = (
    spark.read.option("sep", ",")
    .option("header", "true")
    .schema(schema)
    # parameterize on record_type [authors, works, editions, ratings, reading-log]
    .csv(f"ol_dump_{record_type}_latest.txt")
)

df = df.repartition(24)
df.write.parquet(f"ol/{record_type}/latest", mode="overwrite")
df = spark.read.parquet(f"ol/{record_type}/latest")

# this will vary depending on record_type. this is for authors
json_schema = types.StructType([types.StructField("name", types.StringType(), True)])

# this will vary depending on record_type. this is for authors
df.withColumn("json", from_json("json", json_schema)).select(
    "type", "key", "json.name", "revision", "last_modified"
).show()
