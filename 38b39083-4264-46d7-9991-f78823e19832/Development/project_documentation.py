
import os, json

def write_file(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════════════════
# 1. README.md
# ══════════════════════════════════════════════════════════
write_file("README.md", """\
# BizChat AI — Customer Support Chatbot Platform

> An AI-powered customer support SaaS that lets businesses embed a smart chat widget on their website in minutes.  
> Built with **Node.js + Express**, **MongoDB**, **OpenAI GPT-4o** (with semantic embeddings), and a **React + Vite** frontend.

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Running the App](#running-the-app)
- [Embedding the Chat Widget](#embedding-the-chat-widget)
- [API Reference](#api-reference)

---

## ✨ Features

| Category | Feature |
|---|---|
| **Auth** | JWT-based registration & login; password hashing via bcryptjs |
| **Business Profile** | Create / update business name, description, services, FAQs, hours, and contact details |
| **AI Chat** | GPT-4o powered chat with semantic retrieval-augmented generation (RAG) |
| **Embeddings** | OpenAI `text-embedding-3-small` used to pre-compute FAQ + overview vectors |
| **RAG Search** | Cosine-similarity search surfaces the top-5 most relevant knowledge chunks per query |
| **Chat Sessions** | Persistent session tracking with visitor ID support and message history |
| **Admin Panel** | Paginated chat session viewer; per-session message history; live knowledge-base editor |
| **Embeddable Widget** | Self-contained `widget.js` — drop a single `<script>` tag on any website |
| **React App** | Login, Register, Dashboard (widget preview + business config), Admin Panel pages |
| **Validation** | `express-validator` middleware on all public endpoints |
| **CORS** | Configurable allowed origin via `CLIENT_ORIGIN` env var |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Any Website                              │
│   <script src="widget.js" data-business-id="..."></script>      │
└──────────────────────────┬──────────────────────────────────────┘
                           │  POST /api/chat
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Express API  (port 5000)                      │
│                                                                 │
│  /api/auth     ──►  authController    ──►  User (MongoDB)       │
│  /api/business ──►  businessController──►  Business (MongoDB)   │
│  /api/chat     ──►  chatController    ──►  ChatSession/Message  │
│  /api/admin    ──►  adminController   ──►  (protected)          │
│                                                                 │
│  chatController:                                                │
│    1. Load Business doc                                         │
│    2. buildKnowledgeChunks()  (FAQs + overview)                 │
│    3. searchSimilar()         (cosine similarity via embeddings) │
│    4. GPT-4o chat completion  (RAG system prompt)               │
│    5. Persist ChatMessage & update ChatSession                  │
└──────────────┬──────────────────────┬───────────────────────────┘
               │                      │
               ▼                      ▼
        ┌─────────────┐       ┌──────────────────┐
        │   MongoDB   │       │   OpenAI API      │
        │  (Atlas /   │       │  GPT-4o           │
        │   local)    │       │  text-embedding   │
        └─────────────┘       └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│               React Frontend  (Vite, port 3000)                 │
│                                                                 │
│   /login     ──►  Login page                                    │
│   /register  ──►  Register page                                 │
│   /dashboard ──►  Business config + live widget preview         │
│   /admin     ──►  Chat session viewer + knowledge base editor   │
│                                                                 │
│   All requests to /api/* are proxied to localhost:5000          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Prerequisites

| Tool | Version | Notes |
|---|---|---|
| **Node.js** | ≥ 18.x | [nodejs.org](https://nodejs.org) |
| **npm** | ≥ 9.x | Comes with Node |
| **MongoDB** | Atlas cluster **or** local ≥ 6.x | [mongodb.com/atlas](https://www.mongodb.com/atlas) |
| **OpenAI API Key** | — | [platform.openai.com](https://platform.openai.com) |

---

## ⚙️ Local Setup

### 1 — Clone the repository

```bash
git clone https://github.com/your-org/bizchat-ai.git
cd bizchat-ai
```

### 2 — Configure the Backend

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and fill in the required values:

```env
PORT=5000
NODE_ENV=development
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=7d
OPENAI_API_KEY=sk-...
CLIENT_ORIGIN=http://localhost:3000
```

> **Tip:** For local MongoDB use `MONGO_URI=mongodb://localhost:27017/bizchat`

### 3 — Install Backend Dependencies

```bash
cd backend
npm install
```

### 4 — Configure the Frontend

```bash
cd ../frontend
cp .env.example .env
```

Open `frontend/.env` and set the API URL:

```env
VITE_API_URL=http://localhost:5000/api
```

> **Note:** When running locally the Vite dev server already proxies `/api/*` to `localhost:5000`, so this variable is mainly used when building for production.

### 5 — Install Frontend Dependencies

```bash
npm install
```

---

## 🚀 Running the App

### Backend (with hot-reload via nodemon)

```bash
cd backend
npm run dev        # starts nodemon → http://localhost:5000
```

Or for production:

```bash
npm start          # plain node server.js
```

### Frontend (Vite dev server)

```bash
cd frontend
npm run dev        # starts Vite → http://localhost:3000
```

Open **http://localhost:3000** in your browser.  
Register an account → configure your business → start chatting!

### Running both concurrently (optional)

Install `concurrently` at the root and add a root `package.json`:

```bash
npm install -g concurrently
concurrently "cd backend && npm run dev" "cd frontend && npm run dev"
```

---

## 🌐 Embedding the Chat Widget

Once your backend is deployed, add this single `<script>` tag to **any website**:

```html
<script
  src="https://your-domain.com/widget.js"
  data-business-id="YOUR_BUSINESS_MONGO_ID"
  data-api-base="https://your-api.com/api"
  data-title="Chat with us"
  data-primary-color="#4f46e5"
  data-greeting="👋 Hi! How can I help you today?"
></script>
```

### Widget Attributes

| Attribute | Required | Default | Description |
|---|---|---|---|
| `data-business-id` | ✅ Yes | — | Your MongoDB Business `_id` |
| `data-api-base` | No | `https://your-api.com/api` | Base URL of your deployed API |
| `data-title` | No | `Chat with us` | Widget header title |
| `data-primary-color` | No | `#4f46e5` (indigo) | Accent color for bubble & buttons |
| `data-greeting` | No | `👋 Hi there! How can I help you today?` | First bot message |

The widget is **self-contained** — it dynamically loads React 18 from a CDN and mounts into an isolated DOM node so it never conflicts with the host page's JavaScript.

---

## 📡 API Reference

All endpoints are prefixed with `/api`.  
Protected endpoints require an `Authorization: Bearer <token>` header.

---

### Auth — `/api/auth`

#### `POST /api/auth/register`

Create a new account. Automatically provisions an empty Business record.

**Request body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "securepassword"
}
```

**Response `201`:**
```json
{
  "token": "<jwt>",
  "user": { "_id": "...", "name": "Jane Doe", "email": "jane@example.com", "role": "owner" },
  "businessId": "<business_id>"
}
```

**Errors:** `409 Email already in use` | `422 Validation errors`

---

#### `POST /api/auth/login`

Authenticate and receive a JWT.

**Request body:**
```json
{
  "email": "jane@example.com",
  "password": "securepassword"
}
```

**Response `200`:**
```json
{
  "token": "<jwt>",
  "user": { "_id": "...", "name": "Jane Doe", "email": "jane@example.com" },
  "businessId": "<business_id>"
}
```

**Errors:** `401 Invalid credentials` | `422 Validation errors`

---

#### `GET /api/auth/me` 🔒

Returns the currently authenticated user with populated business.

**Response `200`:**
```json
{
  "user": {
    "_id": "...",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "business": { "_id": "...", "name": "Jane's Business", ... }
  }
}
```

---

### Chat — `/api/chat`

#### `POST /api/chat`

Send a message to the AI chatbot for a specific business.  
No authentication required — designed for public widget use.

**Request body:**
```json
{
  "businessId": "<business_mongo_id>",
  "message": "What are your opening hours?",
  "sessionId": "<optional_existing_session_id>",
  "visitorId": "<optional_anonymous_visitor_id>"
}
```

**Response `200`:**
```json
{
  "reply": "We're open Monday–Friday, 9 AM–5 PM.",
  "sessionId": "<session_id>"
}
```

**How it works:**
1. Loads the Business document and its precomputed embeddings.
2. Embeds the user message and finds the top-5 most semantically similar knowledge chunks (cosine similarity ≥ 0.25).
3. Injects them as context into a GPT-4o system prompt.
4. Returns the AI reply and persists both messages to `ChatSession` / `ChatMessage`.

**Errors:** `400 businessId and message are required` | `404 Business not found` | `422 Validation errors`

---

### Business — `/api/business` 🔒

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/business` | Get the authenticated owner's business |
| `POST` | `/api/business` | Create a business (if missing) |
| `PUT` | `/api/business` | Full update + trigger background knowledge re-indexing |

**PUT request body example:**
```json
{
  "name": "Acme Corp",
  "description": "We sell premium widgets.",
  "services": [{ "name": "Widget Pro", "description": "Best widget", "price": "$99/mo" }],
  "faqs": [{ "question": "Do you offer refunds?", "answer": "Yes, within 30 days." }],
  "hours": [{ "day": "Monday", "open": "09:00", "close": "17:00" }],
  "contact": { "email": "hello@acme.com", "phone": "+1 555-0100", "website": "https://acme.com" }
}
```

---

### Admin — `/api/admin` 🔒

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/admin/chats?page=1&limit=20` | Paginated chat sessions for your business |
| `GET` | `/api/admin/chats/:sessionId/messages` | All messages in a specific session |
| `PATCH` | `/api/admin/business` | Partial business update + background re-indexing |

---

## 📁 Project Structure

```
bizchat-ai/
├── README.md
├── backend/
│   ├── .env.example
│   ├── package.json
│   ├── server.js
│   ├── middleware/
│   │   ├── auth.js
│   │   └── validate.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Business.js
│   │   ├── ChatSession.js
│   │   └── ChatMessage.js
│   ├── controllers/
│   │   ├── authController.js
│   │   ├── businessController.js
│   │   ├── chatController.js
│   │   └── adminController.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── business.js
│   │   ├── chat.js
│   │   └── admin.js
│   └── services/
│       ├── embeddingService.js
│       └── knowledgeBaseService.js
└── frontend/
    ├── .env.example
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── context/
        │   └── AuthContext.jsx
        ├── components/
        │   ├── ChatWidget.jsx
        │   ├── Layout.jsx
        │   ├── Navbar.jsx
        │   ├── ProtectedRoute.jsx
        │   └── Spinner.jsx
        ├── pages/
        │   ├── Login.jsx
        │   ├── Register.jsx
        │   ├── Dashboard.jsx
        │   └── AdminPanel.jsx
        ├── services/
        │   └── api.js
        └── public/
            └── widget.js
```

---

## 🛡️ License

MIT © BizChat AI
""")

# ══════════════════════════════════════════════════════════
# 2. frontend/.env.example
# ══════════════════════════════════════════════════════════
write_file("frontend/.env.example", """\
# ── API ─────────────────────────────────────────────────
# Base URL of the backend API (used in production builds)
# During local development the Vite proxy handles /api/* automatically.
VITE_API_URL=http://localhost:5000/api
""")

# ══════════════════════════════════════════════════════════
# 3. Verify / update backend/package.json — ensure nodemon script
# ══════════════════════════════════════════════════════════
backend_pkg_path = "backend/package.json"
with open(backend_pkg_path) as f:
    backend_pkg = json.load(f)

backend_pkg["scripts"] = {
    "start": "node server.js",
    "dev":   "nodemon server.js"
}
backend_pkg["devDependencies"] = backend_pkg.get("devDependencies", {})
backend_pkg["devDependencies"]["nodemon"] = "^3.1.0"

with open(backend_pkg_path, "w") as f:
    json.dump(backend_pkg, f, indent=2)
print(f"✅  {backend_pkg_path}  (scripts verified: start + dev/nodemon)")

# ══════════════════════════════════════════════════════════
# 4. Verify / update frontend/package.json — ensure vite scripts
# ══════════════════════════════════════════════════════════
frontend_pkg_path = "frontend/package.json"
with open(frontend_pkg_path) as f:
    frontend_pkg = json.load(f)

frontend_pkg["scripts"] = {
    "dev":     "vite",
    "build":   "vite build",
    "preview": "vite preview",
    "lint":    "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
}

with open(frontend_pkg_path, "w") as f:
    json.dump(frontend_pkg, f, indent=2)
print(f"✅  {frontend_pkg_path}  (scripts verified: dev/build/preview/lint)")

# ══════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════
print()
print("=" * 55)
print("  Documentation files written successfully!")
print("=" * 55)
print()
print("  Files created / updated:")
print("  ├── README.md                 (full project docs)")
print("  ├── frontend/.env.example     (VITE_API_URL)")
print("  ├── backend/package.json      (start + dev/nodemon)")
print("  └── frontend/package.json     (dev/build/preview/lint)")
print()
print("  Quick start:")
print("  1.  cp backend/.env.example backend/.env   # fill values")
print("  2.  cp frontend/.env.example frontend/.env")
print("  3.  cd backend  && npm install && npm run dev")
print("  4.  cd frontend && npm install && npm run dev")
print("  5.  Open http://localhost:3000")
