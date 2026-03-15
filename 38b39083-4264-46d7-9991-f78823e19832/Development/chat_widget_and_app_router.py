
import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════
# ChatWidget.jsx  — embeddable React component
# ══════════════════════════════════════════════
write_file("frontend/src/components/ChatWidget.jsx", """\
/**
 * ChatWidget.jsx
 *
 * Embeddable AI chat bubble component.
 *
 * Props:
 *   businessId  {string}  required  — MongoDB ObjectId of the business
 *   apiBase     {string}  optional  — API base URL (default: '/api')
 *   title       {string}  optional  — Widget header title
 *   greeting    {string}  optional  — First bot message
 *   primaryColor {string} optional  — CSS hex for bubble/send button
 */
import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const DEFAULT_GREETING = "👋 Hi there! How can I help you today?";

const ChatWidget = ({
  businessId,
  apiBase     = '/api',
  title       = 'Chat with us',
  greeting    = DEFAULT_GREETING,
  primaryColor = '#4f46e5',
}) => {
  const [open,      setOpen]      = useState(false);
  const [messages,  setMessages]  = useState([
    { role: 'assistant', content: greeting, id: 'greeting' },
  ]);
  const [input,     setInput]     = useState('');
  const [typing,    setTyping]    = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [unread,    setUnread]    = useState(0);

  const bottomRef = useRef(null);
  const inputRef  = useRef(null);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  // Focus input when widget opens
  useEffect(() => {
    if (open) {
      setUnread(0);
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [open]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || typing) return;

    const userMsg = { role: 'user', content: text, id: Date.now().toString() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setTyping(true);

    try {
      const res = await axios.post(`${apiBase}/chat`, {
        businessId,
        message: text,
        sessionId: sessionId || undefined,
      });
      const { reply, sessionId: sid } = res.data;
      if (sid) setSessionId(sid);

      const botMsg = { role: 'assistant', content: reply, id: `bot-${Date.now()}` };
      setMessages((prev) => [...prev, botMsg]);
      if (!open) setUnread((n) => n + 1);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: "Sorry, I couldn't process that. Please try again.",
          id: `err-${Date.now()}`,
        },
      ]);
    } finally {
      setTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const bubbleStyle = { backgroundColor: primaryColor };

  return (
    <div style={{ fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999 }}>
      {/* ── Chat window ─────────────────────── */}
      {open && (
        <div style={{
          position: 'absolute', bottom: '72px', right: '0',
          width: '360px', maxHeight: '520px',
          backgroundColor: '#fff',
          borderRadius: '16px',
          boxShadow: '0 20px 60px rgba(0,0,0,0.18)',
          display: 'flex', flexDirection: 'column',
          overflow: 'hidden',
          border: '1px solid rgba(0,0,0,0.08)',
        }}>
          {/* Header */}
          <div style={{
            ...bubbleStyle,
            padding: '14px 16px',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{
                width: '32px', height: '32px', borderRadius: '50%',
                backgroundColor: 'rgba(255,255,255,0.25)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '16px',
              }}>💬</div>
              <div>
                <p style={{ margin: 0, color: '#fff', fontWeight: 600, fontSize: '14px' }}>{title}</p>
                <p style={{ margin: 0, color: 'rgba(255,255,255,0.75)', fontSize: '11px' }}>
                  <span style={{
                    display: 'inline-block', width: '6px', height: '6px',
                    borderRadius: '50%', backgroundColor: '#4ade80',
                    marginRight: '4px', verticalAlign: 'middle',
                  }} />
                  Online
                </p>
              </div>
            </div>
            <button
              onClick={() => setOpen(false)}
              style={{
                background: 'rgba(255,255,255,0.2)', border: 'none', cursor: 'pointer',
                borderRadius: '50%', width: '28px', height: '28px',
                color: '#fff', fontSize: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div style={{
            flex: 1, overflowY: 'auto', padding: '16px',
            display: 'flex', flexDirection: 'column', gap: '12px',
            scrollbarWidth: 'thin',
          }}>
            {messages.map((m) => (
              <div key={m.id} style={{
                display: 'flex',
                justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start',
              }}>
                <div style={{
                  maxWidth: '78%',
                  padding: '10px 14px',
                  borderRadius: m.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                  backgroundColor: m.role === 'user' ? primaryColor : '#f1f5f9',
                  color: m.role === 'user' ? '#fff' : '#1e293b',
                  fontSize: '14px',
                  lineHeight: '1.5',
                  wordBreak: 'break-word',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.06)',
                }}>
                  {m.content}
                </div>
              </div>
            ))}

            {/* Typing indicator */}
            {typing && (
              <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                <div style={{
                  padding: '10px 16px',
                  backgroundColor: '#f1f5f9',
                  borderRadius: '18px 18px 18px 4px',
                  display: 'flex', alignItems: 'center', gap: '4px',
                }}>
                  {[0, 1, 2].map((i) => (
                    <span key={i} style={{
                      display: 'inline-block', width: '6px', height: '6px',
                      borderRadius: '50%', backgroundColor: '#94a3b8',
                      animation: `bizchat-bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
                    }} />
                  ))}
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input area */}
          <div style={{
            padding: '12px',
            borderTop: '1px solid #e2e8f0',
            backgroundColor: '#fff',
            display: 'flex', gap: '8px', alignItems: 'flex-end',
          }}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a message…"
              rows={1}
              style={{
                flex: 1,
                resize: 'none',
                border: '1px solid #e2e8f0',
                borderRadius: '12px',
                padding: '10px 14px',
                fontSize: '14px',
                fontFamily: 'inherit',
                outline: 'none',
                lineHeight: '1.4',
                maxHeight: '100px',
                overflowY: 'auto',
                color: '#1e293b',
                backgroundColor: '#f8fafc',
              }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || typing}
              style={{
                ...bubbleStyle,
                border: 'none', cursor: input.trim() && !typing ? 'pointer' : 'default',
                borderRadius: '12px', padding: '10px 14px',
                color: '#fff', fontSize: '14px', fontWeight: 600,
                opacity: !input.trim() || typing ? 0.5 : 1,
                transition: 'opacity .15s',
                flexShrink: 0,
              }}
              aria-label="Send message"
            >
              ➤
            </button>
          </div>
        </div>
      )}

      {/* ── Floating bubble button ───────────── */}
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          ...bubbleStyle,
          width: '56px', height: '56px',
          borderRadius: '50%',
          border: 'none',
          cursor: 'pointer',
          boxShadow: '0 8px 24px rgba(0,0,0,0.2)',
          fontSize: '24px',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          transition: 'transform .2s, box-shadow .2s',
          position: 'relative',
        }}
        onMouseEnter={(e) => { e.currentTarget.style.transform = 'scale(1.08)'; }}
        onMouseLeave={(e) => { e.currentTarget.style.transform = 'scale(1)'; }}
        aria-label={open ? 'Close chat' : 'Open chat'}
      >
        {open ? '×' : '💬'}
        {!open && unread > 0 && (
          <span style={{
            position: 'absolute', top: '0', right: '0',
            backgroundColor: '#ef4444',
            color: '#fff', fontSize: '10px', fontWeight: 700,
            width: '18px', height: '18px', borderRadius: '50%',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            border: '2px solid #fff',
          }}>
            {unread}
          </span>
        )}
      </button>

      {/* Typing animation keyframes injected once */}
      <style>{`
        @keyframes bizchat-bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
          40%            { transform: translateY(-5px); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default ChatWidget;
""")

# ══════════════════════════════════════════════
# public/widget.js  — standalone embeddable snippet
# Business owners add: <script src="..." data-business-id="..."></script>
# ══════════════════════════════════════════════
write_file("frontend/public/widget.js", """\
/**
 * BizChat AI — Embeddable Chat Widget
 *
 * Usage:
 *   <script
 *     src="https://your-domain.com/widget.js"
 *     data-business-id="YOUR_BUSINESS_ID"
 *     data-api-base="https://your-api.com/api"
 *     data-title="Chat with us"
 *     data-primary-color="#4f46e5"
 *   ></script>
 *
 * This self-contained script injects React + ReactDOM + the widget
 * into the host page without any bundler or build step required.
 */
(function () {
  'use strict';

  // ── Read config from script tag attributes ──────────────────────────────────
  const scriptEl      = document.currentScript;
  const businessId    = scriptEl.getAttribute('data-business-id')    || '';
  const apiBase       = scriptEl.getAttribute('data-api-base')       || 'https://your-api.com/api';
  const title         = scriptEl.getAttribute('data-title')          || 'Chat with us';
  const primaryColor  = scriptEl.getAttribute('data-primary-color')  || '#4f46e5';
  const greeting      = scriptEl.getAttribute('data-greeting')       || '👋 Hi there! How can I help you today?';

  if (!businessId) {
    console.warn('[BizChat] Missing data-business-id attribute — widget will not load.');
    return;
  }

  // ── Inject React + ReactDOM from CDN ────────────────────────────────────────
  function loadScript(src, onload) {
    const s    = document.createElement('script');
    s.src      = src;
    s.onload   = onload;
    s.crossOrigin = 'anonymous';
    document.head.appendChild(s);
  }

  function mountWidget() {
    const { React, ReactDOM } = window;

    // ── Inline widget component (no Tailwind, pure inline styles) ──────────────
    const e = React.createElement;

    function ChatWidget() {
      const [open,      setOpen]      = React.useState(false);
      const [messages,  setMessages]  = React.useState([
        { role: 'assistant', content: greeting, id: 'greeting' },
      ]);
      const [input,     setInput]     = React.useState('');
      const [typing,    setTyping]    = React.useState(false);
      const [sessionId, setSessionId] = React.useState(null);
      const [unread,    setUnread]    = React.useState(0);
      const bottomRef = React.useRef(null);
      const inputRef  = React.useRef(null);

      React.useEffect(() => {
        bottomRef.current && bottomRef.current.scrollIntoView({ behavior: 'smooth' });
      }, [messages, typing]);

      React.useEffect(() => {
        if (open) {
          setUnread(0);
          setTimeout(() => inputRef.current && inputRef.current.focus(), 150);
        }
      }, [open]);

      const sendMessage = async () => {
        const text = input.trim();
        if (!text || typing) return;
        const userMsg = { role: 'user', content: text, id: String(Date.now()) };
        setMessages((p) => [...p, userMsg]);
        setInput('');
        setTyping(true);
        try {
          const res = await fetch(apiBase + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ businessId, message: text, sessionId: sessionId || undefined }),
          });
          const data = await res.json();
          if (data.sessionId) setSessionId(data.sessionId);
          setMessages((p) => [...p, { role: 'assistant', content: data.reply, id: 'bot-' + Date.now() }]);
          if (!open) setUnread((n) => n + 1);
        } catch {
          setMessages((p) => [...p, {
            role: 'assistant',
            content: "Sorry, I couldn't process that. Please try again.",
            id: 'err-' + Date.now(),
          }]);
        } finally {
          setTyping(false);
        }
      };

      const handleKey = (ev) => {
        if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); sendMessage(); }
      };

      const bubble = { backgroundColor: primaryColor };

      const msgBubble = (m) => e('div', {
        key: m.id,
        style: { display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' },
      }, e('div', {
        style: {
          maxWidth: '78%', padding: '10px 14px', wordBreak: 'break-word',
          borderRadius: m.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
          backgroundColor: m.role === 'user' ? primaryColor : '#f1f5f9',
          color: m.role === 'user' ? '#fff' : '#1e293b',
          fontSize: '14px', lineHeight: '1.5',
          boxShadow: '0 1px 2px rgba(0,0,0,0.06)',
        },
      }, m.content));

      const typingDots = e('div', { style: { display: 'flex', justifyContent: 'flex-start' } },
        e('div', {
          style: {
            padding: '10px 16px', backgroundColor: '#f1f5f9',
            borderRadius: '18px 18px 18px 4px',
            display: 'flex', alignItems: 'center', gap: '4px',
          },
        }, [0, 1, 2].map((i) => e('span', {
          key: i,
          style: {
            display: 'inline-block', width: '6px', height: '6px',
            borderRadius: '50%', backgroundColor: '#94a3b8',
            animation: `bizchat-bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
          },
        })))
      );

      return e('div', {
        style: {
          fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
          position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999,
        },
      },
        // Chat window
        open && e('div', {
          style: {
            position: 'absolute', bottom: '72px', right: '0',
            width: '360px', maxHeight: '520px', backgroundColor: '#fff',
            borderRadius: '16px', boxShadow: '0 20px 60px rgba(0,0,0,0.18)',
            display: 'flex', flexDirection: 'column', overflow: 'hidden',
            border: '1px solid rgba(0,0,0,0.08)',
          },
        },
          // Header
          e('div', { style: { ...bubble, padding: '14px 16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' } },
            e('div', { style: { display: 'flex', alignItems: 'center', gap: '10px' } },
              e('div', { style: { width: '32px', height: '32px', borderRadius: '50%', backgroundColor: 'rgba(255,255,255,0.25)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '16px' } }, '💬'),
              e('div', null,
                e('p', { style: { margin: 0, color: '#fff', fontWeight: 600, fontSize: '14px' } }, title),
                e('p', { style: { margin: 0, color: 'rgba(255,255,255,0.75)', fontSize: '11px' } },
                  e('span', { style: { display: 'inline-block', width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#4ade80', marginRight: '4px', verticalAlign: 'middle' } }),
                  'Online'
                )
              )
            ),
            e('button', {
              onClick: () => setOpen(false),
              style: { background: 'rgba(255,255,255,0.2)', border: 'none', cursor: 'pointer', borderRadius: '50%', width: '28px', height: '28px', color: '#fff', fontSize: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center' },
            }, '×')
          ),
          // Messages
          e('div', {
            style: { flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' },
          },
            ...messages.map(msgBubble),
            typing && typingDots,
            e('div', { ref: bottomRef })
          ),
          // Input
          e('div', {
            style: { padding: '12px', borderTop: '1px solid #e2e8f0', backgroundColor: '#fff', display: 'flex', gap: '8px', alignItems: 'flex-end' },
          },
            e('textarea', {
              ref: inputRef,
              value: input,
              onChange: (ev) => setInput(ev.target.value),
              onKeyDown: handleKey,
              placeholder: 'Type a message…',
              rows: 1,
              style: { flex: 1, resize: 'none', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '10px 14px', fontSize: '14px', fontFamily: 'inherit', outline: 'none', lineHeight: '1.4', maxHeight: '100px', overflowY: 'auto', color: '#1e293b', backgroundColor: '#f8fafc' },
            }),
            e('button', {
              onClick: sendMessage,
              disabled: !input.trim() || typing,
              style: { ...bubble, border: 'none', cursor: input.trim() && !typing ? 'pointer' : 'default', borderRadius: '12px', padding: '10px 14px', color: '#fff', fontSize: '14px', fontWeight: 600, opacity: !input.trim() || typing ? 0.5 : 1 },
            }, '➤')
          )
        ),

        // Bubble button
        e('button', {
          onClick: () => setOpen((o) => !o),
          style: { ...bubble, width: '56px', height: '56px', borderRadius: '50%', border: 'none', cursor: 'pointer', boxShadow: '0 8px 24px rgba(0,0,0,0.2)', fontSize: '24px', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' },
        },
          open ? '×' : '💬',
          !open && unread > 0 && e('span', {
            style: { position: 'absolute', top: '0', right: '0', backgroundColor: '#ef4444', color: '#fff', fontSize: '10px', fontWeight: 700, width: '18px', height: '18px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '2px solid #fff' },
          }, unread)
        ),

        // Keyframes
        e('style', null, '@keyframes bizchat-bounce { 0%,80%,100%{transform:translateY(0);opacity:.5} 40%{transform:translateY(-5px);opacity:1} }')
      );
    }

    // Mount into a new container
    const container = document.createElement('div');
    container.id = 'bizchat-widget-root';
    document.body.appendChild(container);
    ReactDOM.createRoot(container).render(e(ChatWidget));
  }

  // Load React 18 from esm.sh CDN then mount
  if (window.React && window.ReactDOM) {
    mountWidget();
  } else {
    loadScript('https://esm.sh/react@18?dev', () =>
      loadScript('https://esm.sh/react-dom@18/client?dev', mountWidget)
    );
  }
})();
""")

# ══════════════════════════════════════════════
# App.jsx  — React Router wiring
# ══════════════════════════════════════════════
write_file("frontend/src/App.jsx", """\
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import Login      from './pages/Login';
import Register   from './pages/Register';
import Dashboard  from './pages/Dashboard';
import AdminPanel from './pages/AdminPanel';

const App = () => (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login"    element={<Login />}    />
        <Route path="/register" element={<Register />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute>
              <AdminPanel />
            </ProtectedRoute>
          }
        />

        {/* Default redirect */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  </AuthProvider>
);

export default App;
""")

print("✅  ChatWidget.jsx written")
print("✅  public/widget.js written (standalone embed snippet)")
print("✅  App.jsx written (React Router — Login | Register | Dashboard | AdminPanel)")
