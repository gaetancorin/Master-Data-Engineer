from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestReservation") \
    .master("spark://10.31.35.181:7077") \
    .config("spark.sql.catalogImplementation", "in-memory") \
    .getOrCreate()

# 2. Générer un DataFrame de test
data = [
    (1, "Alice", "2024-05-01"),
    (2, "Bob", "2024-05-02"),
    (3, "Charlie", "2024-05-03")
]
columns = ["id", "client", "date_reservation"]

df = spark.createDataFrame(data, schema=columns)

# 3. Écrire la table "reservation" dans Spark (temporaire)
df.createOrReplaceTempView("reservation")

print("✅ Table 'reservation' créée avec succès.")

# 4. Lire la table "reservation"
result = spark.sql("SELECT * FROM reservation")

print("📋 Contenu de la table 'reservation' :")
result.show()

# 5. (Optionnel) Sauvegarder sur disque en format Parquet
# result.write.mode("overwrite").parquet("C:/chemin/vers/reservation.parquet")

# 6. Fermer la session Spark proprement
spark.stop()

