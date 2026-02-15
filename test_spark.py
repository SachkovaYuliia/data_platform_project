import os
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BronzePipeline") \
    .master("local[*]") \
    .getOrCreate()

customers_path = os.path.join("data", "customers")
sales_path = os.path.join("data", "sales")
profiles_path = os.path.join("data", "user_profiles", "user_profiles.json")

df_customers = spark.read.option("header", True) \
    .option("inferSchema", False) \
    .option("recursiveFileLookup", True) \
    .csv(customers_path)

df_sales = spark.read.option("header", True) \
    .option("inferSchema", False) \
    .option("recursiveFileLookup", "true") \
    .csv(sales_path)

df_profiles = spark.read.option("multiLine", False).json(profiles_path)

os.makedirs("bronze", exist_ok=True)

df_customers.write.mode("overwrite").parquet("bronze/customers")
df_sales.write.mode("overwrite").parquet("bronze/sales")
df_profiles.write.mode("overwrite").parquet("bronze/user_profiles")

print("Total customers:", df_customers.count())
print("Total sales:", df_sales.count())
print("Total profiles:", df_profiles.count())

spark.stop()
