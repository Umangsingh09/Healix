# 🩺 Healix – AI Powered Healthcare Triage System

Healix is an **AI-powered healthcare triage platform** that analyzes user symptoms and provides **instant risk assessment and medical guidance**.
It helps users understand the **severity of their condition** and decide whether they should **seek medical attention immediately or manage symptoms at home**.

The goal of Healix is to **reduce unnecessary hospital visits and provide quick preliminary health insights using AI.**

---

# 🚀 Features

* 🧠 **AI Symptom Analysis** – Analyze symptoms using AI models
* ⚡ **Instant Risk Assessment** – Detect low, medium, or high health risk
* 📊 **Health Insights Dashboard**
* 🗂 **Patient Symptom History**
* 🤖 **AI Health Guidance**
* 🔐 **Secure API Backend**
* 🌐 **Cloud Deployment**

---

# 🏗 System Architecture

Frontend → Backend API → AI Engine → Database

```
User
  │
  ▼
Frontend (React / Next.js + Tailwind)
  │
  ▼
Django REST API
  │
  ├── AI Triage Engine (OpenAI / ML)
  │
  ▼
PostgreSQL Database
  │
  ▼
Deployment (Render + Vercel)
```

---

# ⚙️ Tech Stack

## Frontend

* React / Next.js
* Tailwind CSS
* Axios / Fetch API

## Backend

* Django
* Django REST Framework

## AI Layer

* OpenAI API
* Symptom classification
* Risk prediction

## Database

* PostgreSQL (Production)
* SQLite (Development)

## Deployment

* Render – Backend Hosting
* Vercel – Frontend Hosting
* GitHub – Version Control

---

# 📂 Project Structure

```
healix/
│
├── backend/
│   ├── triage/
│   ├── api/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── styles/
│
├── requirements.txt
└── README.md
```

---

# 🔧 Installation & Setup

## 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/healix.git
cd healix
```

---

## 2️⃣ Setup Backend

```
cd backend

python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start server:

```
python manage.py runserver
```

---

## 3️⃣ Setup Frontend

```
cd frontend
npm install
npm run dev
```

---

# 🧠 AI Workflow

1. User enters symptoms
2. Backend sends symptoms to AI model
3. AI predicts health risk level
4. Response returned to frontend
5. Results displayed on dashboard

---

# 📊 Example Output

```
Symptoms: fever, headache, fatigue

AI Result:
Risk Level: Medium
Recommendation: Monitor symptoms and consult doctor if condition worsens.
```

---

# 🌍 Deployment

| Service  | Platform   |
| -------- | ---------- |
| Frontend | Vercel     |
| Backend  | Render     |
| Database | PostgreSQL |

---

# 🔮 Future Improvements

* Doctor appointment integration
* Wearable health device data
* Emergency alert system
* ML-based disease prediction
* Mobile application

---

# 👨‍💻 Team

**Umang Raj**
**Raja kumar**
**Hariom singh**
**Aditya kumar**

B.Tech Data Science Engineering
Jaipur National University

---

# ⭐ Contributing

Contributions are welcome!
Feel free to fork this repository and submit a pull request.

---

# 📜 License

This project is licensed under the MIT License.
