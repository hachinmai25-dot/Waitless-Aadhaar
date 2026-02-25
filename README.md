# 🪪 WaitLess Aadhaar
### An Online-First Approach to Faster, Smarter Aadhaar Enrollment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Backend-Flask-blue)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/Frontend-React-61DAFB)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/Database-MySQL-orange)](https://www.mysql.com/)

---

## 📌 About the Project

**WaitLess Aadhaar** is a smart digital platform that eliminates long queues and reduces waiting time at Aadhaar enrollment centers. Citizens pre-fill their details online, and the system automatically allocates them to the **nearest available biometric center** using geolocation — saving time, reducing overcrowding, and improving accuracy.

> **Problem:** People waste hours in queues at Aadhaar centers with no prior data entry, leading to delays, errors, and frustration.

> **Solution:** Allow citizens to register all details online first, then intelligently assign them the nearest center with available capacity and a confirmed time slot.

---

## 🎯 Key Features

- 📋 **Online Pre-Registration** — Fill personal details, document type, and application purpose before visiting.
- 📍 **Smart Center Allocation** — Uses the Haversine geolocation algorithm to find the top 3 nearest biometric centers.
- ⚖️ **Load Balancing** — Centers with full capacity are excluded; workload is distributed evenly.
- 🗓️ **Slot Booking** — Users pick a date and time at their chosen center.
- 🎫 **Token Generation** — Each applicant gets a unique token (e.g., `WLA-4821`) for tracking.
- 📊 **Status Tracking** — Check appointment status anytime using a registered mobile number.
- 🔒 **Secure & Scalable** — Built with REST APIs, environment variables, and Docker-ready architecture.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, React Router, Axios, Vite |
| Backend | Python 3, Flask, Flask-CORS |
| Database | MySQL |
| Algorithm | Haversine Formula (Geolocation) |
| Auth/Config | python-dotenv, Environment Variables |
| Deployment | Docker, docker-compose |

---

## 📁 Project Structure

```
waitless-aadhaar/
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # App configuration
│   ├── models.py               # DB models
│   ├── routes/
│   │   ├── applicant.py        # Registration, slot booking, status
│   │   └── center.py           # Center management APIs
│   ├── utils/
│   │   └── geo_allocator.py    # Haversine distance + center sorter
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── RegistrationForm.jsx
│   │   │   ├── SlotBooking.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Register.jsx
│   │   │   └── Status.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── database/
│   └── schema.sql              # DB schema + sample data
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Git

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/hachinmai25-dot/waitless-aadhaar.git
cd waitless-aadhaar
```

---

### 2️⃣ Setup the Database

```bash
mysql -u root -p < database/schema.sql
```

This will:
- Create the `waitless_aadhaar` database
- Create all tables (`applicants`, `biometric_centers`, `appointments`)
- Insert sample biometric center data

---

### 3️⃣ Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=waitless_aadhaar
SECRET_KEY=your_secret_key_here
GOOGLE_MAPS_API=your_google_maps_api_key
```

---

### 4️⃣ Run the Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs at: `http://localhost:5000`

---

### 5️⃣ Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 🐳 Run with Docker (Optional)

```bash
docker-compose up --build
```

This starts the backend, frontend, and MySQL container together.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/applicant/register` | Register a new applicant |
| `POST` | `/api/applicant/nearest-centers` | Get top 3 nearest centers |
| `POST` | `/api/applicant/book-slot` | Book an appointment slot |
| `GET` | `/api/applicant/status/:mobile` | Check application status |

### Sample Request — Register

```json
POST /api/applicant/register
{
  "full_name": "Ravi Kumar",
  "dob": "1995-06-15",
  "gender": "Male",
  "mobile": "9876543210",
  "email": "ravi@example.com",
  "address": "12, MG Road, Bengaluru",
  "pincode": "560001",
  "latitude": 12.9716,
  "longitude": 77.5946,
  "application_type": "New"
}
```

### Sample Response — Nearest Centers

```json
{
  "centers": [
    {
      "id": 1,
      "name": "Aadhaar Seva Kendra - MG Road",
      "distance_km": 0.8,
      "current_load": 23,
      "capacity_per_day": 60
    },
    {
      "id": 3,
      "name": "Aadhaar Center - Jayanagar",
      "distance_km": 5.2,
      "current_load": 15,
      "capacity_per_day": 50
    }
  ]
}
```

---

## 🧠 Algorithm — Smart Center Allocation

The **Haversine Formula** calculates the real-world distance (in km) between the applicant's GPS coordinates and each biometric center:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
distance = 2R × atan2(√a, √(1−a))
```

Centers are then:
1. Filtered — those with `current_load < capacity_per_day` only
2. Sorted — by distance (ascending)
3. Returned — top 3 nearest centers presented to the user

---

## 🔄 Application Flow

```
User Visits Site
      │
      ▼
Fills Registration Form (Name, DOB, Address, etc.)
      │
      ▼
Browser Fetches GPS Coordinates
      │
      ▼
Backend Calculates Nearest Centers (Haversine Algorithm)
      │
      ▼
User Selects Center + Date + Time Slot
      │
      ▼
Token Generated (e.g., WLA-4821)
      │
      ▼
Appointment Confirmed ✅
      │
      ▼
User Visits Center with Token — Fast Biometric Processing
```

---

## 📸 Screenshots

> Add screenshots of your UI here after building:

| Page | Description |
|---|---|
| `/` | Home / Landing Page |
| `/register` | Multi-step registration form |
| `/status` | Status tracker by mobile number |

---

## 🚧 Future Enhancements

- [ ] SMS/Email notifications via Twilio / SendGrid
- [ ] Admin dashboard to manage centers and appointments
- [ ] Google Maps visual center display
- [ ] Aadhaar document upload (secure)
- [ ] Multi-language support (Hindi, Tamil, Telugu, etc.)
- [ ] OTP-based mobile verification
- [ ] QR code for appointment token
- [ ] Analytics dashboard for government officials

---

## 🤝 Contributing

Contributions are welcome!

```bash
# Fork the repo
# Create a new branch
git checkout -b feature/your-feature-name

# Commit your changes
git commit -m "Add: your feature description"

# Push and create a Pull Request
git push origin feature/your-feature-name
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [yourprofile](https://linkedin.com/in/yourprofile)
- Email: youremail@example.com

---

## 🙏 Acknowledgements

- [UIDAI](https://uidai.gov.in/) — Unique Identification Authority of India
- [Haversine Formula](https://en.wikipedia.org/wiki/Haversine_formula) — Distance calculation
- Flask & React open-source communities

---

> *"Waiting is not a service. WaitLess Aadhaar makes enrollment faster, smarter, and citizen-friendly."*
