# CITY GUARDIAN AI – Multilingual Citizen Assistant

> **AI-Powered Civic Complaint & Mission Management Platform**  
> Integrated with Gemini 2.5 Flash, React.js, Flask, YOLOv5 Vision, and Haversine Semantic Duplicate Detection.

---

## 🌟 Key Capabilities

1. **Multilingual Conversational Assistance**: Seamless natural conversation in **Hindi**, **English**, and **Hinglish**.
2. **AI-Powered Complaint Registration**: Proposes structured complaint drafts and strictly enforces **human citizen confirmation** before writing to the database.
3. **Image Analysis & Civic Vision**: Local YOLOv5 object detection + Gemini Multimodal Vision classification across 6 civic grievance categories (`garbage`, `drainage`, `pothole`, `water_leakage`, `broken_streetlight`, `illegal_dumping`).
4. **Tri-Signal Duplicate Detection**: Combines Haversine GPS proximity (<200m), Category matching, and Semantic description similarity to identify redundant complaints.
5. **Real-Time Mission Tracking**: Authoritative, database-backed countdown timer and squad assignment updates with object-level security.
6. **Gamification & Citizen Rewards**: Real-time points accumulation, badge progression (`New Guardian` → `Active Citizen` → `Civic Hero`), and local business voucher redemption.
7. **Voice-Based Reporting**: Audio capture with Whisper & Gemini Multimodal voice note transcription and browser SpeechSynthesis output.
8. **Preserved Municipal Controls**: AI assists and drafts; human municipal officers retain final approval, resolution, and inspection rights.

---

## 🏗️ System Architecture

```
CITIZEN (Text / Voice / Images / GPS)
                    │
                    ▼
       React.js + Vite Frontend (Port 5173)
[Chat UI • Image Upload • Voice Recorder • Mission & Reward Cards]
                    │
                    ▼  (REST API + JWT Bearer Auth)
           Flask API Gateway (Port 5000)
                    │
   ┌────────────────┼────────────────┐
   ▼                ▼                ▼
Gemini 2.5     Authoritative   YOLOv5 / Vision
Function Call    Services       & Duplicate Engine
   └────────────────┬────────────────┘
                    ▼
          SQLAlchemy ORM
        (MySQL 8.0 / SQLite)
```

---

## 📁 Directory Structure

```
CITY-GUARDIAN/
├── backend/
│   ├── ai/
│   │   ├── agent.py              # Multi-turn Gemini orchestrator & function calling loop
│   │   ├── gemini_client.py      # Official Google GenAI SDK client setup
│   │   ├── intent.py             # Multilingual intent recognizer
│   │   ├── prompts.py            # System prompts and civic behavioral guidelines
│   │   ├── response_parser.py    # Structured card JSON formatter
│   │   └── tools.py              # Gemini function declarations & tool handlers
│   ├── models/                   # SQLAlchemy Database Models (User, Complaint, Mission, Reward, Conversation)
│   ├── routes/                   # REST Endpoints (chat, complaints, missions, rewards, uploads)
│   ├── services/                 # Authoritative business logic (duplicate, vision, voice, mission, rewards)
│   ├── schemas/                  # Pydantic validation schemas
│   ├── utils/                    # JWT Auth, Haversine helpers, and validators
│   ├── uploads/                  # Upload directory for images & audio notes
│   ├── app.py                    # Flask application factory and database seed runner
│   ├── config.py                 # Configuration loader
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── chatbot/          # ChatWindow, ChatHeader, ChatInput, ImageUploader, VoiceRecorder
│   │   │   ├── cards/            # MissionCard, ComplaintCard, RewardCard, DuplicateAlert
│   │   │   └── common/           # Loader, ErrorMessage
│   │   ├── services/             # Axios API clients for chat, uploads, and voice
│   │   ├── utils/                # Countdown timer and badge utilities
│   │   ├── App.jsx
│   │   └── index.css             # Tailwind CSS styles
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env
├── database/
│   ├── schema.sql                # Complete MySQL DDL schema
│   └── seed_data.sql             # Demo wards, users, complaints, missions & coupons
├── yolov5/
│   ├── weights/
│   └── detect.py                 # Local YOLOv5 civic inference wrapper
├── docker-compose.yml            # Multi-container Docker deployment
├── test_city_guardian.py         # 12/12 Automated Verification Test Suite
└── README.md
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) Docker & Docker Compose

### 1. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create & activate virtual environment (if not already created)
python -m venv ..\.venv
..\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask backend
python app.py
```
> The backend will automatically initialize and seed the database with demo users, missions, and rewards on first launch at `http://127.0.0.1:5000`.

### 2. Frontend Setup

In a new terminal:
```powershell
# Navigate to frontend directory
cd frontend

# Install npm packages
npm install

# Start Vite development server
npm run dev
```
> The React interface will be live at `http://localhost:5173`.

---

## 🧪 12/12 Verification Test Suite

Run the full automated test suite covering all functional, architectural, and security constraints:

```powershell
python test_city_guardian.py
```

### Verified Test Cases:
| # | Test Scenario | Verified Behavior |
|---|---------------|-------------------|
| 1 | Hindi Complaint Registration | Correctly parses *"Naala overflow ho raha hai"* and drafts complaint |
| 2 | English Complaint Registration | Correctly classifies pothole and drafts grievance report |
| 3 | Hinglish Natural Query | Responds to *"Bhai mere points kitne hain"* in context |
| 4 | Civic Image Analysis | Extracts category, confidence score, and detected hazards |
| 5 | Tri-Signal Duplicate Detection | Flags nearby active issues (<200m) with identical category |
| 6 | Citizen Confirmation Safeguard | Enforces explicit human approval before writing complaint to DB |
| 7 | Live Mission Tracking | Computes accurate countdown deadline and squad assignment |
| 8 | Authorization & Privacy | Blocks Citizen B from accessing Citizen A's private mission |
| 9 | Citizen Rewards Inquiry | Returns authoritative points tally and Guardian badge level |
| 10| Local Coupon Redemption | Safely deducts points and issues unique voucher code |
| 11| Multilingual Voice Reporting | Transcribes audio reports into complaint text |
| 12| Municipal Human Verification | Preserves human approval status; blocks AI auto-closure |

---

## 🐳 Docker Deployment

To launch the full stack with MySQL 8.0, Flask backend, and Nginx React frontend:

```powershell
docker-compose up --build
```
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:5000`
- MySQL: Port `3306`

