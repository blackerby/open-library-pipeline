# %%
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

# %%
df = spark.read.json(f"../first_thousand_works.json")
# %%
df.show()

# %%
df = df.select(F.col("string_field_4").alias("json"))

# %%
df.show()

# %%
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

# %%
df.show()
