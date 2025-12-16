# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d5c2ab53-a721-42c1-8b28-07f0079cf878",
# META       "default_lakehouse_name": "Alake",
# META       "default_lakehouse_workspace_id": "7dd85790-2e04-4e40-90a7-f20f50640ed8",
# META       "known_lakehouses": [
# META         {
# META           "id": "d5c2ab53-a721-42c1-8b28-07f0079cf878"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

table_name = "sales"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *

table_name = "sales"

schema = StructType([
    StructField("SalesOrderNumber", StringType(), True),
    StructField("SalesOrderLineNumber", IntegerType(), True),
    StructField("OrderDate", StringType(), True),
    StructField("CustomerName", StringType(), True),
    StructField("EmailAddress", StringType(), True),
    StructField("Item", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("UnitPrice", DoubleType(), True),
    StructField("TaxAmount", DoubleType(), True),
])

df_raw = spark.read.format("csv").schema(schema).option("header", "true").option("delimiter", ",").option("quote", "\"").option("escape", "\"").option("multiLine", "true").option("ignoreLeadingWhiteSpace", "true").option("ignoreTrailingWhiteSpace", "true").load("Files/new_data/*.csv")

df = df_raw.filter(col("SalesOrderNumber").rlike("^SO[0-9]+$"))

df = df.withColumn("OrderDate", to_date(col("OrderDate"), "yyyy-MM-dd"))

df = df.withColumn("Year", year(col("OrderDate"))).withColumn("Month", month(col("OrderDate")))

df = df.withColumn("FirstName", split(col("CustomerName"), " ").getItem(0)).withColumn("LastName", expr("substring_index(CustomerName, ' ', -1)"))

df = df.select("SalesOrderNumber", "SalesOrderLineNumber", "OrderDate", "Year", "Month", "FirstName", "LastName", "EmailAddress", "Item", "Quantity", "UnitPrice", "TaxAmount")
#spark.sql(f"TRUNCATE TABLE {table_name}")
#df.write.format("delta").mode("append").saveAsTable(table_name)

df.write.format("delta").mode("overwrite").saveAsTable(table_name)




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.filter(col("SalesOrderNumber").startswith('"')).count()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#df.filter(col("Item").contains(",")).show(truncate=False)
spark.sql(f"SELECT COUNT(*) AS row_count FROM {table_name}").show()
spark.sql(f"DESCRIBE HISTORY {table_name}").show(truncate=False)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql(f"""
SELECT
  COUNT(*)                       AS total_rows,
  COUNT(DISTINCT SalesOrderNumber) AS distinct_orders
FROM {table_name}
""").show()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#Для sales CSV уникальный ключ — это: (SalesOrderNumber, SalesOrderLineNumber)
#Проверка дубликатов ПЕРЕД записью
df_raw.groupBy("SalesOrderNumber", "SalesOrderLineNumber").count().filter(col("count") > 1).count()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
