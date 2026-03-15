
import os

# ─────────────────────────────────────────────
# Helper to write files, creating dirs as needed
# ─────────────────────────────────────────────
def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

BASE = "backend"

# ══════════════════════════════════════════════
# 1. .env.example
# ══════════════════════════════════════════════
write_file(f"{BASE}/.env.example", """\
# ── Server ──────────────────────────────────
PORT=5000
NODE_ENV=development

# ── MongoDB ─────────────────────────────────
MONGO_URI=mongodb+srv://<user>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority

# ── JWT ─────────────────────────────────────
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=7d

# ── OpenAI ──────────────────────────────────
OPENAI_API_KEY=sk-...

# ── CORS ─────────────────────────────────────
CLIENT_ORIGIN=http://localhost:3000
""")

# ══════════════════════════════════════════════
# 2. package.json
# ══════════════════════════════════════════════
write_file(f"{BASE}/package.json", """\
{
  "name": "chatbot-backend",
  "version": "1.0.0",
  "description": "Express + MongoDB backend for AI chatbot SaaS",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "bcryptjs": "^2.4.3",
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.18.3",
    "express-validator": "^7.0.1",
    "jsonwebtoken": "^9.0.2",
    "mongoose": "^8.2.3",
    "openai": "^4.47.1"
  },
  "devDependencies": {
    "nodemon": "^3.1.0"
  }
}
""")

# ══════════════════════════════════════════════
# 3. server.js  (entry point)
# ══════════════════════════════════════════════
write_file(f"{BASE}/server.js", """\
require('dotenv').config();
const express = require('express');
const cors    = require('cors');
const mongoose = require('mongoose');

const authRoutes     = require('./routes/auth');
const businessRoutes = require('./routes/business');
const chatRoutes     = require('./routes/chat');
const adminRoutes    = require('./routes/admin');

const app = express();

// ── Middleware ────────────────────────────────
app.use(cors({
  origin: process.env.CLIENT_ORIGIN || '*',
  credentials: true,
}));
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));

// ── Routes ────────────────────────────────────
app.use('/api/auth',     authRoutes);
app.use('/api/business', businessRoutes);
app.use('/api/chat',     chatRoutes);
app.use('/api/admin',    adminRoutes);

// ── Health check ──────────────────────────────
app.get('/health', (_req, res) => res.json({ status: 'ok' }));

// ── 404 handler ───────────────────────────────
app.use((_req, res) => res.status(404).json({ message: 'Route not found' }));

// ── Global error handler ──────────────────────
app.use((err, _req, res, _next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({ message: err.message || 'Internal server error' });
});

// ── Database + server start ───────────────────
const PORT = process.env.PORT || 5000;

mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log('✅  MongoDB connected');
    app.listen(PORT, () => console.log(`🚀  Server running on port ${PORT}`));
  })
  .catch((err) => {
    console.error('❌  MongoDB connection error:', err.message);
    process.exit(1);
  });
""")

# ══════════════════════════════════════════════
# 4. Models
# ══════════════════════════════════════════════

# ── User ─────────────────────────────────────
write_file(f"{BASE}/models/User.js", """\
const mongoose = require('mongoose');
const bcrypt   = require('bcryptjs');

const userSchema = new mongoose.Schema(
  {
    name:     { type: String, required: true, trim: true },
    email:    { type: String, required: true, unique: true, lowercase: true, trim: true },
    password: { type: String, required: true, minlength: 6 },
    // Reference to the business this owner manages
    business: { type: mongoose.Schema.Types.ObjectId, ref: 'Business', default: null },
    role:     { type: String, enum: ['owner', 'admin'], default: 'owner' },
  },
  { timestamps: true }
);

// Hash password before saving
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();
  const salt = await bcrypt.genSalt(12);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

// Compare plain text vs stored hash
userSchema.methods.comparePassword = function (plain) {
  return bcrypt.compare(plain, this.password);
};

// Never expose hashed password in JSON responses
userSchema.methods.toJSON = function () {
  const obj = this.toObject();
  delete obj.password;
  return obj;
};

module.exports = mongoose.model('User', userSchema);
""")

# ── Business ──────────────────────────────────
write_file(f"{BASE}/models/Business.js", """\
const mongoose = require('mongoose');

const hoursSchema = new mongoose.Schema(
  {
    day:   { type: String, required: true }, // e.g. "Monday"
    open:  { type: String },                 // e.g. "09:00"
    close: { type: String },                 // e.g. "17:00"
    closed: { type: Boolean, default: false },
  },
  { _id: false }
);

const faqSchema = new mongoose.Schema(
  {
    question:  { type: String, required: true },
    answer:    { type: String, required: true },
    // Precomputed OpenAI embedding for cosine similarity search
    embedding: { type: [Number], default: [] },
  },
  { _id: true }
);

const serviceSchema = new mongoose.Schema(
  {
    name:        { type: String, required: true },
    description: { type: String },
    price:       { type: String },
  },
  { _id: true }
);

const businessSchema = new mongoose.Schema(
  {
    owner:       { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    name:        { type: String, required: true, trim: true },
    description: { type: String, default: '' },
    services:    [serviceSchema],
    faqs:        [faqSchema],
    hours:       [hoursSchema],
    contact: {
      email:   { type: String },
      phone:   { type: String },
      address: { type: String },
      website: { type: String },
    },
    // Flat text blob embedding (covers description + services text)
    overviewEmbedding: { type: [Number], default: [] },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Business', businessSchema);
""")

# ── ChatSession ───────────────────────────────
write_file(f"{BASE}/models/ChatSession.js", """\
const mongoose = require('mongoose');

const chatSessionSchema = new mongoose.Schema(
  {
    business:  { type: mongoose.Schema.Types.ObjectId, ref: 'Business', required: true },
    // Optional: visitor identifier (IP hash, anonymous ID, etc.)
    visitorId: { type: String, default: null },
    // Quick reference: how many messages in the session
    messageCount: { type: Number, default: 0 },
    // Copy of last message snippet for admin preview
    lastMessage:  { type: String, default: '' },
  },
  { timestamps: true }
);

module.exports = mongoose.model('ChatSession', chatSessionSchema);
""")

# ── ChatMessage ───────────────────────────────
write_file(f"{BASE}/models/ChatMessage.js", """\
const mongoose = require('mongoose');

const chatMessageSchema = new mongoose.Schema(
  {
    session:  { type: mongoose.Schema.Types.ObjectId, ref: 'ChatSession', required: true },
    business: { type: mongoose.Schema.Types.ObjectId, ref: 'Business',   required: true },
    role:     { type: String, enum: ['user', 'assistant'], required: true },
    content:  { type: String, required: true },
  },
  { timestamps: true }
);

module.exports = mongoose.model('ChatMessage', chatMessageSchema);
""")

# ══════════════════════════════════════════════
# 5. Middleware
# ══════════════════════════════════════════════
write_file(f"{BASE}/middleware/auth.js", """\
const jwt  = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Protects routes — verifies Bearer JWT and attaches req.user
 */
const protect = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Not authenticated — no token provided' });
  }

  const token = authHeader.split(' ')[1];
  const decoded = jwt.verify(token, process.env.JWT_SECRET); // throws on invalid
  const user = await User.findById(decoded.id).select('-password');
  if (!user) return res.status(401).json({ message: 'User no longer exists' });

  req.user = user;
  next();
};

module.exports = { protect };
""")

# ══════════════════════════════════════════════
# 6. Services
# ══════════════════════════════════════════════
write_file(f"{BASE}/services/embeddingService.js", """\
const OpenAI = require('openai');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const EMBED_MODEL = 'text-embedding-3-small'; // fast + cheap

/**
 * Returns an embedding vector for a single text string.
 * @param {string} text
 * @returns {Promise<number[]>}
 */
async function getEmbedding(text) {
  const response = await openai.embeddings.create({
    model: EMBED_MODEL,
    input: text.replace(/\\n/g, ' ').trim(),
  });
  return response.data[0].embedding;
}

/**
 * Cosine similarity between two equal-length vectors.
 * @param {number[]} a
 * @param {number[]} b
 * @returns {number}  value in [-1, 1]
 */
function cosineSimilarity(a, b) {
  if (a.length !== b.length) throw new Error('Vector length mismatch');
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot   += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Given a query and a list of { text, embedding } objects, returns the
 * top-k most similar entries sorted by cosine similarity (descending).
 *
 * @param {string}   query
 * @param {{ text: string, embedding: number[] }[]} candidates
 * @param {number}   topK
 * @returns {Promise<{ text: string, score: number }[]>}
 */
async function searchSimilar(query, candidates, topK = 5) {
  const queryVec = await getEmbedding(query);
  return candidates
    .map((c) => ({ text: c.text, score: cosineSimilarity(queryVec, c.embedding) }))
    .sort((a, b) => b.score - a.score)
    .slice(0, topK);
}

module.exports = { getEmbedding, cosineSimilarity, searchSimilar };
""")

write_file(f"{BASE}/services/knowledgeBaseService.js", """\
const Business          = require('../models/Business');
const { getEmbedding }  = require('./embeddingService');

/**
 * (Re)computes embeddings for all FAQs and the overview text of a business,
 * then persists them back to MongoDB.
 *
 * @param {string} businessId  Mongoose ObjectId string
 * @returns {Promise<void>}
 */
async function indexBusinessKnowledge(businessId) {
  const business = await Business.findById(businessId);
  if (!business) throw new Error('Business not found');

  // ── Overview embedding ───────────────────────────────
  const overviewText = [
    business.name,
    business.description,
    business.services.map((s) => `${s.name}: ${s.description || ''}`).join('. '),
  ]
    .filter(Boolean)
    .join(' ');

  business.overviewEmbedding = overviewText ? await getEmbedding(overviewText) : [];

  // ── FAQ embeddings ────────────────────────────────────
  for (const faq of business.faqs) {
    const text = `${faq.question} ${faq.answer}`;
    faq.embedding = await getEmbedding(text);
  }

  await business.save();
}

/**
 * Builds a flat list of { text, embedding } knowledge chunks from a business doc.
 * Used by the chat service for similarity search.
 *
 * @param {object} business  Mongoose Business document
 * @returns {{ text: string, embedding: number[] }[]}
 */
function buildKnowledgeChunks(business) {
  const chunks = [];

  // Overview
  if (business.overviewEmbedding.length > 0) {
    const text = [
      `Business: ${business.name}`,
      business.description ? `About: ${business.description}` : '',
    ]
      .filter(Boolean)
      .join(' ');
    chunks.push({ text, embedding: business.overviewEmbedding });
  }

  // FAQs
  for (const faq of business.faqs) {
    if (faq.embedding.length > 0) {
      chunks.push({
        text: `Q: ${faq.question}\\nA: ${faq.answer}`,
        embedding: faq.embedding,
      });
    }
  }

  return chunks;
}

module.exports = { indexBusinessKnowledge, buildKnowledgeChunks };
""")

# ══════════════════════════════════════════════
# 7. Controllers
# ══════════════════════════════════════════════

# ── Auth controller ───────────────────────────
write_file(f"{BASE}/controllers/authController.js", """\
const jwt      = require('jsonwebtoken');
const User     = require('../models/User');
const Business = require('../models/Business');

/** Generates a signed JWT for the given user id */
const signToken = (id) =>
  jwt.sign({ id }, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  });

// ─────────────────────────────────────────────
// POST /api/auth/register
// ─────────────────────────────────────────────
const register = async (req, res) => {
  const { name, email, password } = req.body;

  const existing = await User.findOne({ email });
  if (existing) return res.status(409).json({ message: 'Email already in use' });

  const user = await User.create({ name, email, password });

  // Auto-create an empty Business record for this owner
  const business = await Business.create({ owner: user._id, name: `${name}'s Business` });
  user.business = business._id;
  await user.save();

  const token = signToken(user._id);
  res.status(201).json({ token, user, businessId: business._id });
};

// ─────────────────────────────────────────────
// POST /api/auth/login
// ─────────────────────────────────────────────
const login = async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email }).select('+password');
  if (!user) return res.status(401).json({ message: 'Invalid credentials' });

  const valid = await user.comparePassword(password);
  if (!valid) return res.status(401).json({ message: 'Invalid credentials' });

  const token = signToken(user._id);
  res.json({ token, user: user.toJSON(), businessId: user.business });
};

// ─────────────────────────────────────────────
// GET /api/auth/me  (protected)
// ─────────────────────────────────────────────
const getMe = async (req, res) => {
  const user = await User.findById(req.user._id).populate('business');
  res.json({ user });
};

module.exports = { register, login, getMe };
""")

# ── Business controller ───────────────────────
write_file(f"{BASE}/controllers/businessController.js", """\
const Business = require('../models/Business');
const { indexBusinessKnowledge } = require('../services/knowledgeBaseService');

// ─────────────────────────────────────────────
// GET /api/business  — get owner's business
// ─────────────────────────────────────────────
const getBusiness = async (req, res) => {
  const business = await Business.findOne({ owner: req.user._id });
  if (!business) return res.status(404).json({ message: 'Business not found' });
  res.json({ business });
};

// ─────────────────────────────────────────────
// POST /api/business  — create (if somehow missing)
// ─────────────────────────────────────────────
const createBusiness = async (req, res) => {
  const exists = await Business.findOne({ owner: req.user._id });
  if (exists) return res.status(409).json({ message: 'Business already exists', business: exists });

  const business = await Business.create({ ...req.body, owner: req.user._id });
  res.status(201).json({ business });
};

// ─────────────────────────────────────────────
// PUT /api/business  — full update + re-index knowledge
// ─────────────────────────────────────────────
const updateBusiness = async (req, res) => {
  const { name, description, services, faqs, hours, contact } = req.body;

  const business = await Business.findOneAndUpdate(
    { owner: req.user._id },
    { name, description, services, faqs, hours, contact },
    { new: true, runValidators: true }
  );
  if (!business) return res.status(404).json({ message: 'Business not found' });

  // Re-index embeddings asynchronously — don't block response
  indexBusinessKnowledge(business._id).catch((err) =>
    console.error('Embedding index error:', err.message)
  );

  res.json({ business, message: 'Business updated. Knowledge base re-indexing in background.' });
};

module.exports = { getBusiness, createBusiness, updateBusiness };
""")

# ── Chat controller ───────────────────────────
write_file(f"{BASE}/controllers/chatController.js", """\
const OpenAI       = require('openai');
const Business     = require('../models/Business');
const ChatSession  = require('../models/ChatSession');
const ChatMessage  = require('../models/ChatMessage');
const { searchSimilar }        = require('../services/embeddingService');
const { buildKnowledgeChunks } = require('../services/knowledgeBaseService');

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// ─────────────────────────────────────────────
// POST /api/chat
//
// Body: { businessId, message, sessionId? }
// Returns: { reply, sessionId }
// ─────────────────────────────────────────────
const chat = async (req, res) => {
  const { businessId, message, sessionId, visitorId } = req.body;

  if (!businessId || !message) {
    return res.status(400).json({ message: 'businessId and message are required' });
  }

  // ── 1. Load business ──────────────────────────
  const business = await Business.findById(businessId);
  if (!business) return res.status(404).json({ message: 'Business not found' });

  // ── 2. Resolve / create session ───────────────
  let session;
  if (sessionId) {
    session = await ChatSession.findById(sessionId);
  }
  if (!session) {
    session = await ChatSession.create({ business: businessId, visitorId: visitorId || null });
  }

  // ── 3. Persist user message ───────────────────
  await ChatMessage.create({ session: session._id, business: businessId, role: 'user', content: message });

  // ── 4. Build knowledge context via cosine similarity ──
  const chunks   = buildKnowledgeChunks(business);
  let context = '';

  if (chunks.length > 0) {
    const relevant = await searchSimilar(message, chunks, 5);
    // Only include chunks with similarity > 0.25
    const filtered = relevant.filter((r) => r.score > 0.25);
    context = filtered.map((r) => r.text).join('\\n\\n');
  }

  // ── 5. Build conversation history (last 10 messages) ──
  const history = await ChatMessage.find({ session: session._id })
    .sort({ createdAt: -1 })
    .limit(10)
    .lean();
  const historyMessages = history
    .reverse()
    .map((m) => ({ role: m.role, content: m.content }));

  // ── 6. Build system prompt ─────────────────────
  const systemPrompt = `You are a helpful customer support assistant for ${business.name}.
${business.description ? `About the business: ${business.description}` : ''}
${context ? `\\nRelevant knowledge:\\n${context}` : ''}

Guidelines:
- Answer only based on the business information provided.
- Be friendly, concise, and professional.
- If you don't know something, say so politely and suggest contacting the business directly.
- Do NOT make up prices, hours, or contact details not provided.`;

  // ── 7. Call GPT-4o ────────────────────────────
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: systemPrompt },
      ...historyMessages,
    ],
    temperature: 0.4,
    max_tokens: 512,
  });

  const reply = completion.choices[0].message.content;

  // ── 8. Persist assistant message ─────────────
  await ChatMessage.create({ session: session._id, business: businessId, role: 'assistant', content: reply });

  // ── 9. Update session metadata ────────────────
  await ChatSession.findByIdAndUpdate(session._id, {
    $inc: { messageCount: 2 },
    lastMessage: message.slice(0, 120),
  });

  res.json({ reply, sessionId: session._id });
};

module.exports = { chat };
""")

# ── Admin controller ──────────────────────────
write_file(f"{BASE}/controllers/adminController.js", """\
const ChatSession  = require('../models/ChatSession');
const ChatMessage  = require('../models/ChatMessage');
const Business     = require('../models/Business');
const { indexBusinessKnowledge } = require('../services/knowledgeBaseService');

// ─────────────────────────────────────────────
// GET /api/admin/chats?page=1&limit=20
// Returns paginated chat sessions for the owner's business
// ─────────────────────────────────────────────
const getChats = async (req, res) => {
  const business = await Business.findOne({ owner: req.user._id }).lean();
  if (!business) return res.status(404).json({ message: 'Business not found' });

  const page  = Math.max(parseInt(req.query.page)  || 1, 1);
  const limit = Math.min(parseInt(req.query.limit) || 20, 100);
  const skip  = (page - 1) * limit;

  const [sessions, total] = await Promise.all([
    ChatSession.find({ business: business._id })
      .sort({ updatedAt: -1 })
      .skip(skip)
      .limit(limit)
      .lean(),
    ChatSession.countDocuments({ business: business._id }),
  ]);

  res.json({
    sessions,
    pagination: { total, page, limit, pages: Math.ceil(total / limit) },
  });
};

// ─────────────────────────────────────────────
// GET /api/admin/chats/:sessionId/messages
// Returns all messages for a specific session
// ─────────────────────────────────────────────
const getSessionMessages = async (req, res) => {
  const business = await Business.findOne({ owner: req.user._id }).lean();
  if (!business) return res.status(404).json({ message: 'Business not found' });

  const session = await ChatSession.findOne({
    _id: req.params.sessionId,
    business: business._id,
  }).lean();
  if (!session) return res.status(404).json({ message: 'Session not found' });

  const messages = await ChatMessage.find({ session: session._id })
    .sort({ createdAt: 1 })
    .lean();

  res.json({ session, messages });
};

// ─────────────────────────────────────────────
// PATCH /api/admin/business
// Partial update (FAQs / info) + trigger re-indexing
// ─────────────────────────────────────────────
const patchBusiness = async (req, res) => {
  const allowedFields = ['name', 'description', 'services', 'faqs', 'hours', 'contact'];
  const updates = {};
  for (const field of allowedFields) {
    if (req.body[field] !== undefined) updates[field] = req.body[field];
  }

  const business = await Business.findOneAndUpdate(
    { owner: req.user._id },
    { $set: updates },
    { new: true, runValidators: true }
  );
  if (!business) return res.status(404).json({ message: 'Business not found' });

  // Re-index embeddings asynchronously
  indexBusinessKnowledge(business._id).catch((err) =>
    console.error('Re-index error:', err.message)
  );

  res.json({ business, message: 'Business updated. Knowledge base re-indexing in background.' });
};

module.exports = { getChats, getSessionMessages, patchBusiness };
""")

# ══════════════════════════════════════════════
# 8. Routes
# ══════════════════════════════════════════════

# ── Auth routes ───────────────────────────────
write_file(f"{BASE}/routes/auth.js", """\
const { Router }    = require('express');
const { body }      = require('express-validator');
const { protect }   = require('../middleware/auth');
const { register, login, getMe } = require('../controllers/authController');
const validate      = require('../middleware/validate');

const router = Router();

router.post(
  '/register',
  [
    body('name').trim().notEmpty().withMessage('Name is required'),
    body('email').isEmail().withMessage('Valid email required'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  ],
  validate,
  register
);

router.post(
  '/login',
  [
    body('email').isEmail().withMessage('Valid email required'),
    body('password').notEmpty().withMessage('Password is required'),
  ],
  validate,
  login
);

router.get('/me', protect, getMe);

module.exports = router;
""")

# ── Business routes ───────────────────────────
write_file(f"{BASE}/routes/business.js", """\
const { Router } = require('express');
const { protect } = require('../middleware/auth');
const { getBusiness, createBusiness, updateBusiness } = require('../controllers/businessController');

const router = Router();

router.use(protect); // all business routes require auth

router.get('/',  getBusiness);
router.post('/', createBusiness);
router.put('/',  updateBusiness);

module.exports = router;
""")

# ── Chat routes ───────────────────────────────
write_file(f"{BASE}/routes/chat.js", """\
const { Router } = require('express');
const { body }   = require('express-validator');
const validate   = require('../middleware/validate');
const { chat }   = require('../controllers/chatController');

const router = Router();

router.post(
  '/',
  [
    body('businessId').notEmpty().withMessage('businessId is required'),
    body('message').trim().notEmpty().withMessage('message is required'),
  ],
  validate,
  chat
);

module.exports = router;
""")

# ── Admin routes ──────────────────────────────
write_file(f"{BASE}/routes/admin.js", """\
const { Router }  = require('express');
const { protect } = require('../middleware/auth');
const { getChats, getSessionMessages, patchBusiness } = require('../controllers/adminController');

const router = Router();

router.use(protect); // all admin routes require auth

router.get('/chats',                     getChats);
router.get('/chats/:sessionId/messages', getSessionMessages);
router.patch('/business',                patchBusiness);

module.exports = router;
""")

# ── Validate middleware ───────────────────────
write_file(f"{BASE}/middleware/validate.js", """\
const { validationResult } = require('express-validator');

/**
 * Express middleware — reads express-validator errors and
 * returns a 422 with a structured errors array when validation fails.
 */
const validate = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(422).json({ errors: errors.array() });
  }
  next();
};

module.exports = validate;
""")

# ══════════════════════════════════════════════
# 9. Print final summary
# ══════════════════════════════════════════════
print()
print("=" * 55)
print("  Backend scaffold written successfully!")
print("=" * 55)
print()
print("  Folder structure:")
print("  backend/")
print("  ├── .env.example")
print("  ├── package.json")
print("  ├── server.js")
print("  ├── middleware/")
print("  │   ├── auth.js")
print("  │   └── validate.js")
print("  ├── models/")
print("  │   ├── User.js")
print("  │   ├── Business.js")
print("  │   ├── ChatSession.js")
print("  │   └── ChatMessage.js")
print("  ├── controllers/")
print("  │   ├── authController.js")
print("  │   ├── businessController.js")
print("  │   ├── chatController.js")
print("  │   └── adminController.js")
print("  ├── routes/")
print("  │   ├── auth.js")
print("  │   ├── business.js")
print("  │   ├── chat.js")
print("  │   └── admin.js")
print("  └── services/")
print("      ├── embeddingService.js")
print("      └── knowledgeBaseService.js")
print()
print("  Next steps:")
print("  1. cp backend/.env.example backend/.env && fill in values")
print("  2. cd backend && npm install")
print("  3. npm run dev")
