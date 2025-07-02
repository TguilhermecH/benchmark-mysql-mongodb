import time
from pymongo import MongoClient

# Conectar no MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["benchmark_db"]
collection = db["movies"]

# -----------------------------------------
# Função para medir tempo + contar resultado
def measure_time(func, description):
    start = time.time()
    result, count = func()
    end = time.time()
    elapsed = end - start
    print(f"{description}: {elapsed:.4f} segundos, {count} documentos processados")
    return result

# -----------------------------------------
# 1️⃣ Consulta simples: contar todos os documentos
def simple_query():
    count = collection.count_documents({})
    return None, count

# 2️⃣ Consulta complexa: agregação (filmes por gênero)
def complex_query():
    pipeline = [
        { "$unwind": "$genres" },
        { "$group": { "_id": "$genres", "total": { "$sum": 1 } } },
        { "$sort": { "total": -1 } },
        { "$limit": 10 }
    ]
    result = list(collection.aggregate(pipeline))
    count = len(result)
    return result, count

# 3️⃣ Atualização: marcar filmes longos
def update_operation():
    result = collection.update_many(
        { "runtimeMinutes": { "$gt": 120 } },
        { "$set": { "longMovie": False } }
    )
    count = result.modified_count
    return result, count

# 4️⃣ Deleção: remover filmes antes de 1900
def delete_operation():
    result = collection.delete_many({ "startYear": { "$lt": 2000 } })
    count = result.deleted_count
    return result, count

# -----------------------------------------
# Executar e medir
measure_time(simple_query, "Consulta simples - count_documents")
measure_time(complex_query, "Consulta complexa - agregação por gênero")
measure_time(update_operation, "Atualização - marcar filmes longos")
measure_time(delete_operation, "Deleção - remover filmes antes de 1900")
