# %%
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

# %%


# %%
schema = T.StructType(
    [
        T.StructField("type", T.StringType(), True),
        T.StructField("key", T.StringType(), True),
        T.StructField("revision", T.IntegerType(), True),
        T.StructField("last_modified", T.TimestampType(), True),
        T.StructField("json", T.StringType(), True),
    ],
)

# %%
df = (
    spark.read.json(f"../first_thousand_works.json")
    # parameterize on record_type [authors, works, editions, ratings, reading-log]
    # .csv(f"ol_dump_{record_type}_latest.txt")
)
# %%
df.show()
# %%
# essential links
# https://stackoverflow.com/questions/41107835/pyspark-parse-a-column-of-json-strings
# https://stackoverflow.com/questions/38895057/reading-json-with-apache-spark-corrupt-record
# https://stackoverflow.com/questions/66053285/pyspark-corrupt-record-while-reading-json-file
# https://stackoverflow.com/questions/59246005/need-to-add-corrupt-record-column-explicitly-in-the-schema-if-you-need-to-do

# %%
df = df.select(F.col("string_field_4").alias("json"))
# %%
json_schema = T.StructType(
    [
        T.StructField("key", T.StringType(), True),
        T.StructField("title", T.StringType(), True),
        T.StructField("subjects", T.ArrayType(T.StringType()), True),
    ]
)

# %%
df.withColumn("string_field_4", F.from_json("string_field_4", json_schema)).select(
    "string_field_4.title", F.explode("string_field_4.subjects")
).show()

# %%
df.select(F.get_json_object(F.col("string_field_4"), "$.title")).show()
# %%
df.select(F.get_json_object(F.col("string_field_4"), "$.subjects")).show()
# %%
authors = df.select(F.get_json_object(F.col("string_field_4"), "$.authors"))
# %%
authors.show()
