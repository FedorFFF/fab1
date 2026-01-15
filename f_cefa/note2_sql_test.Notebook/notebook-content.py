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

# Читаем PSV файл (разделитель |)
path = "Files/in_psv/MDFR-Input-Docket-*.psv" # путь к твоим файлам

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("sep", "|") \
    .load(path)

# Показываем первые 10 записей
display(df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Записываем наши 10 строк в таблицу Lakehouse
try:
    df.limit(10).write.mode("overwrite").format("delta").saveAsTable("dbo.test_from_spark")
    print("✅ УСПЕХ! Таблица dbo.test_from_spark создана в Lakehouse.")
except Exception as e:
    print(f"❌ Даже здесь ошибка: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Твои данные (тестовая строка)
df = spark.createDataFrame([("Official Connector Test",)], ["test_message"])

# 2. Твои параметры
# ВНИМАНИЕ: Замени 'CEFA' и 'CEFA_Lakehouse' на точные имена, если они другие
# Формат: "WorkspaceName.WarehouseName.SchemaName.TableName"
target_table = "CEFA.CEFA_Lakehouse.lnd.test_simple_write"

try:
    print("Пробую запись через официальный Fabric Warehouse Connector...")
    
    df.write \
        .format("fabric.warehouse") \
        .option("table", target_table) \
        .mode("append") \
        .save()
        
    print("✅ ПОБЕДА! Официальный коннектор сработал.")
except Exception as e:
    print(f"❌ Ошибка даже с официальным коннектором: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils

# Получаем токен для Power BI / Fabric API
token = mssparkutils.credentials.getToken("pbi")

# Выводим первые 50 символов, чтобы убедиться, что он есть, но не светить весь код безопасности
print(f"Токен получен успешно! Начало токена: {token[:50]}...")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import mssparkutils

# 1. Твои реквизиты (Endpoint, который ты нашел)
server = 'txevxqqrsppuve3evkv42zse3a-5ole3t76tenebfblsb4pmvhxyi.datawarehouse.fabric.microsoft.com'
database = 'CEFA_Lakehouse'

# 2. Берем токен (твой "паспорт") и упаковываем его для SQL-драйвера
token_str = mssparkutils.credentials.getToken("pbi")
token_bytes = token_str.encode("utf-16-le")
token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)

# 3. Настройка строки подключения
# Используем драйвер ODBC 18, который встроен в Fabric
conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Database={database};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

try:
    print("Открываю прямой SQL-канал в обход Spark...")
    # Атрибут 1256 — это способ передать токен вместо логина и пароля
    with pyodbc.connect(conn_str, attrs_before={1256: token_struct}) as conn:
        with conn.cursor() as cursor:
            print("Соединение установлено! Пробую записать строку...")
            
            # Это чистый SQL INSERT. Он не создает файлы в OneLake, поэтому 403 не будет.
            cursor.execute("INSERT INTO lnd.test_simple_write (test_message) VALUES ('Победа! Записано через Python и Токен!')")
            
            conn.commit()
            print("✅ ТЕСТ ПРОЙДЕН! Данные успешно улетели в Warehouse.")
            
            # Проверяем, что данные там
            cursor.execute("SELECT TOP 1 test_message FROM lnd.test_simple_write ORDER BY 1 DESC")
            print(f"Подтверждение из базы: {cursor.fetchone()[0]}")

except Exception as e:
    print(f"❌ Ошибка записи: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pyodbc

# 1. Данные для подключения
server = 'txevxqqrsppuve3evkv42zse3a-5ole3t76tenebfblsb4pmvhxyi.datawarehouse.fabric.microsoft.com'
database = 'CEFA_Lakehouse'

# Строка подключения (используем ActiveDirectoryInteractive для Fabric)
conn_str = (
    f"Driver={{ODBC Driver 18 for SQL Server}};"
    f"Server={server},1433;"
    f"Database={database};"
    f"Authentication=ActiveDirectoryInteractive;"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

try:
    print(f"Попытка подключения к {database}...")
    
    # Устанавливаем соединение
    with pyodbc.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            print("Соединение установлено. Пробую выполнить INSERT...")
            
            # Вставляем тестовую запись
            cursor.execute("""
                INSERT INTO lnd.test_simple_write (test_message) 
                VALUES (?)
            """, ('Direct Write Success - No Spark Files!',))
            
            # Фиксируем транзакцию
            conn.commit()
            print("✅ ПОБЕДА! Данные записаны напрямую через SQL.")

            # Проверяем результат
            cursor.execute("SELECT TOP 1 test_message FROM lnd.test_simple_write ORDER BY 1 DESC")
            row = cursor.fetchone()
            print(f"Подтверждение из базы: {row[0]}")

except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("\nЕсли ошибка 'Login timeout', проверьте, не 'спит' ли Warehouse (зайдите в него в UI).")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import pyodbc
import struct
from notebookutils import mssparkutils

# 1. Данные для подключения
server = 'txevxqqrsppuve3evkv42zse3a-5ole3t76tenebfblsb4pmvhxyi.datawarehouse.fabric.microsoft.com'
database = 'CEFA_Lakehouse'

# 2. Получаем системный токен доступа (Bearer Token)
token_path = mssparkutils.credentials.getToken("pbi")
# Токен нужно перекодировать для драйвера ODBC
tokenb = bytes(token_path, "UTF-8")
exptoken = b""
for i in tokenb:
    exptoken += struct.pack("B", i)
    exptoken += struct.pack("B", 0)

# 3. Новая строка подключения (через SQL Driver 18)
conn_str = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Database={database};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"

try:
    print(f"Пробую подключиться к {server} с системным токеном...")
    
    # SQL_COPT_SS_ACCESS_TOKEN = 1256 (это магия для передачи токена драйверу)
    conn = pyodbc.connect(conn_str, attrs_before={1256: exptoken})
    
    with conn.cursor() as cursor:
        print("✅ СОЕДИНЕНИЕ УСТАНОВЛЕНО!")
        cursor.execute("INSERT INTO lnd.test_simple_write (test_message) VALUES (?)", ('Success with Token!',))
        conn.commit()
        print("Данные успешно записаны.")
        
    conn.close()

except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nЕсли ошибка всё еще HYT00, зайди в Warehouse в интерфейсе Fabric,")
    print("убедись, что он активен (зеленый статус) и попробуй снова.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. Создаем тестовый DataFrame
test_df = spark.createDataFrame([("Final Test Success",)], ["test_message"])

# 2. Пытаемся записать в НОВУЮ таблицу в схему dbo
# Мы не используем шорткаты, не используем схему lnd. Только родной dbo.
target_table_name = "CEFA_Lakehouse.dbo.final_spark_test"

try:
    print(f"Пробую записать в {target_table_name}...")
    
    test_df.write.format("delta").mode("overwrite").saveAsTable(target_table_name)
    
    print("✅ СВЕРШИЛОСЬ! Spark записал данные в dbo.")
    display(spark.sql(f"SELECT * FROM {target_table_name}"))

except Exception as e:
    print(f"❌ Даже в dbo не пишет: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
