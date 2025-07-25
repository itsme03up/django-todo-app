# 📝 Todo & Chat App - Powered by Django

A collaborative and extensible TODO list web application with real-time chat and planning features. Built using Django, Django Channels, Bootstrap, and PostgreSQL.

---

## 🚀 Features

- ✅ Task creation, completion, deletion
- 💬 Real-time chat for each task using Django Channels + WebSocket
- 📅 Google Calendar sync (planned)
- 📷 Memory photo + comment support (planned)
- 📍 Location saving via Mapbox/Leaflet (planned)
- 👥 User login and task ownership
- 🌐 Mobile-friendly responsive design (Bootstrap)

---

## 🔧 Tech Stack

| Layer        | Technology              |
|--------------|--------------------------|
| Backend      | Django, Django Channels, Gunicorn |
| Frontend     | Bootstrap + JavaScript   |
| Real-time    | Redis + Channels         |
| Database     | PostgreSQL (Render)      |
| File Storage | Amazon S3 (planned)      |
| Hosting      | Render.com               |

---

## 📦 Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/yourname/django-todo-app.git
cd django-todo-app
2. Setup virtual environment
bash
コピーする
編集する
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Run migrations
bash
コピーする
編集する
python manage.py migrate
4. Start development server
bash
コピーする
編集する
python manage.py runserver
🌍 Deployment (Render.com)
This project is optimized for deployment on Render.com:

Key files for Render:
render.yaml – Render build & deploy instructions

requirements.txt – Python dependencies

asgi.py – ASGI config for Channels

static/ – Collected static files

Environment Variables:
Variable	Description
DJANGO_SECRET_KEY	Django secret key
DEBUG	Set to False
DATABASE_URL	PostgreSQL DB URL
REDIS_URL	Redis instance URL
ALLOWED_HOSTS	Your domain or *

📚 Coming Soon
Google Calendar sync

Commented photo memories

Location-based planning

Mobile PWA support

Offline caching with Workbox

🤝 Contributing
Pull requests welcome! Ideas, issues, and collaboration are encouraged.

