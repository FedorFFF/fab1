# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "872e97b5-207d-421c-8846-4d8b23c80f2d",
# META       "default_lakehouse_name": "CEFA_Lakehouse",
# META       "default_lakehouse_workspace_id": "cf4d96eb-99fe-401a-942b-9078f654f7c2",
# META       "known_lakehouses": [
# META         {
# META           "id": "872e97b5-207d-421c-8846-4d8b23c80f2d"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# localhost <15.01.2026>
# Проверка наличия таблицы в текущем контексте Spark
table_exists = spark.catalog.tableExists("lnd.mdfr_docket")

if table_exists:
    print("Таблица lnd.mdfr_docket существует. Можно делать append.")
else:
    print("Таблица не найдена. Проверьте схему lnd или создайте таблицу.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

direct_path = "abfss://cf4d96eb-99fe-401a-942b-9078f654f7c2@onelake.dfs.fabric.microsoft.com/872e97b5-207d-421c-8846-4d8b23c80f2d/Tables/lnd/mdfr_docket"
print("Схема таблицы в OneLake:")
spark.read.format("delta").load(direct_path).printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print("111 222")
# Попробуем прочитать список схем в твоей базе
# Показывает все таблицы в текущей базе Spark
display(spark.sql("SHOW TABLES"))

# CELL ********************

# Посмотреть текущую базу
print(f"Текущая база данных: {spark.catalog.currentDatabase()}")

# Посмотреть все доступные базы (ваша будет называться как ваш Lakehouse)
display(spark.sql("SHOW DATABASES"))
display(spark.sql("SHOW TABLES"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# display(spark.sql("SHOW TABLES"))
# Чтение через полное имя
# df = spark.sql("SELECT * FROM `CEFA.CEFA_Lakehouse.lnd`.mdfr_docket")
# display(df.limit(10))
# Путь формируется из ваших данных в UI
# Формат: abfss://[WorkspaceName]@onelake.dfs.fabric.microsoft.com/[LakehouseName].Lakehouse/Tables/lnd/mdfr_docket

path = "abfss://CEFA@onelake.dfs.fabric.microsoft.com/CEFA_Lakehouse.Lakehouse/Tables/lnd/mdfr_docket"

try:
    # Читаем как дельта-таблицу
    df = spark.read.format("delta").load(path)
    print("Успешно прочитано через OneLake путь!")
    display(df.limit(5))
except Exception as e:
    print(f"Ошибка доступа к пути: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Важно: используем точное имя базы, которое мы видели в SHOW DATABASES
database_name = "`CEFA.CEFA_Lakehouse.lnd`"

try:
    tables = spark.catalog.listTables(database_name)
    import pandas as pd
    
    # Выводим в красивой таблице
    df_tables = pd.DataFrame([(t.name, t.tableType, t.isTemporary) for t in tables], 
                             columns=['Table Name', 'Type', 'Is Temporary'])
    display(df_tables)
except Exception as e:
    print(f"Ошибка при обращении к каталогу: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM CEFA_Lakehouse.lnd.mdfr_docket LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    print("Пробую записать данные в новую таблицу Lakehouse 'a01'...")
    
    # 1. Очистим имя таблицы от путей, просто создадим её в текущем Lakehouse
    target_table_name = "a01"
    
    # 2. Записываем. Режим 'overwrite' создаст таблицу, если её нет, или перезапишет.
    # Мы не указываем сложные схемы, просто имя.
    df_final.write.format("delta").mode("overwrite").saveAsTable(target_table_name)
    
    print(f"✅ УСПЕХ! Таблица {target_table_name} создана и заполнена.")
    
    # 3. Проверка - читаем то, что записали
    count = spark.table(target_table_name).count()
    print(f"Количество строк в a01: {count}")
    display(spark.table(target_table_name).limit(5))

except Exception as e:
    print(f"❌ Даже в 'a01' не удалось записать: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM CEFA_Lakehouse.dbo.a01 LIMIT 1000")
display(df)
# Ты это уже сделал, и это работает:
# df_final.write.format("delta").mode("overwrite").saveAsTable("CEFA_Lakehouse.dbo.a01")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Записываем данные во временную таблицу в Lakehouse
temp_staging_table = "stg_temp_docket_load"

try:
    # Используем ваш логически верный df_final из предыдущего шага
    df_final.write.format("delta").mode("overwrite").saveAsTable(temp_staging_table)
    print(f"✅ Данные готовы в промежуточной таблице: {temp_staging_table}")
except Exception as e:
    print(f"❌ Ошибка даже в Lakehouse: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

try:
    print("Запускаю принудительный SQL-перенос...")

    # Мы используем конструктор запроса, который Fabric поймет как чисто внутреннюю операцию SQL
    # Без участия файлового API Spark
    query = """
    INSERT INTO CEFA_Lakehouse.lnd.mdfr_docket
    SELECT * FROM CEFA_Lakehouse.dbo.stg_temp_docket_load
    """
    
    # Выполняем это не как действие над DataFrame, а как сырой SQL запрос
    spark.conf.set("spark.sql.execution.arrow.enabled", "true") # ускоряем, если данных много
    spark.sql(query)

    print("✅ УСПЕХ! SQL-движок перенес данные.")
    
    # Проверка
    display(spark.sql("SELECT COUNT(*) FROM CEFA_Lakehouse.lnd.mdfr_docket"))

except Exception as e:
    print(f"❌ Даже внутренний SQL не прошел: {e}")
    print("\nПЛАН Б: Если это не сработает, значит таблица mdfr_docket заблокирована.")
    print("Вам нужно будет в SSMS выполнить: TRUNCATE TABLE lnd.mdfr_docket и попробовать еще раз.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC -- Выполни это в следующей ячейке
# MAGIC INSERT INTO CEFA_Lakehouse.lnd.mdfr_docket
# MAGIC SELECT * FROM CEFA_Lakehouse.dbo.a01;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Создаем одну строчку данных в памяти
test_data = [("Hello from Notebook!",)]
columns = ["test_message"]

df_test = spark.createDataFrame(test_data, columns)

# 2. Пробуем записать через INSERT INTO (это самый "чистый" путь для SQL таблиц)
try:
    print("Пробую вставить константу в lnd.test_simple_write...")
    
    # Регистрируем наш временный DF, чтобы SQL его увидел
    df_test.createOrReplaceTempView("temp_const")
    
    # Выполняем вставку
    spark.sql("INSERT INTO CEFA_Lakehouse.lnd.test_simple_write SELECT * FROM temp_const")
    
    print("✅ УСПЕХ! Данные записаны.")
    
    # Проверяем чтением
    display(spark.sql("SELECT * FROM CEFA_Lakehouse.lnd.test_simple_write"))

except Exception as e:
    print(f"❌ Ошибка записи константы: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Создаем простейшую строку
test_data = [("Test via Synapse Connector",)]
columns = ["test_message"]
df_test = spark.createDataFrame(test_data, columns)

# 2. Настройки подключения
# В Fabric для этого коннектора часто не нужны пароли, он использует текущую сессию
staging_storage = "Files/staging_temp" # Путь в Lakehouse для временных файлов
target_table = "CEFA_Lakehouse.lnd.test_simple_write"

try:
    print("Запускаю запись через Synapse SQL Connector...")
    
    # Этот метод имитирует поведение SQL-движка
    df_test.write \
        .format("com.microsoft.spark.sqlanalytics") \
        .option("dbName", "CEFA_Lakehouse") \
        .option("tableName", "lnd.test_simple_write") \
        .option("tempDir", staging_storage) \
        .mode("append") \
        .save()

    print("✅ ФАНТАСТИКА! Оно сработало через коннектор!")
    display(spark.sql(f"SELECT * FROM {target_table}"))

except Exception as e:
    print(f"❌ Коннектор тоже не помог: {e}")
    print("\nРазбор полетов:")
    if "403" in str(e):
        print("Это значит, что даже системному коннектору запрещено писать в Warehouse из Spark.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
