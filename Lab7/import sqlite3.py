import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
        return conn
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(e)

def select_high_pr_tasks(conn):
    sql = 'SELECT t.task, t.data, p.prior_name FROM tasks t JOIN prior p ON t.prior = p.id WHERE t.prior = 1'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
# Створення нового завдання
def create_task(conn, task):
    sql = ''' INSERT INTO tasks(task, data, prior)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)


# Оновлення дати в завданні
def update_data_task(conn, data):
    sql = ''' UPDATE tasks
              SET data = ?
              WHERE task = ?'''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()


# Видалення завдання за його текстом
def remove_task(conn, removed_task):
    sql = ''' DELETE FROM tasks WHERE task = ? '''
    cur = conn.cursor()
    cur.execute(sql, removed_task)
    conn.commit()


def main():
    database = "planner.db"
    conn = create_connection(database)

     # Використовууючи встановлене з'єднання виконуються операції над БД
    with conn:
        print("\nВсі завдання (завдання, дата, приорітет)")
        select_all_tasks(conn)
        print("\nЗавдання з найвищим приорітетом (завдання, дата, приорітет)")
        select_high_pr_tasks(conn)
        print("\nВставка нового рядка...")
        create_task(conn, ('Навідатися до друга','01-12-2023',1))
        print("\nВсі завдання (завдання, дата, приорітет)")
        select_all_tasks(conn)
        print("\nЗміна рядка...")
        update_data_task(conn, ('08-01-2024','Навідатися до друга'))
        print("\nВсі завдання (завдання, дата, приорітет)")
        select_all_tasks(conn)        
        print("\nВставка нового рядка...")
        create_task(conn, ('Відпочити на морі','20-07-2024',1))
        print("\nВсі завдання (завдання, дата, приорітет)")
        select_all_tasks(conn)
        print("\nВидалення рядка")
        remove_task(conn, ('Відпочити на морі',))
        print("\nВсі завдання (завдання, дата, приорітет)")
        select_all_tasks(conn)
if __name__ == '__main__':
    main()
