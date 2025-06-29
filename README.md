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

## 👨‍💻 Developed By

**Muhammad Nur Suxbatullayev**  
🎓 Junior Back-End Developer with 1+ years of hands-on experience  
🏫 Full Scholarship Recipient at PDP University  
🧠 Skilled in building scalable and secure back-end systems using:  
- Python & Django  
- Django REST Framework (DRF)  
- PostgreSQL  
- Docker & Containerization  
- Aiogram (Telegram Bot Framework)  
- RESTful API Design & Integration

🔗 **GitHub:** [github.com/muhammadnuruz](https://github.com/muhammadnuruz)  
📬 **Telegram:** [@TheMuhammadNur](https://t.me/TheMuhammadNur)

---

## ⭐ Support the Project

If this project helped you, inspired you, or you simply liked it, please consider giving it a **⭐ on GitHub**.  
Your support boosts the project's visibility and motivates continued improvements and future updates.

Thank you for being part of the journey!
