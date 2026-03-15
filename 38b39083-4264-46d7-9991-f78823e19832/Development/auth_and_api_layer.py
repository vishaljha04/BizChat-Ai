
import os

BASE = "frontend/src"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════
# services/api.js  — axios service layer
# ══════════════════════════════════════════════
write_file(f"{BASE}/services/api.js", """\
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
});

// ── Request interceptor: attach JWT ─────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('bizchat_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Response interceptor: surface error messages ─
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.message ||
      err.response?.data?.errors?.[0]?.msg ||
      err.message ||
      'Something went wrong';
    return Promise.reject(new Error(message));
  }
);

// ────────────────────────────────────────────────
// Auth endpoints
// ────────────────────────────────────────────────
export const authApi = {
  register: (data)  => api.post('/auth/register', data),
  login:    (data)  => api.post('/auth/login', data),
  getMe:    ()      => api.get('/auth/me'),
};

// ────────────────────────────────────────────────
// Business endpoints
// ────────────────────────────────────────────────
export const businessApi = {
  get:    ()     => api.get('/business'),
  create: (data) => api.post('/business', data),
  update: (data) => api.put('/business', data),
};

// ────────────────────────────────────────────────
// Admin endpoints
// ────────────────────────────────────────────────
export const adminApi = {
  getChats:          (params) => api.get('/admin/chats', { params }),
  getSessionMessages:(id)     => api.get(`/admin/chats/${id}/messages`),
  patchBusiness:     (data)   => api.patch('/admin/business', data),
};

// ────────────────────────────────────────────────
// Chat endpoint
// ────────────────────────────────────────────────
export const chatApi = {
  send: (data) => api.post('/chat', data),
};

export default api;
""")

# ══════════════════════════════════════════════
# context/AuthContext.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/context/AuthContext.jsx", """\
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authApi } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user,       setUser]       = useState(null);
  const [businessId, setBusinessId] = useState(null);
  const [loading,    setLoading]    = useState(true); // checking session on mount

  // ── Bootstrap: restore session from localStorage ──
  useEffect(() => {
    const token = localStorage.getItem('bizchat_token');
    const storedBizId = localStorage.getItem('bizchat_business_id');
    if (token) {
      authApi.getMe()
        .then((res) => {
          setUser(res.data.user);
          const bizId = storedBizId || res.data.user?.business?._id || res.data.user?.business;
          setBusinessId(bizId || null);
        })
        .catch(() => {
          localStorage.removeItem('bizchat_token');
          localStorage.removeItem('bizchat_business_id');
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  // ── Register ──────────────────────────────────────
  const register = useCallback(async (name, email, password) => {
    const res = await authApi.register({ name, email, password });
    const { token, user: u, businessId: bId } = res.data;
    localStorage.setItem('bizchat_token', token);
    localStorage.setItem('bizchat_business_id', bId);
    setUser(u);
    setBusinessId(bId);
    return res.data;
  }, []);

  // ── Login ─────────────────────────────────────────
  const login = useCallback(async (email, password) => {
    const res = await authApi.login({ email, password });
    const { token, user: u, businessId: bId } = res.data;
    localStorage.setItem('bizchat_token', token);
    localStorage.setItem('bizchat_business_id', bId);
    setUser(u);
    setBusinessId(bId);
    return res.data;
  }, []);

  // ── Logout ────────────────────────────────────────
  const logout = useCallback(() => {
    localStorage.removeItem('bizchat_token');
    localStorage.removeItem('bizchat_business_id');
    setUser(null);
    setBusinessId(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, businessId, loading, register, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
""")

# ══════════════════════════════════════════════
# components/Spinner.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/components/Spinner.jsx", """\
const Spinner = ({ size = 'md', className = '' }) => {
  const sizes = { sm: 'h-4 w-4', md: 'h-6 w-6', lg: 'h-10 w-10' };
  return (
    <div
      className={`animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600 ${sizes[size]} ${className}`}
      aria-label="Loading"
    />
  );
};

export default Spinner;
""")

# ══════════════════════════════════════════════
# components/Navbar.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/components/Navbar.jsx", """\
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navLink = (to, label) => (
    <Link
      to={to}
      className={`text-sm font-medium px-3 py-1.5 rounded-md transition-colors ${
        pathname === to
          ? 'bg-indigo-100 text-indigo-700'
          : 'text-slate-600 hover:text-indigo-600 hover:bg-slate-100'
      }`}
    >
      {label}
    </Link>
  );

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        {/* Brand */}
        <Link to="/dashboard" className="flex items-center gap-2 font-semibold text-indigo-600 text-base">
          <span className="text-xl">💬</span> BizChat AI
        </Link>

        {/* Nav links */}
        {user && (
          <div className="hidden sm:flex items-center gap-1">
            {navLink('/dashboard', 'Dashboard')}
            {navLink('/admin',     'Admin Panel')}
          </div>
        )}

        {/* User menu */}
        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden sm:block text-sm text-slate-500 truncate max-w-[140px]">
                {user.name}
              </span>
              <button onClick={handleLogout} className="btn-secondary text-xs py-1.5 px-3">
                Logout
              </button>
            </>
          ) : (
            <div className="flex gap-2">
              {navLink('/login',    'Login')}
              {navLink('/register', 'Register')}
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
""")

# ══════════════════════════════════════════════
# components/Layout.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/components/Layout.jsx", """\
import Navbar from './Navbar';

const Layout = ({ children }) => (
  <div className=\"min-h-screen flex flex-col bg-slate-50\">
    <Navbar />
    <main className=\"flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8\">
      {children}
    </main>
  </div>
);

export default Layout;
""")

# ══════════════════════════════════════════════
# components/ProtectedRoute.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/components/ProtectedRoute.jsx", """\
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Spinner from './Spinner';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className=\"min-h-screen flex items-center justify-center\">
        <Spinner size=\"lg\" />
      </div>
    );
  }
  return user ? children : <Navigate to=\"/login\" replace />;
};

export default ProtectedRoute;
""")

print("✅  Auth context, API service layer, and shared components written")
