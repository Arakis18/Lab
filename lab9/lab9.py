from pymongo import MongoClient

# Підключення до сервера MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Створення бази даних
db = client["expense_tracker"]

# Створення колекції (еквівалент таблиці в реляційних базах даних)
collection = db["expenses"]

# Додавання документів (еквівалент записів в таблиці)
data1 = {"category": "Groceries", "amount": 50.0, "description": "Weekly grocery shopping"}
data2 = {"category": "Utilities", "amount": 120.0, "description": "Electricity bill"}

# Вставка документів
inserted_data1 = collection.insert_one(data1)
inserted_data2 = collection.insert_one(data2)

# Зчитування документів
print("Всі документи:")
for document in collection.find():
    print(document)

# Оновлення документа
query = {"category": "Groceries"}
new_data = {"$set": {"amount": 55.0}}
collection.update_one(query, new_data)

# Видалення документа
delete_query = {"category": "Utilities"}
collection.delete_one(delete_query)

# Зчитування документів після оновлення та видалення
print("\nПісля оновлення та видалення:")
for document in collection.find():
    print(document)

# Закриття підключення
client.close()
