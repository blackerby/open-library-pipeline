# %%
import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.types as T
import pyspark.sql.functions as F

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

# %%
df = spark.read.json(f"../first_thousand_works.json")
df = df.select(F.col("string_field_4").alias("json"))

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

# %%
subjects_schema = T.ArrayType(T.StringType())
# %%
df_subjects = df.withColumn(
    "subjects", F.from_json("subjects", subjects_schema)
).select(
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    F.explode("subjects").alias("subject"),
    F.col("authors"),
)

# %%
df_subjects.show()
# %%
to_array_udf = F.udf(lambda s: s if s.startswith("[") else "[" + s + "]")

# %%
new_df = df_subjects.select(
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    "subject",
    to_array_udf(F.col("authors")).alias("authors"),
)
# %%
new_df.show()
# %%
authors_schema = T.ArrayType(T.StringType())
# %%
df_authors = new_df.withColumn(
    "authors", F.from_json("authors", authors_schema)
).select(
    "title",
    "type",
    "revision",
    "created",
    "last_modified",
    "subject",
    F.explode_outer("authors").alias("author"),
)
# %%
df_authors.show()

# %%
