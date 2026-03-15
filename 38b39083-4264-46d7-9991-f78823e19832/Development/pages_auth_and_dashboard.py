
import os

BASE = "frontend/src/pages"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════
# Login.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/Login.jsx", """\
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/Spinner';

const Login = () => {
  const { login } = useAuth();
  const navigate  = useNavigate();

  const [form,    setForm]    = useState({ email: '', password: '' });
  const [error,   setError]   = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <span className="text-4xl">💬</span>
          <h1 className="mt-3 text-2xl font-bold text-slate-900">Welcome back</h1>
          <p className="text-slate-500 text-sm mt-1">Sign in to your BizChat AI account</p>
        </div>

        {/* Card */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="email" className="label">Email address</label>
              <input
                id="email" name="email" type="email"
                value={form.email} onChange={handleChange}
                className="input-field" placeholder="you@company.com"
                required autoFocus
              />
            </div>

            <div>
              <label htmlFor="password" className="label">Password</label>
              <input
                id="password" name="password" type="password"
                value={form.password} onChange={handleChange}
                className="input-field" placeholder="••••••••"
                required
              />
            </div>

            <button type="submit" className="btn-primary w-full py-2.5" disabled={loading}>
              {loading ? <Spinner size="sm" className="mx-auto" /> : 'Sign in'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-indigo-600 font-medium hover:underline">
              Create one free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
""")

# ══════════════════════════════════════════════
# Register.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/Register.jsx", """\
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Spinner from '../components/Spinner';

const Register = () => {
  const { register } = useAuth();
  const navigate     = useNavigate();

  const [form,    setForm]    = useState({ name: '', email: '', password: '', confirm: '' });
  const [error,   setError]   = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.confirm) {
      setError('Passwords do not match');
      return;
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }
    setLoading(true);
    try {
      await register(form.name, form.email, form.password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <span className="text-4xl">💬</span>
          <h1 className="mt-3 text-2xl font-bold text-slate-900">Create your account</h1>
          <p className="text-slate-500 text-sm mt-1">Set up BizChat AI for your business in minutes</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="reg-name" className="label">Full name</label>
              <input
                id="reg-name" name="name" type="text"
                value={form.name} onChange={handleChange}
                className="input-field" placeholder="Jane Smith"
                required autoFocus
              />
            </div>

            <div>
              <label htmlFor="reg-email" className="label">Email address</label>
              <input
                id="reg-email" name="email" type="email"
                value={form.email} onChange={handleChange}
                className="input-field" placeholder="you@company.com"
                required
              />
            </div>

            <div>
              <label htmlFor="reg-password" className="label">Password</label>
              <input
                id="reg-password" name="password" type="password"
                value={form.password} onChange={handleChange}
                className="input-field" placeholder="At least 6 characters"
                required
              />
            </div>

            <div>
              <label htmlFor="reg-confirm" className="label">Confirm password</label>
              <input
                id="reg-confirm" name="confirm" type="password"
                value={form.confirm} onChange={handleChange}
                className="input-field" placeholder="••••••••"
                required
              />
            </div>

            <button type="submit" className="btn-primary w-full py-2.5 mt-2" disabled={loading}>
              {loading ? <Spinner size="sm" className="mx-auto" /> : 'Create account'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-indigo-600 font-medium hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
""")

# ══════════════════════════════════════════════
# Dashboard.jsx  — business info form
# ══════════════════════════════════════════════
write_file(f"{BASE}/Dashboard.jsx", """\
import { useState, useEffect } from 'react';
import { businessApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import Layout from '../components/Layout';
import Spinner from '../components/Spinner';

// ── Days of week for working hours ─────────────
const DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];

// ── Blank hour entry ───────────────────────────
const blankHour = (day) => ({ day, open: '09:00', close: '17:00', closed: false });

// ── Blank service entry ────────────────────────
const blankService = () => ({ name: '', description: '', price: '' });

// ── Blank FAQ entry ────────────────────────────
const blankFaq = () => ({ question: '', answer: '' });

const Dashboard = () => {
  const { businessId } = useAuth();

  const [form, setForm] = useState({
    name:        '',
    description: '',
    services:    [blankService()],
    faqs:        [blankFaq()],
    hours:       DAYS.map(blankHour),
    contact:     { email: '', phone: '', address: '', website: '' },
  });

  const [status,  setStatus]  = useState('idle');   // idle | loading | saving | saved | error
  const [message, setMessage] = useState('');

  // ── Load existing business data ───────────────
  useEffect(() => {
    setStatus('loading');
    businessApi.get()
      .then((res) => {
        const b = res.data.business;
        setForm({
          name:        b.name        || '',
          description: b.description || '',
          services:    b.services?.length  ? b.services  : [blankService()],
          faqs:        b.faqs?.length      ? b.faqs      : [blankFaq()],
          hours:       b.hours?.length     ? b.hours     : DAYS.map(blankHour),
          contact:     b.contact || { email: '', phone: '', address: '', website: '' },
        });
        setStatus('idle');
      })
      .catch(() => setStatus('idle'));
  }, [businessId]);

  // ── Generic field updater ─────────────────────
  const setField = (field, value) => setForm((f) => ({ ...f, [field]: value }));

  // ── Services helpers ──────────────────────────
  const updateService = (idx, key, val) => {
    const updated = form.services.map((s, i) => i === idx ? { ...s, [key]: val } : s);
    setField('services', updated);
  };
  const addService    = () => setField('services', [...form.services, blankService()]);
  const removeService = (idx) => setField('services', form.services.filter((_, i) => i !== idx));

  // ── FAQ helpers ───────────────────────────────
  const updateFaq = (idx, key, val) => {
    const updated = form.faqs.map((f, i) => i === idx ? { ...f, [key]: val } : f);
    setField('faqs', updated);
  };
  const addFaq    = () => setField('faqs', [...form.faqs, blankFaq()]);
  const removeFaq = (idx) => setField('faqs', form.faqs.filter((_, i) => i !== idx));

  // ── Hours helpers ─────────────────────────────
  const updateHour = (idx, key, val) => {
    const updated = form.hours.map((h, i) => i === idx ? { ...h, [key]: val } : h);
    setField('hours', updated);
  };

  // ── Contact helper ────────────────────────────
  const updateContact = (key, val) =>
    setForm((f) => ({ ...f, contact: { ...f.contact, [key]: val } }));

  // ── Submit ────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('saving');
    setMessage('');
    try {
      await businessApi.update(form);
      setStatus('saved');
      setMessage('Business info saved! Knowledge base is re-indexing in the background.');
      setTimeout(() => setStatus('idle'), 4000);
    } catch (err) {
      setStatus('error');
      setMessage(err.message);
    }
  };

  if (status === 'loading') {
    return (
      <Layout>
        <div className="flex items-center justify-center py-24">
          <Spinner size="lg" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-slate-900">Business Dashboard</h1>
          <p className="text-slate-500 text-sm mt-1">
            Keep your info up-to-date — it powers your AI chat widget.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">

          {/* ── Basic Info ─────────────────────── */}
          <div className="card space-y-5">
            <h2 className="text-base font-semibold text-slate-800 border-b border-slate-100 pb-3">
              Basic Information
            </h2>

            <div>
              <label className="label">Business Name *</label>
              <input
                className="input-field"
                value={form.name}
                onChange={(e) => setField('name', e.target.value)}
                placeholder="Acme Corp"
                required
              />
            </div>

            <div>
              <label className="label">Description</label>
              <textarea
                className="input-field resize-none"
                rows={3}
                value={form.description}
                onChange={(e) => setField('description', e.target.value)}
                placeholder="Brief description of what your business does…"
              />
            </div>
          </div>

          {/* ── Contact Info ───────────────────── */}
          <div className="card space-y-5">
            <h2 className="text-base font-semibold text-slate-800 border-b border-slate-100 pb-3">
              Contact Information
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                ['email',   'Email',   'support@company.com', 'email'],
                ['phone',   'Phone',   '+1 (555) 000-0000',   'tel'],
                ['website', 'Website', 'https://company.com', 'url'],
                ['address', 'Address', '123 Main St, City',   'text'],
              ].map(([key, label, placeholder, type]) => (
                <div key={key} className={key === 'address' ? 'sm:col-span-2' : ''}>
                  <label className="label">{label}</label>
                  <input
                    type={type}
                    className="input-field"
                    value={form.contact[key] || ''}
                    onChange={(e) => updateContact(key, e.target.value)}
                    placeholder={placeholder}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* ── Services ───────────────────────── */}
          <div className="card space-y-4">
            <h2 className="text-base font-semibold text-slate-800 border-b border-slate-100 pb-3">
              Services
            </h2>
            {form.services.map((svc, idx) => (
              <div key={idx} className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-4 bg-slate-50 rounded-lg border border-slate-200">
                <div>
                  <label className="label">Name</label>
                  <input
                    className="input-field"
                    value={svc.name}
                    onChange={(e) => updateService(idx, 'name', e.target.value)}
                    placeholder="Service name"
                  />
                </div>
                <div>
                  <label className="label">Description</label>
                  <input
                    className="input-field"
                    value={svc.description || ''}
                    onChange={(e) => updateService(idx, 'description', e.target.value)}
                    placeholder="What it includes"
                  />
                </div>
                <div className="flex gap-2">
                  <div className="flex-1">
                    <label className="label">Price</label>
                    <input
                      className="input-field"
                      value={svc.price || ''}
                      onChange={(e) => updateService(idx, 'price', e.target.value)}
                      placeholder="$99 / month"
                    />
                  </div>
                  {form.services.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeService(idx)}
                      className="self-end mb-px text-red-400 hover:text-red-600 transition-colors"
                      title="Remove"
                    >
                      ✕
                    </button>
                  )}
                </div>
              </div>
            ))}
            <button type="button" onClick={addService} className="btn-secondary text-xs">
              + Add Service
            </button>
          </div>

          {/* ── FAQs ───────────────────────────── */}
          <div className="card space-y-4">
            <h2 className="text-base font-semibold text-slate-800 border-b border-slate-100 pb-3">
              FAQs
            </h2>
            {form.faqs.map((faq, idx) => (
              <div key={idx} className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-3">
                <div className="flex justify-between items-start">
                  <span className="text-xs text-slate-400 font-medium">FAQ #{idx + 1}</span>
                  {form.faqs.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeFaq(idx)}
                      className="text-red-400 hover:text-red-600 text-sm transition-colors"
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
                    placeholder="What are your refund policies?"
                  />
                </div>
                <div>
                  <label className="label">Answer</label>
                  <textarea
                    className="input-field resize-none"
                    rows={2}
                    value={faq.answer}
                    onChange={(e) => updateFaq(idx, 'answer', e.target.value)}
                    placeholder="We offer a 30-day money-back guarantee…"
                  />
                </div>
              </div>
            ))}
            <button type="button" onClick={addFaq} className="btn-secondary text-xs">
              + Add FAQ
            </button>
          </div>

          {/* ── Working Hours ───────────────────── */}
          <div className="card space-y-3">
            <h2 className="text-base font-semibold text-slate-800 border-b border-slate-100 pb-3">
              Working Hours
            </h2>
            {form.hours.map((h, idx) => (
              <div key={h.day} className="flex items-center gap-3 py-1">
                <span className="w-24 text-sm text-slate-600 font-medium">{h.day}</span>
                <label className="flex items-center gap-1.5 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={h.closed}
                    onChange={(e) => updateHour(idx, 'closed', e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span className="text-xs text-slate-500">Closed</span>
                </label>
                {!h.closed && (
                  <>
                    <input
                      type="time"
                      className="input-field w-32 text-xs"
                      value={h.open}
                      onChange={(e) => updateHour(idx, 'open', e.target.value)}
                    />
                    <span className="text-slate-400 text-sm">–</span>
                    <input
                      type="time"
                      className="input-field w-32 text-xs"
                      value={h.close}
                      onChange={(e) => updateHour(idx, 'close', e.target.value)}
                    />
                  </>
                )}
              </div>
            ))}
          </div>

          {/* ── Status bar & Submit ─────────────── */}
          {message && (
            <div className={`rounded-lg px-4 py-3 text-sm border ${
              status === 'saved'
                ? 'bg-green-50 border-green-200 text-green-700'
                : 'bg-red-50 border-red-200 text-red-700'
            }`}>
              {message}
            </div>
          )}

          <div className="flex justify-end pb-8">
            <button type="submit" className="btn-primary px-6 py-2.5" disabled={status === 'saving'}>
              {status === 'saving' ? (
                <span className="flex items-center gap-2">
                  <Spinner size="sm" /> Saving…
                </span>
              ) : (
                'Save & Update Widget'
              )}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default Dashboard;
""")

print("✅  Login, Register, Dashboard pages written")
