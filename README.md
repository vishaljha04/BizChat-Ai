🚀 BizChat AI - Intelligent Customer Support Platform
<p align="center"> <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version"> <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"> <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"> <img src="https://img.shields.io/badge/React-18.2.0-61DAFB.svg" alt="React"> <img src="https://img.shields.io/badge/Node.js-18.x-339933.svg" alt="Node.js"> <img src="https://img.shields.io/badge/MongoDB-8.2.3-47A248.svg" alt="MongoDB"> <img src="https://img.shields.io/badge/OpenAI-GPT--4-412991.svg" alt="OpenAI"> </p>
📋 Table of Contents
Overview

Features

Tech Stack

Architecture

Project Structure

Prerequisites

Quick Start

Environment Variables

Docker Deployment

Cloud Deployment

API Documentation

Core Features

Security

Testing

Troubleshooting

Contributing

License

Contact

📋 Overview
BizChat AI is a cutting-edge, AI-powered customer support SaaS platform that enables businesses to deploy intelligent chatbots on their websites within minutes. Powered by OpenAI's GPT-4o and semantic search technology, it provides accurate, context-aware responses to customer queries based on your business data.

✨ Features
Category	Features
🤖 AI Chat	GPT-4o powered conversations with semantic understanding
🔍 Smart Search	Cosine similarity search using OpenAI embeddings
📊 Dashboard	Real-time analytics and business configuration
💼 Business Profile	Manage services, FAQs, hours, and contact details
🔐 Authentication	Secure JWT-based auth with bcrypt encryption
📱 Responsive UI	Beautiful Tailwind CSS interface
🌐 Embeddable Widget	One-line script to add chat to any website
📈 Analytics	Track conversations and user engagement
🛠️ Tech Stack
Backend
Node.js 18.x - JavaScript runtime

Express 4.18 - Web framework

MongoDB 8.2 - Database

Mongoose 8.2 - ODM

JWT 9.0 - Authentication

OpenAI 4.47 - AI/ML APIs

bcryptjs - Password hashing

express-validator - Input validation

cors - CORS middleware

dotenv - Environment variables

Frontend
React 18.2 - UI library

Vite 5.2 - Build tool

Tailwind CSS 3.4 - Styling

React Router 6.23 - Navigation

Axios 1.7 - HTTP client

React Context - State management

DevOps & Deployment
Docker 24.0 - Containerization

GitHub Actions - CI/CD

Vercel - Frontend hosting

Railway - Backend hosting

MongoDB Atlas - Cloud database

🏗️ Architecture
text
┌─────────────────────────────────────────────────────────────────┐
│                         🌐 Any Website                          │
│   <script src="widget.js" data-business-id="..."></script>      │
└──────────────────────────┬──────────────────────────────────────┘
                           │  POST /api/chat
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     🚀 Express API (Port 5000)                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  /api/auth   │  │ /api/business│  │     /api/chat        │  │
│  │  JWT Auth    │  │  CRUD Ops    │  │  RAG + GPT-4o       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                  │                     │               │
│         ▼                  ▼                     ▼               │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              MongoDB (Data Persistence)              │       │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │       │
│  │  │  Users  │  │Business │  │Sessions │  │Messages │ │       │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │       │
│  └─────────────────────────────────────────────────────┘       │
│                           │                                     │
│                           ▼                                     │
│                 ┌─────────────────────┐                         │
│                 │   🤖 OpenAI API     │                         │
│                 │  • GPT-4o           │                         │
│                 │  • Embeddings       │                         │
│                 └─────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ⚛️ React Frontend (Port 3000)                 │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   /login     │  │  /register   │  │     /dashboard       │  │
│  │  User Auth   │  │  Sign Up     │  │  Business Config     │  │
│  └──────────────┘  └──────────────┘  └──────────────┬───────┘  │
│                                                      │           │
│  ┌──────────────┐  ┌──────────────┐                  │           │
│  │   /admin     │  │  ChatWidget  │◄─────────────────┘           │
│  │  Analytics   │  │  Embeddable  │                              │
│  └──────────────┘  └──────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
📁 Project Structure
text
bizchat-ai/
├── 📦 backend/
│   ├── 📄 .env.example
│   ├── 📄 package.json
│   ├── 📄 server.js
│   ├── 📁 controllers/
│   │   ├── authController.js
│   │   ├── businessController.js
│   │   ├── chatController.js
│   │   └── adminController.js
│   ├── 📁 models/
│   │   ├── User.js
│   │   ├── Business.js
│   │   ├── ChatSession.js
│   │   └── ChatMessage.js
│   ├── 📁 routes/
│   │   ├── auth.js
│   │   ├── business.js
│   │   ├── chat.js
│   │   └── admin.js
│   ├── 📁 middleware/
│   │   ├── auth.js
│   │   └── validate.js
│   ├── 📁 services/
│   │   ├── embeddingService.js
│   │   └── knowledgeBaseService.js
│   └── 📁 public/
│       └── widget.js
│
├── 🎨 frontend/
│   ├── 📄 .env.example
│   ├── 📄 package.json
│   ├── 📄 vite.config.js
│   ├── 📄 tailwind.config.js
│   ├── 📄 index.html
│   ├── 📁 src/
│   │   ├── 📄 App.jsx
│   │   ├── 📄 main.jsx
│   │   ├── 📄 index.css
│   │   ├── 📁 components/
│   │   │   ├── ChatWidget.jsx
│   │   │   ├── Layout.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── Spinner.jsx
│   │   ├── 📁 pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── AdminPanel.jsx
│   │   ├── 📁 context/
│   │   │   └── AuthContext.jsx
│   │   └── 📁 services/
│   │       └── api.js
│   └── 📁 public/
│       └── widget.js
│
├── 🐳 docker-compose.yml
├── 📦 Dockerfile.backend
├── 📦 Dockerfile.frontend
├── 📄 vercel.json
└── 📄 README.md
🔧 Prerequisites
Tool	Version	Installation
Node.js	≥ 18.x	nodejs.org
npm	≥ 9.x	Comes with Node
MongoDB	≥ 6.x	mongodb.com
Git	≥ 2.40	git-scm.com
Docker (optional)	≥ 24.0	docker.com
🚀 Quick Start (5 minutes)
bash
# 1. Clone repository
git clone https://github.com/yourusername/bizchat-ai.git
cd bizchat-ai

# 2. Backend setup
cd backend
cp .env.example .env
npm install

# 3. Frontend setup
cd ../frontend
cp .env.example .env
npm install

# 4. Start development servers
# Terminal 1 - Backend
cd backend && npm run dev

# Terminal 2 - Frontend
cd frontend && npm run dev

# 5. Open browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
🔐 Environment Variables
Backend .env
env
# Server Configuration
PORT=5000
NODE_ENV=development

# MongoDB Connection
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/bizchat

# JWT Authentication
JWT_SECRET=your-super-secret-jwt-key-change-this
JWT_EXPIRES_IN=7d

# OpenAI API
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# CORS Settings
CLIENT_ORIGIN=http://localhost:3000
Frontend .env
env
VITE_API_URL=http://localhost:5000/api
🐳 Docker Deployment
Using Docker Compose
bash
# Build and run all services
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
docker-compose.yml
yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6
    container_name: bizchat-mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: bizchat
    volumes:
      - mongodb_data:/data/db

  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile.backend
    container_name: bizchat-backend
    restart: always
    ports:
      - "5000:5000"
    environment:
      - NODE_ENV=production
      - PORT=5000
      - MONGO_URI=mongodb://admin:password123@mongodb:27017/bizchat?authSource=admin
      - JWT_SECRET=your_super_secret_jwt_key_here
      - JWT_EXPIRES_IN=7d
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - CLIENT_ORIGIN=http://localhost:3000
    depends_on:
      - mongodb
    volumes:
      - ./backend:/app
      - /app/node_modules

  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile.frontend
    container_name: bizchat-frontend
    restart: always
    ports:
      - "3000:80"
    environment:
      - VITE_API_URL=http://localhost:5000/api
    depends_on:
      - backend

volumes:
  mongodb_data:
Dockerfile.backend
dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

RUN mkdir -p public
COPY public/widget.js ./public/

EXPOSE 5000

CMD ["node", "server.js"]
Dockerfile.frontend
dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
☁️ Cloud Deployment
Frontend (Vercel)
Push code to GitHub

Import project to Vercel

Set environment variable: VITE_API_URL=https://your-backend-url.com/api

Deploy!

vercel.json
json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-url.vercel.app/api/$1"
    }
  ],
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "installCommand": "cd frontend && npm install",
  "devCommand": "cd frontend && npm run dev"
}
Backend (Railway)
Create account on Railway

Connect GitHub repository

Set environment variables

Deploy!

Database (MongoDB Atlas)
Create cluster at MongoDB Atlas

Get connection string

Add to backend .env

📡 API Documentation
Authentication Endpoints
POST /api/auth/register
json
// Request
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure123"
}

// Response (201)
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "_id": "65f1a2b3c4d5e6f7g8h9i0j1",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "businessId": "65f1a2b3c4d5e6f7g8h9i0j2"
}
POST /api/auth/login
json
// Request
{
  "email": "john@example.com",
  "password": "secure123"
}

// Response (200)
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "_id": "65f1a2b3c4d5e6f7g8h9i0j1",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "businessId": "65f1a2b3c4d5e6f7g8h9i0j2"
}
GET /api/auth/me (Protected)
json
// Headers
Authorization: Bearer <token>

// Response (200)
{
  "user": {
    "_id": "65f1a2b3c4d5e6f7g8h9i0j1",
    "name": "John Doe",
    "email": "john@example.com",
    "business": {
      "_id": "65f1a2b3c4d5e6f7g8h9i0j2",
      "name": "John's Business"
    }
  }
}
Chat Endpoint
POST /api/chat
json
// Request
{
  "businessId": "65f1a2b3c4d5e6f7g8h9i0j2",
  "message": "What are your business hours?",
  "sessionId": "optional-existing-session-id",
  "visitorId": "optional-visitor-id"
}

// Response (200)
{
  "reply": "We're open Monday to Friday, 9 AM to 5 PM EST.",
  "sessionId": "65f1a2b3c4d5e6f7g8h9i0j3"
}
Business Endpoints (Protected)
GET /api/business
json
// Headers
Authorization: Bearer <token>

// Response (200)
{
  "business": {
    "_id": "65f1a2b3c4d5e6f7g8h9i0j2",
    "name": "Acme Corp",
    "description": "Leading provider of...",
    "services": [
      {
        "name": "Basic Plan",
        "description": "Essential features",
        "price": "$29/month"
      }
    ],
    "faqs": [
      {
        "question": "What is your refund policy?",
        "answer": "30-day money-back guarantee"
      }
    ],
    "hours": [
      {
        "day": "Monday",
        "open": "09:00",
        "close": "17:00",
        "closed": false
      }
    ],
    "contact": {
      "email": "info@acme.com",
      "phone": "+1-555-0123",
      "address": "123 Business St",
      "website": "https://acme.com"
    }
  }
}
PUT /api/business (Full Update)
json
// Headers
Authorization: Bearer <token>

// Request Body
{
  "name": "Updated Business Name",
  "description": "New description",
  "services": [...],
  "faqs": [...],
  "hours": [...],
  "contact": {...}
}
Admin Endpoints (Protected)
GET /api/admin/chats?page=1&limit=20
json
// Response
{
  "sessions": [...],
  "pagination": {
    "total": 150,
    "page": 1,
    "limit": 20,
    "pages": 8
  }
}
GET /api/admin/chats/:sessionId/messages
json
// Response
{
  "session": {...},
  "messages": [...]
}
PATCH /api/admin/business
json
// Partial Update
{
  "faqs": [...],
  "name": "New Name"
}
💡 Core Features Deep Dive
1. Semantic Search with Embeddings
javascript
// embeddingService.js
const OpenAI = require('openai');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function getEmbedding(text) {
  const response = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: text.replace(/\n/g, ' ').trim(),
  });
  return response.data[0].embedding;
}

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function searchSimilar(query, candidates, topK = 5) {
  const queryVec = await getEmbedding(query);
  return candidates
    .map(c => ({ 
      text: c.text, 
      score: cosineSimilarity(queryVec, c.embedding) 
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}
2. Knowledge Base Service
javascript
// knowledgeBaseService.js
async function indexBusinessKnowledge(businessId) {
  const business = await Business.findById(businessId);
  
  // Index overview
  const overviewText = [
    business.name,
    business.description,
    business.services.map(s => `${s.name}: ${s.description}`).join('. ')
  ].join(' ');
  
  business.overviewEmbedding = await getEmbedding(overviewText);
  
  // Index FAQs
  for (const faq of business.faqs) {
    const text = `${faq.question} ${faq.answer}`;
    faq.embedding = await getEmbedding(text);
  }
  
  await business.save();
}
3. Chat Controller with RAG
javascript
// chatController.js
const chat = async (req, res) => {
  const { businessId, message, sessionId } = req.body;
  
  // Load business and knowledge chunks
  const business = await Business.findById(businessId);
  const chunks = buildKnowledgeChunks(business);
  
  // Semantic search
  const relevant = await searchSimilar(message, chunks, 5);
  const context = relevant
    .filter(r => r.score > 0.25)
    .map(r => r.text)
    .join('\n\n');
  
  // Build system prompt
  const systemPrompt = `You are a support assistant for ${business.name}.
  ${context ? `Relevant info:\n${context}` : ''}`;
  
  // Get GPT-4o response
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: systemPrompt },
      ...historyMessages
    ]
  });
  
  // Save and return response
  const reply = completion.choices[0].message.content;
  res.json({ reply, sessionId });
};
4. Chat Widget Embedding
Add this to any website:

html
<script
  src="https://your-domain.com/widget.js"
  data-business-id="YOUR_BUSINESS_ID"
  data-api-base="https://your-api.com/api"
  data-primary-color="#4f46e5"
  data-title="Chat with Support"
  data-greeting="👋 How can I help you today?">
</script>
5. Widget.js Implementation
javascript
// public/widget.js
(function() {
  const scriptEl = document.currentScript;
  const businessId = scriptEl.getAttribute('data-business-id');
  
  if (!businessId) {
    console.warn('[BizChat] Missing business ID');
    return;
  }
  
  // Load React and mount widget
  function loadScript(src, onload) {
    const s = document.createElement('script');
    s.src = src;
    s.onload = onload;
    document.head.appendChild(s);
  }
  
  loadScript('https://esm.sh/react@18', () => {
    loadScript('https://esm.sh/react-dom@18/client', mountWidget);
  });
  
  function mountWidget() {
    // Widget component implementation
    const container = document.createElement('div');
    document.body.appendChild(container);
    // React rendering logic...
  }
})();
🔒 Security Features
✅ JWT Authentication - Secure token-based auth with expiration

✅ Password Hashing - bcrypt with 12 salt rounds

✅ CORS Protection - Configurable allowed origins

✅ Input Validation - express-validator middleware

✅ XSS Prevention - Automatic escaping in React

✅ Rate Limiting - DDoS protection (optional)

✅ MongoDB Injection - Mongoose sanitization

✅ Helmet.js - Security headers (optional)

🧪 Testing
bash
# Backend tests
cd backend
npm install --save-dev jest supertest
npm test

# Example test file
cat > backend/tests/auth.test.js << 'EOF'
const request = require('supertest');
const app = require('../server');

describe('Auth Endpoints', () => {
  it('should register a new user', async () => {
    const res = await request(app)
      .post('/api/auth/register')
      .send({
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123'
      });
    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('token');
  });
});
EOF

# Frontend tests
cd frontend
npm test

# E2E tests
npm install --save-dev cypress
npm run test:e2e
🐛 Troubleshooting
Common Issues & Solutions
Issue	Solution
MongoDB connection error	Check connection string and network
OpenAI API rate limits	Implement retry logic with exponential backoff
CORS errors	Verify CLIENT_ORIGIN matches frontend URL
JWT invalid	Check JWT_SECRET consistency across deployments
Widget not loading	Verify businessId and API endpoint
Embedding generation fails	Check OpenAI API key and credits
Build fails	Clear npm cache and node_modules
Debug Mode
bash
# Backend debug
DEBUG=express:* npm run dev

# Frontend debug
npm run dev -- --debug

# MongoDB debug
mongod --dbpath=data --verbose
🤝 Contributing
We welcome contributions! Please follow these steps:

Fork the repository

Create feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open a Pull Request

Development Guidelines
Follow ESLint configuration

Write unit tests for new features

Update documentation

Use conventional commits

Add comments for complex logic

📄 License
MIT © BizChat AI

📞 Contact & Support
Documentation: docs.bizchat.ai

Email: support@bizchat.ai

Twitter: @BizChatAI

Discord: Join our server

GitHub Issues: Report bug

<p align="center"> Made with ❤️ by the BizChat AI Team <br> <sub>Empowering businesses with AI-powered customer support</sub> </p><p align="center"> <a href="#-overview">Overview</a> • <a href="#-quick-start-5-minutes">Quick Start</a> • <a href="#-api-documentation">API</a> • <a href="#-docker-deployment">Docker</a> • <a href="#-contributing">Contributing</a> </p>
