# 🤝 JobScope — Field Operations Management Platform

**JobScope** is a smart platform that connects store owners and company managers via a Telegram bot and an internal API.  
It enables real-time task assignment, communication, and performance tracking — all within a 6 km radius.

---

## 🎯 Key Features

### 🏪 For Store Owners:
- Submit product requests to nearby companies (within 6 km)
- Add store details: location, contact info, and more
- Save favourite companies for quick access
- Receive and respond to task assignments

### 🏢 For Companies:
- Manage and view nearby stores
- Receive and approve store requests
- Assign tasks to internal staff
- Set and track bonuses & penalties
- View staff performance and task status

### 👨‍💼 For Employees:
- View tasks within a 6 km radius
- Update task statuses (e.g. in-progress, done)
- Earn bonuses or penalties based on task completion

---

## 🛠️ Tech Stack

- **Python** • **Django** • **DRF**
- **Aiogram 2** – Telegram Bot Framework
- **PostgreSQL** – Relational database
- **Docker** – Containerized development
- **JWT Authentication** – Secure session handling

---

## ⚙️ Project Structure

WorkLink/
├── backend/ # Django + DRF API
├── bot/ # Aiogram Telegram bot logic
├── core/ # Core models: tasks, users, stores
├── utils/ # Business logic & helpers
└── README.md # You're here

yaml
Copy
Edit

---

## 🚀 Quick Start

### 1. Clone the repository:
```bash
git clone https://github.com/muhammadnuruz/JobScope.git
cd JobScope
```
### 2. Apply migrations & create superuser:
```bash
docker exec -it app python manage.py migrate
docker exec -it app python manage.py createsuperuser
```
#### Replace app with your Django container name if different.

## 📍 Location-Based Intelligence
- Dynamic 6 km geolocation filtering
- Near-me detection using coordinates
- Separate visibility rules for stores, employees, and companies

## 🔐 Authentication
- JWT tokens for secure access
- Role-based permissions (store, employee, company admin)

📬 Contact
For questions, collaborations or feedback:
[![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white&style=for-the-badge)](https://github.com/muhammadnuruz)
[![Telegram](https://img.shields.io/badge/Telegram-0088CC?logo=telegram&logoColor=white&style=for-the-badge)](https://t.me/themuhammadnur)

“Great teams are built by great coordination — and WorkLink makes that coordination seamless.”
