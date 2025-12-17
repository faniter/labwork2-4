# Лабораторна робота 6

**Студент:** Ваше ім'я  
**Група:** Назва групи

## 📋 Опис проєкту

Веб-застосунок "Світ Кросівок" (KickZone) - це інтернет-магазин взуття з повнофункціональним API. Застосунок дозволяє переглядати каталог товарів, фільтрувати за категоріями, додавати товари до кошика, залишати відгуки та керувати контентом через адміністративну панель. API Demo сторінка демонструє роботу з REST API для управління відгуками через AJAX запити.

## 📁 Структура проєкту

```
labwork2-4/
├── app.py                    # Головний файл Flask додатку
├── models.py                 # Моделі бази даних та функції доступу
├── requirements.txt          # Залежності Python
├── db.sqlite                 # База даних SQLite
├── Dockerfile                # Docker конфігурація
├── docker-compose.yml        # Docker Compose для production
├── nginx.conf                # Конфігурація Nginx
├── API_README.md             # Документація API
├── README.md                 # Цей файл
├── routes/                   # Маршрути Flask
│   ├── __init__.py
│   ├── admin.py              # Адмін-панель
│   ├── api.py                # REST API endpoints
│   ├── api_demo.py           # API Demo сторінка
│   ├── auth.py               # Аутентифікація
│   ├── feedback.py           # Відгуки
│   └── shop.py               # Магазин
├── templates/                # HTML шаблони
│   ├── base.html             # Базовий шаблон
│   ├── home.html             # Головна сторінка
│   ├── catalog.html          # Каталог товарів
│   ├── cart.html             # Кошик
│   ├── feedback.html         # Форма відгуків
│   ├── api_demo.html         # API Demo інтерфейс
│   ├── admin.html            # Адмін-панель відгуків
│   ├── admin_categories.html # Керування категоріями
│   ├── admin_catalog.html    # Керування каталогом
│   └── ...
└── lab-reports/              # Звіти з лабораторних робіт
```

## 🔌 API Endpoints

### Відгуки (Feedback)

#### GET /api/feedback
Отримує список всіх відгуків від користувачів.

**Відповідь:**
```json
[
  {
    "id": 1,
    "user_name": "Іван Петренко",
    "email": "ivan@example.com",
    "message": "Чудовий магазин! Швидка доставка.",
    "created_at": "2025-12-17 14:30:00"
  },
  {
    "id": 2,
    "user_name": "Марія Коваленко",
    "email": "maria@example.com",
    "message": "Дуже задоволена покупкою!",
    "created_at": "2025-12-17 15:45:00"
  }
]
```

#### POST /api/feedback
Створює новий відгук.

**Тіло запиту (form-data):**
```
user_name: "Олексій Шевченко"
email: "oleksiy@example.com"
message: "Відмінний сервіс і якість товару!"
```

**Відповідь:** Перенаправлення на головну сторінку

### Товари (Products)

#### GET /api/v1/products
Отримує список всіх товарів з можливістю фільтрації.

**Параметри запиту:**
- `category_id` (optional) - ID категорії для фільтрації
- `search` (optional) - Пошуковий запит

**Відповідь:**
```json
[
  {
    "id": 1,
    "name": "Nike Air Max 90",
    "description": "Класичні кросівки для повсякденного носіння",
    "price": 3500,
    "image_url": "/static/uploads/nike-air-max.jpg",
    "category_id": 1,
    "category_name": "Спортивні"
  }
]
```

#### GET /api/v1/products/{product_id}
Отримує деталі конкретного товару за ID.

**Відповідь:**
```json
{
  "id": 1,
  "name": "Nike Air Max 90",
  "description": "Класичні кросівки для повсякденного носіння",
  "price": 3500,
  "image_url": "/static/uploads/nike-air-max.jpg",
  "category_id": 1,
  "category_name": "Спортивні"
}
```

#### POST /api/v1/products
Створює новий товар (вимагає JWT токен).

**Заголовки:**
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Тіло запиту:**
```json
{
  "name": "Adidas Ultraboost",
  "description": "Комфортні бігові кросівки",
  "price": 4200,
  "image_url": "/static/uploads/adidas.jpg",
  "category_id": 1
}
```

### Категорії

#### GET /api/v1/categories
Отримує список всіх категорій товарів.

**Відповідь:**
```json
[
  {
    "id": 1,
    "name": "Спортивні"
  },
  {
    "id": 2,
    "name": "Повсякденні"
  }
]
```

## 🎨 Функціонал API Demo

API Demo сторінка (`/api-demo`) демонструє роботу з REST API:

- ✅ **Відображення списку відгуків** - GET запит до `/api/feedback`
- ✅ **Додавання нового відгуку** - POST запит через AJAX
- ✅ **Повідомлення про успіх/помилку** - динамічне оновлення інтерфейсу
- ✅ **Автоматичне оновлення** - список відгуків оновлюється після додавання
- ✅ **Сучасний дизайн** - Tailwind CSS з градієнтами та анімаціями

## 📸 Скріншоти

### Головна сторінка
![Головна сторінка застосунку](screenshots/main.png)

### Форма додавання відгуку
![Форма додавання нового відгуку](screenshots/add-form.png)

### Повідомлення про успіх
![Повідомлення про успішне додавання](screenshots/success.png)

## 🚀 Як запустити проєкт

### Локально

1. Клонуйте репозиторій
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Ініціалізуйте базу даних:
   ```bash
   python seed.py
   ```
4. Запустіть додаток:
   ```bash
   python app.py
   ```
5. Відкрийте браузер: `http://localhost:5000`

### За допомогою Docker

```bash
docker-compose up --build
```

## 🛠️ Технології

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **API:** REST API з JSON відповідями
- **Documentation:** Swagger/Flasgger
- **Authentication:** Flask-JWT-Extended
- **Containerization:** Docker + Docker Compose

## 🔗 Посилання

- [Посилання на GitHub](https://github.com/faniter/labwork2-4)

## ✅ Висновки

В ході виконання лабораторної роботи №6 було успішно реалізовано інтерактивну веб-сторінку для роботи з REST API. Я навчився створювати асинхронні AJAX запити за допомогою Fetch API, обробляти відповіді від сервера у форматі JSON, динамічно оновлювати DOM без перезавантаження сторінки, та відображати інформативні повідомлення користувачу. Також було покращено навігацію адміністративної панелі, додавши кнопку API Demo до всіх розділів. Робота з FormData та обробка помилок HTTP запитів поглибила розуміння взаємодії frontend та backend частин веб-застосунку.