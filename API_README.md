# Labwork 2-4 REST API Documentation

## Огляд

REST API для інтернет-магазину кросівок з підтримкою версіонування (v1, v2), повною документацією Swagger та валідацією даних.

**Базовий URL:** `http://localhost:5000/api`  
**Документація:** http://localhost:5000/apidocs

---

## Швидкий старт

### 1. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 2. Запуск сервера
```bash
python app.py
```

Сервер запуститься на `http://localhost:5000`

### 3. Перевірка API
- Swagger UI: http://localhost:5000/apidocs
- Тестовий запит: `curl http://localhost:5000/api/v1/products`

---

## API Endpoints

### Products (v1)

#### GET `/api/v1/products`
Отримати список всіх товарів з можливістю фільтрації.

**Query параметри:**
- `category_id` (integer, optional) — фільтр за категорією
- `search` (string, optional) — пошук за назвою/описом

**Приклади:**
```bash
# Всі товари
curl http://localhost:5000/api/v1/products

# Товари категорії 1
curl http://localhost:5000/api/v1/products?category_id=1

# Пошук
curl http://localhost:5000/api/v1/products?search=nike
```

**Відповідь (200):**
```json
[
  {
    "id": 1,
    "name": "Nike Air Max",
    "description": "Classic sneakers",
    "price": 120.0,
    "image_url": "/static/uploads/nike.jpg",
    "category_id": 1,
    "category_name": "Running"
  }
]
```

---

#### GET `/api/v1/products/<id>`
Отримати товар за ID.

**Приклад:**
```bash
curl http://localhost:5000/api/v1/products/1
```

**Відповідь (200):**
```json
{
  "id": 1,
  "name": "Nike Air Max",
  "description": "Classic sneakers",
  "price": 120.0,
  "image_url": "/static/uploads/nike.jpg",
  "category_id": 1,
  "category_name": "Running"
}
```

**Відповідь (404):**
```json
{
  "error": "Product not found"
}
```

---

#### POST `/api/v1/products`
Створити новий товар.

**Body (JSON):**
```json
{
  "name": "Adidas Ultraboost",
  "description": "Comfortable running shoes",
  "price": 150.0,
  "image_url": "/static/uploads/adidas.jpg",
  "category_id": 1
}
```

**Приклад:**
```bash
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Sneakers","price":99.99}'
```

**Відповідь (201):**
```json
{
  "id": 5
}
```

**Відповідь (400):**
```json
{
  "error": "Missing \"name\" or \"price\""
}
```

---

#### DELETE `/api/v1/products/<id>`
Видалити товар за ID.

**Приклад:**
```bash
curl -X DELETE http://localhost:5000/api/v1/products/5
```

**Відповідь (200):**
```json
{
  "status": "deleted"
}
```

**Відповідь (404):**
```json
{
  "error": "Product not found"
}
```

---

### Categories (v1)

#### GET `/api/v1/categories`
Отримати список всіх категорій.

**Приклад:**
```bash
curl http://localhost:5000/api/v1/categories
```

**Відповідь (200):**
```json
[
  {"id": 1, "name": "Running"},
  {"id": 2, "name": "Basketball"}
]
```

---

### Feedback (v1)

#### POST `/api/v1/feedback`
Надіслати відгук.

**Body (JSON):**
```json
{
  "user_name": "Іван Іванов",
  "email": "ivan@example.com",
  "message": "Чудовий магазин!"
}
```

**Приклад:**
```bash
curl -X POST http://localhost:5000/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{"message":"Great store!"}'
```

**Відповідь (201):**
```json
{
  "status": "ok"
}
```

**Відповідь (400):**
```json
{
  "error": "Message is required"
}
```

---

### Products (v2) — Строга валідація

#### POST `/api/v2/products`
Створити товар з посиленою валідацією та поверненням повного об'єкта.

**Відмінності від v1:**
- Строга перевірка типів (name має бути непорожнім рядком)
- Повертає повний об'єкт створеного товару (не тільки ID)

**Body (JSON):**
```json
{
  "name": "Puma RS-X",
  "description": "Modern retro style",
  "price": 110.0,
  "image_url": "/static/uploads/puma.jpg",
  "category_id": 2
}
```

**Приклад:**
```bash
curl -X POST http://localhost:5000/api/v2/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Puma RS-X","price":110.0}'
```

**Відповідь (201):**
```json
{
  "id": 6,
  "name": "Puma RS-X",
  "description": "Modern retro style",
  "price": 110.0,
  "image_url": "/static/uploads/puma.jpg",
  "category_id": 2,
  "category_name": "Casual"
}
```

**Відповідь (400):**
```json
{
  "error": "Field \"name\" must be a non-empty string"
}
```

---

## Коди статусів

| Код | Значення | Опис |
|-----|----------|------|
| 200 | OK | Запит успішний |
| 201 | Created | Ресурс створено |
| 400 | Bad Request | Невалідні вхідні дані |
| 404 | Not Found | Ресурс не знайдено |
| 500 | Internal Server Error | Помилка сервера |

---

## Версіонування

API підтримує версіонування через URL:
- **v1**: `/api/v1/...` — базова версія з м'якою валідацією
- **v2**: `/api/v2/...` — строга валідація, розширені відповіді

**Рекомендація:** Використовуйте v2 для нових інтеграцій.

---

## Тестування

### Postman
1. Імпортуйте колекцію: `Labwork_API.postman_collection.json`
2. Запустіть сервер: `python app.py`
3. Виконайте тести з колекції

### Swagger UI
1. Відкрийте http://localhost:5000/apidocs
2. Оберіть endpoint
3. Натисніть "Try it out"
4. Виконайте запит

### cURL
```bash
# Отримати всі товари
curl http://localhost:5000/api/v1/products

# Створити товар
curl -X POST http://localhost:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":100}'

# Видалити товар
curl -X DELETE http://localhost:5000/api/v1/products/5
```

---

## Структура проекту

```
labwork2-4/
├── app.py                          # Головний файл Flask
├── models.py                       # Моделі БД
├── requirements.txt                # Залежності
├── routes/
│   ├── api.py                      # REST API endpoints
│   ├── shop.py                     # Web-інтерфейс
│   ├── admin.py                    # Адмін-панель
│   ├── auth.py                     # Авторизація
│   └── feedback.py                 # Відгуки
├── templates/                      # HTML шаблони
├── static/                         # Статичні файли
└── Labwork_API.postman_collection.json  # Postman тести
```

---

## Troubleshooting

### ModuleNotFoundError: No module named 'flask'
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
Змініть порт у `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Swagger UI не відображається
Перевірте, що `flasgger` встановлено:
```bash
pip install flasgger
```

---

## Ліцензія

Проект для навчальних цілей (Labwork 2-4)
