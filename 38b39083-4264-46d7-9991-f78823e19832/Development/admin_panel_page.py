
import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════
# AdminPanel.jsx  — tabbed: Chat History | FAQ Editor | Business Info
# ══════════════════════════════════════════════
write_file("frontend/src/pages/AdminPanel.jsx", """\
import { useState, useEffect, useCallback } from 'react';
import { adminApi } from '../services/api';
import Layout from '../components/Layout';
import Spinner from '../components/Spinner';

// ─────────────────────────────────────────────
// Sub-component: Chat History Tab
// ─────────────────────────────────────────────
const ChatHistoryTab = () => {
  const [sessions,    setSessions]    = useState([]);
  const [selected,    setSelected]    = useState(null);
  const [messages,    setMessages]    = useState([]);
  const [pagination,  setPagination]  = useState({ page: 1, pages: 1, total: 0 });
  const [loading,     setLoading]     = useState(true);
  const [msgLoading,  setMsgLoading]  = useState(false);

  const loadSessions = useCallback(async (page = 1) => {
    setLoading(true);
    try {
      const res = await adminApi.getChats({ page, limit: 20 });
      setSessions(res.data.sessions);
      setPagination(res.data.pagination);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadSessions(1); }, [loadSessions]);

  const openSession = async (session) => {
    setSelected(session);
    setMsgLoading(true);
    try {
      const res = await adminApi.getSessionMessages(session._id);
      setMessages(res.data.messages);
    } finally {
      setMsgLoading(false);
    }
  };

  const formatDate = (iso) =>
    new Date(iso).toLocaleString('en-US', {
      month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });

  return (
    <div className="flex gap-6 h-[calc(100vh-220px)] min-h-[480px]">
      {/* Sessions list */}
      <div className="w-80 shrink-0 flex flex-col border border-slate-200 rounded-xl overflow-hidden bg-white">
        <div className="px-4 py-3 border-b border-slate-100 bg-slate-50">
          <h3 className="font-semibold text-sm text-slate-700">
            Chat Sessions
            <span className="ml-2 text-xs text-slate-400 font-normal">
              {pagination.total} total
            </span>
          </h3>
        </div>

        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <Spinner />
          </div>
        ) : sessions.length === 0 ? (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-sm text-slate-400">No chat sessions yet</p>
          </div>
        ) : (
          <div className="flex-1 overflow-y-auto">
            {sessions.map((s) => (
              <button
                key={s._id}
                onClick={() => openSession(s)}
                className={`w-full text-left px-4 py-3 border-b border-slate-100 hover:bg-indigo-50 transition-colors ${
                  selected?._id === s._id ? 'bg-indigo-50 border-l-2 border-l-indigo-500' : ''
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-slate-400 truncate w-32">
                    {s._id.slice(-8)}
                  </span>
                  <span className="text-xs text-slate-400">{s.messageCount} msgs</span>
                </div>
                <p className="text-sm text-slate-600 truncate mt-0.5">{s.lastMessage || '…'}</p>
                <p className="text-xs text-slate-400 mt-0.5">{formatDate(s.updatedAt)}</p>
              </button>
            ))}
          </div>
        )}

        {/* Pagination */}
        {pagination.pages > 1 && (
          <div className="flex justify-between items-center px-4 py-2 border-t border-slate-100 bg-slate-50">
            <button
              disabled={pagination.page <= 1}
              onClick={() => loadSessions(pagination.page - 1)}
              className="text-xs text-indigo-600 disabled:text-slate-300"
            >
              ← Prev
            </button>
            <span className="text-xs text-slate-400">
              {pagination.page} / {pagination.pages}
            </span>
            <button
              disabled={pagination.page >= pagination.pages}
              onClick={() => loadSessions(pagination.page + 1)}
              className="text-xs text-indigo-600 disabled:text-slate-300"
            >
              Next →
            </button>
          </div>
        )}
      </div>

      {/* Message thread */}
      <div className="flex-1 border border-slate-200 rounded-xl overflow-hidden bg-white flex flex-col">
        {!selected ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
            <span className="text-4xl mb-3">💬</span>
            <p className="text-sm">Select a session to view messages</p>
          </div>
        ) : (
          <>
            <div className="px-5 py-3 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
              <div>
                <span className="font-semibold text-sm text-slate-700">Session</span>
                <span className="font-mono text-xs text-slate-400 ml-2">{selected._id}</span>
              </div>
              <span className="text-xs text-slate-400">{formatDate(selected.updatedAt)}</span>
            </div>

            {msgLoading ? (
              <div className="flex-1 flex items-center justify-center">
                <Spinner />
              </div>
            ) : (
              <div className="flex-1 overflow-y-auto chat-scroll p-5 space-y-4">
                {messages.map((m) => (
                  <div
                    key={m._id}
                    className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[75%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
                        m.role === 'user'
                          ? 'bg-indigo-600 text-white rounded-br-sm'
                          : 'bg-slate-100 text-slate-800 rounded-bl-sm'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{m.content}</p>
                      <p className={`text-xs mt-1 ${m.role === 'user' ? 'text-indigo-200' : 'text-slate-400'}`}>
                        {formatDate(m.createdAt)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// Sub-component: FAQ Editor Tab
// ─────────────────────────────────────────────
const blankFaq = () => ({ question: '', answer: '' });

const FaqEditorTab = () => {
  const [faqs,    setFaqs]    = useState([]);
  const [status,  setStatus]  = useState('idle');
  const [message, setMessage] = useState('');

  useEffect(() => {
    adminApi.getChats({ page: 1, limit: 1 })
      .then(() => {}) // auth warm-up
      .catch(() => {});
    // Load FAQs via admin business patch (read via the business endpoint actually)
    import('../services/api').then(({ businessApi }) => {
      businessApi.get()
        .then((res) => {
          const raw = res.data.business.faqs || [];
          setFaqs(raw.length ? raw.map((f) => ({ question: f.question, answer: f.answer })) : [blankFaq()]);
        })
        .catch(() => setFaqs([blankFaq()]));
    });
  }, []);

  const updateFaq  = (idx, key, val) =>
    setFaqs((prev) => prev.map((f, i) => i === idx ? { ...f, [key]: val } : f));
  const addFaq     = () => setFaqs((prev) => [...prev, blankFaq()]);
  const removeFaq  = (idx) => setFaqs((prev) => prev.filter((_, i) => i !== idx));

  const handleSave = async () => {
    setStatus('saving');
    setMessage('');
    try {
      await adminApi.patchBusiness({ faqs });
      setStatus('saved');
      setMessage('FAQs updated! Knowledge base re-indexing…');
      setTimeout(() => setStatus('idle'), 4000);
    } catch (err) {
      setStatus('error');
      setMessage(err.message);
    }
  };

  return (
    <div className="max-w-2xl space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-slate-800">FAQ Editor</h3>
          <p className="text-sm text-slate-500 mt-0.5">Edit the FAQs your chatbot uses to answer questions.</p>
        </div>
        <button
          onClick={handleSave}
          disabled={status === 'saving'}
          className="btn-primary"
        >
          {status === 'saving' ? <Spinner size="sm" className="mx-auto" /> : 'Save FAQs'}
        </button>
      </div>

      {message && (
        <div className={`rounded-lg px-4 py-3 text-sm border ${
          status === 'saved'
            ? 'bg-green-50 border-green-200 text-green-700'
            : 'bg-red-50 border-red-200 text-red-700'
        }`}>
          {message}
        </div>
      )}

      {faqs.map((faq, idx) => (
        <div key={idx} className="p-4 bg-white border border-slate-200 rounded-xl space-y-3 shadow-sm">
          <div className="flex justify-between items-center">
            <span className="text-xs font-medium text-slate-400">FAQ #{idx + 1}</span>
            {faqs.length > 1 && (
              <button
                onClick={() => removeFaq(idx)}
                className="text-xs text-red-400 hover:text-red-600 transition-colors"
              >
                Remove
              </button>
            )}
          </div>
          <div>
            <label className="label">Question</label>
            <input
              className="input-field"
              value={faq.question}
              onChange={(e) => updateFaq(idx, 'question', e.target.value)}
              placeholder="Customer question…"
            />
          </div>
          <div>
            <label className="label">Answer</label>
            <textarea
              className="input-field resize-none"
              rows={3}
              value={faq.answer}
              onChange={(e) => updateFaq(idx, 'answer', e.target.value)}
              placeholder="Your answer…"
            />
          </div>
        </div>
      ))}

      <button onClick={addFaq} className="btn-secondary text-xs">
        + Add FAQ
      </button>
    </div>
  );
};

// ─────────────────────────────────────────────
// Sub-component: Business Info Editor Tab
// ─────────────────────────────────────────────
const BusinessInfoTab = () => {
  const [info,    setInfo]    = useState({ name: '', description: '', contact: {} });
  const [status,  setStatus]  = useState('idle');
  const [message, setMessage] = useState('');

  useEffect(() => {
    import('../services/api').then(({ businessApi }) => {
      businessApi.get()
        .then((res) => {
          const b = res.data.business;
          setInfo({
            name:        b.name        || '',
            description: b.description || '',
            contact:     b.contact     || {},
          });
        })
        .catch(() => {});
    });
  }, []);

  const handleSave = async () => {
    setStatus('saving');
    setMessage('');
    try {
      await adminApi.patchBusiness(info);
      setStatus('saved');
      setMessage('Business info updated!');
      setTimeout(() => setStatus('idle'), 4000);
    } catch (err) {
      setStatus('error');
      setMessage(err.message);
    }
  };

  const setContact = (key, val) =>
    setInfo((prev) => ({ ...prev, contact: { ...prev.contact, [key]: val } }));

  return (
    <div className="max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-slate-800">Business Info Editor</h3>
          <p className="text-sm text-slate-500 mt-0.5">Quick-edit core details without leaving the Admin Panel.</p>
        </div>
        <button onClick={handleSave} disabled={status === 'saving'} className="btn-primary">
          {status === 'saving' ? <Spinner size="sm" className="mx-auto" /> : 'Save Changes'}
        </button>
      </div>

      {message && (
        <div className={`rounded-lg px-4 py-3 text-sm border ${
          status === 'saved'
            ? 'bg-green-50 border-green-200 text-green-700'
            : 'bg-red-50 border-red-200 text-red-700'
        }`}>
          {message}
        </div>
      )}

      <div className="card space-y-4">
        <div>
          <label className="label">Business Name</label>
          <input
            className="input-field"
            value={info.name}
            onChange={(e) => setInfo((p) => ({ ...p, name: e.target.value }))}
            placeholder="Acme Corp"
          />
        </div>
        <div>
          <label className="label">Description</label>
          <textarea
            className="input-field resize-none"
            rows={4}
            value={info.description}
            onChange={(e) => setInfo((p) => ({ ...p, description: e.target.value }))}
            placeholder="What does your business do?"
          />
        </div>
      </div>

      <div className="card space-y-4">
        <h4 className="text-sm font-semibold text-slate-700 border-b border-slate-100 pb-2">Contact</h4>
        {[
          ['email',   'Email'],
          ['phone',   'Phone'],
          ['website', 'Website'],
          ['address', 'Address'],
        ].map(([key, label]) => (
          <div key={key}>
            <label className="label">{label}</label>
            <input
              className="input-field"
              value={info.contact[key] || ''}
              onChange={(e) => setContact(key, e.target.value)}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// Main AdminPanel page
// ─────────────────────────────────────────────
const TABS = [
  { id: 'chats',    label: '💬 Chat History' },
  { id: 'faqs',     label: '❓ FAQ Editor' },
  { id: 'bizinfo',  label: '🏢 Business Info' },
];

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('chats');

  return (
    <Layout>
      <div>
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-900">Admin Panel</h1>
          <p className="text-slate-500 text-sm mt-1">
            Manage chat history, FAQs, and business info.
          </p>
        </div>

        {/* Tab bar */}
        <div className="flex gap-1 border-b border-slate-200 mb-6">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2.5 text-sm font-medium rounded-t-lg transition-colors ${
                activeTab === tab.id
                  ? 'text-indigo-700 border-b-2 border-indigo-600 bg-indigo-50/60'
                  : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {activeTab === 'chats'   && <ChatHistoryTab />}
        {activeTab === 'faqs'    && <FaqEditorTab />}
        {activeTab === 'bizinfo' && <BusinessInfoTab />}
      </div>
    </Layout>
  );
};

export default AdminPanel;
""")

print("✅  AdminPanel.jsx written (Chat History | FAQ Editor | Business Info tabs)")
