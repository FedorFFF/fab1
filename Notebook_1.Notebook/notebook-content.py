# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "89b26255-9375-4061-9a6e-bdce49bc227f",
# META       "default_lakehouse_name": "lake1",
# META       "default_lakehouse_workspace_id": "7dd85790-2e04-4e40-90a7-f20f50640ed8",
# META       "known_lakehouses": [
# META         {
# META           "id": "89b26255-9375-4061-9a6e-bdce49bc227f"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

%ls /lakehouse/default/Files


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("binaryFile").load("Files/")
df = df.select("path")

df.toPandas().to_csv("file_list.csv", index=False)



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

#%ls /
#dbutils.fs.ls("Files")
display(spark.read.format("binaryFile").load("Files/"))




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
