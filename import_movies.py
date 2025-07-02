import pandas as pd
from pymongo import MongoClient

# 1️⃣ Caminho do arquivo TSV original
TSV_PATH = "title.basics.tsv"  # 👉 Troque pelo nome real

# 2️⃣ Ler o TSV usando Pandas
df = pd.read_csv(
    TSV_PATH,
    sep="\t",
    na_values="\\N"  # o IMDb usa '\N' para NULL
)

# 3️⃣ Tratar tipos de dados
df['isAdult'] = df['isAdult'].fillna(0).astype(int)
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce').astype('Int64')
df['endYear'] = pd.to_numeric(df['endYear'], errors='coerce').astype('Int64')
df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce').astype('Int64')

# 4️⃣ Converter genres de string para lista
df['genres'] = df['genres'].fillna("").apply(lambda x: x.split(",") if x else [])

# 5️⃣ Conectar no MongoDB local
client = MongoClient("mongodb://localhost:27017/")

# Nome do banco e coleção
db = client["benchmark_db"]
collection = db["movies"]

# 6️⃣ Converter para dict
records = df.to_dict(orient='records')

# 7️⃣ Inserir tudo na coleção
result = collection.insert_many(records)

print(f"Inseridos {len(result.inserted_ids)} documentos no MongoDB!")