# ...existing code...
import os
from models import init_db, get_db_conn

# Виконає створення таблиць у db.sqlite (як у models.py)
init_db()

conn = get_db_conn()
cursor = conn.cursor()

print("Очищення старих даних (якщо є)...")
# без помилок, якщо таблиці пусті
cursor.execute('DELETE FROM sneakers')
cursor.execute('DELETE FROM categories')
cursor.execute('DELETE FROM feedback')

print("Додавання категорій...")
categories = ['Для Бігу', 'Лайфстайл', 'Для Баскетболу']
for name in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

conn.commit()

# Отримати id категорій
cat_run_id = cursor.execute("SELECT id FROM categories WHERE name = ?", ('Для Бігу',)).fetchone()[0]
cat_life_id = cursor.execute("SELECT id FROM categories WHERE name = ?", ('Лайфстайл',)).fetchone()[0]

print("Додавання товарів...")
sneakers = [
    ('Nike Air Force 1', 'Класичний білий стиль', 4500, 'https://imgproxy.cdn-tinkoff.ru/t_device_1920_x2/aHR0cHM6Ly9wdWJsaWMtc3RhdGljLnRpbmtvZmZqb3VybmFsLnJ1L2RvbHlhbWUvdXBsb2Fkcy8yMDI1LzA0L3FIcVZqOElkLWNvdmVyLWgucG5n', cat_life_id),
    ('Adidas Superstar', 'Легенда вулиць', 4200, 'https://img.joomcdn.net/d31c53bd95c49e3794030aeaf1872e392e889191_1024_1024.jpeg', cat_life_id),
    ('Nike Pegasus 40', 'Для щоденних пробіжок', 5100, 'https://s.6264.com.ua/section/promonewsintext/upload/images/promo/intext/000/051/384/krosipng_5db97aadb2edb.jpg', cat_run_id)
]

for s in sneakers:
    cursor.execute("""
        INSERT INTO sneakers (name, description, price, image_url, category_id)
        VALUES (?, ?, ?, ?, ?)
    """, s)

conn.commit()
conn.close()
print("Seed complete: db.sqlite")
# ...existing code...