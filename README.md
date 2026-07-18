
# 🪞 MindMirror AI

## AI-Powered Behavioral Coaching & Habit Transformation Platform

MindMirror AI is an intelligent self-improvement platform that helps users understand their behavioral patterns, identify triggers, build healthier replacement habits, and receive personalized AI coaching.

Powered by **NVIDIA AI**, MindMirror analyzes user reflections and conversations to provide compassionate, science-based behavioral guidance.

---

# ✨ Features

## 🧠 AI Behavioral Coach

* Personalized AI conversations
* Context-aware coaching based on user habits
* Empathetic and non-judgmental responses
* Real-time coaching support
* Trigger identification and pattern recognition

---

## 📊 Habit Intelligence

Track and understand:

* Habit patterns
* Emotional triggers
* Risk periods
* Behavioral cycles
* Progress over time

---

## 📝 Reflection System

Users can record thoughts and experiences:

* Daily reflections
* Emotional states
* Habit struggles
* Personal observations

The AI analyzes reflections to generate meaningful insights.

---

## 🔍 AI Trigger Analysis

MindMirror identifies:

* Primary triggers
* Emotional patterns
* Environmental factors
* High-risk moments

Example:

```
Trigger:
Stress after work

Behavior:
Excessive social media usage

Outcome:
Reduced focus and sleep disruption
```

---

## 🔄 Replacement Habit Suggestions

The AI recommends healthier alternatives:

Examples:

* Mindful breathing
* Short walks
* Journaling
* Delayed response techniques
* Awareness exercises

---

## 🕸️ Behavior Graph Visualization

MindMirror creates behavioral maps:

```
Stress
  |
  ↓
Social Media Scrolling
  |
  ↓
Sleep Loss
  |
  ↓
Low Energy
```

This helps users understand the cycle behind their habits.

---

# 🏗️ System Architecture

```
                 User
                  |
                  |
          React Frontend
                  |
                  |
             FastAPI API
                  |
        --------------------
        |                  |
 Habit Management     AI Coaching
        |                  |
        |            NVIDIA AI API
        |
 In-Memory Storage
```

---

# 🛠️ Technology Stack

## Frontend

| Technology         | Purpose             |
| ------------------ | ------------------- |
| React + TypeScript | User Interface      |
| Vite               | Frontend Build Tool |
| Tailwind CSS       | Styling             |
| Framer Motion      | Animations          |
| Lucide Icons       | UI Icons            |

---

## Backend

| Technology  | Purpose                 |
| ----------- | ----------------------- |
| Python 3.12 | Backend Language        |
| FastAPI     | REST API Framework      |
| Pydantic    | Data Validation         |
| Uvicorn     | ASGI Server             |
| HTTPX       | Async API Communication |

---

## Artificial Intelligence

| Technology         | Purpose                 |
| ------------------ | ----------------------- |
| NVIDIA AI API      | LLM Intelligence        |
| Meta Llama Models  | Conversational Coaching |
| Prompt Engineering | Behavioral Analysis     |

---

# 📂 Project Structure

```
MindMirror-AI
│
├── backend
│   │
│   ├── app
│   │   ├── api
│   │   ├── services
│   │   ├── schemas
│   │   ├── models
│   │   ├── core
│   │   └── utils
│   │
│   ├── requirements.txt
│   └── main.py
│
├── frontend
│   │
│   ├── src
│   │   ├── components
│   │   ├── hooks
│   │   ├── services
│   │   └── pages
│   │
│   ├── package.json
│   └── vite.config.ts
│
└── README.md
```

---

# 🚀 Local Setup

## Prerequisites

Install:

* Python 3.12+
* Node.js 18+
* npm

---

# Backend Setup

Navigate:

```bash
cd backend
```

Create virtual environment:

```bash
python3 -m venv .venv
```

Activate:

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create:

```
backend/.env
```

Add:

```env
NVIDIA_API_KEY=your_nvidia_api_key

CORS_ORIGINS=http://localhost:3000
```

---

## Start Backend

Run:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend runs:

```
http://localhost:8000
```

API Documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Create:

```
.env
```

Add:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Start:

```bash
npm run dev
```

Frontend runs:

```
http://localhost:3000
```

---

# 🔌 API Endpoints

## Health Check

```
GET /health
```

---

## Get Coaching Plan

```
GET /api/habits/{habit_id}/coaching
```

---

## AI Chat

```
POST /api/habits/{habit_id}/chat
```

Request:

```json
{
  "message": "I feel stressed and want to relapse",
  "context": {
    "reflections_count": 5
  }
}
```

Response:

```json
{
  "type": "message",
  "content": "Let's understand what triggered this feeling..."
}
```

---

## Submit Reflection

```
POST /api/habits/{habit_id}/quick-reflection
```

---

# 🔐 Security Considerations

Implemented:

✅ Environment-based secrets
✅ Input sanitization
✅ Request validation
✅ CORS configuration
✅ Rate limiting middleware
✅ Exception handling

---

# 🧪 Testing

Backend:

```bash
pytest
```

Frontend:

```bash
npm test
```

---

# 🚢 Deployment Plan

## Frontend

Recommended:

* Vercel
* Netlify

Environment:

```
VITE_API_BASE_URL=<backend-url>
```

---

## Backend

Recommended:

* Render
* Railway
* Fly.io

Environment:

```
NVIDIA_API_KEY=<secret>
```

---

# 🔮 Future Enhancements

## Phase 2

* User authentication
* Persistent database storage
* User profiles
* Progress analytics
* Mobile application

---

## Phase 3

* Voice-based AI coaching
* Emotion detection
* Long-term behavioral memory
* Personalized AI models
* Community challenges

---

# 🤝 Contributing

Contributions are welcome.

Steps:

```bash
git clone <repository-url>

git checkout -b feature/new-feature

git commit -m "Add new feature"

git push origin feature/new-feature
```

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Sairam Chathurvedi Sreekonda**

Built with ❤️ using:

* React
* FastAPI
* NVIDIA AI
* Modern AI Engineering Practices

---

⭐ If you find this project useful, consider starring the repository.
