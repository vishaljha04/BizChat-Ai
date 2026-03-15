# 🚀 BizChat AI - Intelligent Customer Support Platform

<p align="center">
<img src="https://img.shields.io/badge/version-1.0.0-blue.svg">
<img src="https://img.shields.io/badge/license-MIT-green.svg">
<img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
<img src="https://img.shields.io/badge/React-18.2.0-61DAFB.svg">
<img src="https://img.shields.io/badge/Node.js-18.x-339933.svg">
<img src="https://img.shields.io/badge/MongoDB-8.x-47A248.svg">
<img src="https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg">
</p>

<p align="center">
<b>AI-Powered Customer Support Platform for Businesses</b>
</p>

---

# 🏆 Zerve AI Hackathon Challenge 2026

This project was built for the **Zerve AI Hackathon Challenge 2026**.

The goal of this challenge is to create **real-world AI applications** that solve practical problems using intelligent automation and modern AI tools.

**BizChat AI** helps businesses automate customer support by using:

* AI chat agents
* Semantic search
* Business knowledge retrieval
* Large Language Models

---

# 📋 Table of Contents

* Overview
* Features
* Tech Stack
* Architecture
* Project Structure
* Prerequisites
* Quick Start
* Environment Variables
* Docker Deployment
* Cloud Deployment
* API Documentation
* Core Features
* Security
* Testing
* Troubleshooting
* Contributing
* License
* Author

---

# 📋 Overview

**BizChat AI** is an AI-powered SaaS platform that allows businesses to deploy intelligent chatbots on their websites within minutes.

Using **GPT-4o and semantic search**, the system provides accurate responses to customer queries based on business information such as:

* FAQs
* Services
* Business hours
* Contact information
* Product details

This platform helps businesses:

* automate customer support
* reduce response time
* improve customer experience
* reduce support costs

---

# ✨ Features

| Category             | Features                                   |
| -------------------- | ------------------------------------------ |
| 🤖 AI Chat           | GPT-4o powered conversations               |
| 🔍 Smart Search      | Semantic similarity search with embeddings |
| 📊 Dashboard         | Manage business data and analytics         |
| 💼 Business Profile  | Manage services, FAQs, hours, contact      |
| 🔐 Authentication    | JWT authentication with bcrypt             |
| 📱 Responsive UI     | Tailwind CSS responsive interface          |
| 🌐 Embeddable Widget | Add chatbot with one script                |
| 📈 Analytics         | Track conversations and usage              |

---

# 🛠️ Tech Stack

## Backend

* Node.js
* Express.js
* MongoDB
* Mongoose
* JWT Authentication
* OpenAI API
* bcryptjs
* express-validator
* cors
* dotenv

## Frontend

* React
* Vite
* Tailwind CSS
* React Router
* Axios
* React Context

## DevOps

* Docker
* GitHub Actions
* Vercel
* Railway
* MongoDB Atlas

---

# 🏗️ Architecture

```
Website
   │
   ▼
Chat Widget
   │
   ▼
Express API
   │
   ├ Authentication Service
   ├ Business Management
   └ AI Chat Service
   │
   ▼
Semantic Search Engine
   │
   ▼
OpenAI GPT-4o
   │
   ▼
MongoDB Database
```

---

# 📁 Project Structure

```
bizchat-ai
│
├── backend
│   ├── controllers
│   ├── models
│   ├── routes
│   ├── middleware
│   ├── services
│   └── server.js
│
├── frontend
│   ├── components
│   ├── pages
│   ├── context
│   └── services
│
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

---

# 🔧 Prerequisites

| Tool    | Version |
| ------- | ------- |
| Node.js | ≥ 18.x  |
| npm     | ≥ 9.x   |
| MongoDB | ≥ 6.x   |
| Git     | Latest  |

Optional

* Docker

---

# 🚀 Quick Start

Clone repository

```
git clone https://github.com/yourusername/bizchat-ai.git
cd bizchat-ai
```

Backend setup

```
cd backend
cp .env.example .env
npm install
npm run dev
```

Frontend setup

```
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open in browser

```
http://localhost:3000
```

---

# 🔐 Environment Variables

Backend `.env`

```
PORT=5000
NODE_ENV=development

MONGO_URI=your_mongodb_connection

JWT_SECRET=your_secret
JWT_EXPIRES_IN=7d

OPENAI_API_KEY=your_openai_key

CLIENT_ORIGIN=http://localhost:3000
```

Frontend `.env`

```
VITE_API_URL=http://localhost:5000/api
```

---

# 🐳 Docker Deployment

Run project

```
docker-compose up -d --build
```

Stop project

```
docker-compose down
```

---

# ☁️ Cloud Deployment

Frontend

* Vercel

Backend

* Railway

Database

* MongoDB Atlas

---

# 📡 API Documentation

## Register

POST `/api/auth/register`

```
{
"name": "John Doe",
"email": "john@example.com",
"password": "secure123"
}
```

## Login

POST `/api/auth/login`

```
{
"email": "john@example.com",
"password": "secure123"
}
```

---

## Chat API

POST `/api/chat`

```
{
"businessId": "BUSINESS_ID",
"message": "What are your business hours?"
}
```

Response

```
{
"reply": "We are open Monday to Friday from 9 AM to 5 PM."
}
```

---

# 💡 Core Features

### Semantic Search

Uses OpenAI embeddings to retrieve the most relevant business knowledge.

### Retrieval Augmented Generation (RAG)

Relevant knowledge is injected into the prompt to generate accurate responses.

### Chat Widget

Add chatbot to any website:

```
<script
src="https://your-domain.com/widget.js"
data-business-id="YOUR_BUSINESS_ID">
</script>
```

---

# 🔒 Security

* JWT authentication
* bcrypt password hashing
* input validation
* CORS protection
* XSS protection
* MongoDB sanitization

---

# 🧪 Testing

Backend tests

```
npm test
```

Frontend tests

```
npm run test
```

---

# 🐛 Troubleshooting

| Issue                    | Solution                |
| ------------------------ | ----------------------- |
| MongoDB connection error | Check connection string |
| OpenAI API error         | Verify API key          |
| CORS error               | Verify frontend URL     |
| Widget not loading       | Check business ID       |

---

# 🤝 Contributing

1. Fork repository
2. Create new branch
3. Commit changes
4. Open Pull Request

---

# 📜 License

MIT License

---

# 👨‍💻 Author

**Vishal Jha**

Project built for

🏆 **Zerve AI Hackathon Challenge 2026**

---

⭐ If you like this project, consider giving it a star on GitHub.
