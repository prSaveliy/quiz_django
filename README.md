# Quiz Django App

Вебсайт для створення та проходження квізів.

## Встановлення
1. **Клонуйте репозиторій:**

```bash
git clone https://github.com/prSaveliy/quiz_django.git
cd quiz_django
```

2. **Створіть віртуальне середовище:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

3. **Встановіть залежності:**
```bash
pip install -r requirements.txt
```

4. **Застосуйте міграції:**
```bash
cd src/quiz
python manage.py migrate
```

5. **Запустіть локальний сервер:**
```bash
python manage.py runserver
```