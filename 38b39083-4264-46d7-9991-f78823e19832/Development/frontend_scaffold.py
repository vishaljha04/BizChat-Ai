
import os

BASE = "frontend"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"✅  {path}")

# ══════════════════════════════════════════════
# package.json
# ══════════════════════════════════════════════
write_file(f"{BASE}/package.json", """\
{
  "name": "bizchat-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "axios": "^1.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.23.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.2",
    "eslint-plugin-react-hooks": "^4.6.2",
    "eslint-plugin-react-refresh": "^0.4.7",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "vite": "^5.2.11"
  }
}
""")

# ══════════════════════════════════════════════
# vite.config.js
# ══════════════════════════════════════════════
write_file(f"{BASE}/vite.config.js", """\
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});
""")

# ══════════════════════════════════════════════
# tailwind.config.js
# ══════════════════════════════════════════════
write_file(f"{BASE}/tailwind.config.js", """\
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        indigo: {
          50:  '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
""")

# ══════════════════════════════════════════════
# postcss.config.js
# ══════════════════════════════════════════════
write_file(f"{BASE}/postcss.config.js", """\
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
""")

# ══════════════════════════════════════════════
# index.html
# ══════════════════════════════════════════════
write_file(f"{BASE}/index.html", """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
    <title>BizChat AI – Smart Customer Support</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

# ══════════════════════════════════════════════
# src/main.jsx
# ══════════════════════════════════════════════
write_file(f"{BASE}/src/main.jsx", """\
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
""")

# ══════════════════════════════════════════════
# src/index.css  (Tailwind directives)
# ══════════════════════════════════════════════
write_file(f"{BASE}/src/index.css", """\
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply border-slate-200;
  }
  body {
    @apply bg-slate-50 text-slate-900 font-sans antialiased;
  }
}

@layer components {
  .btn-primary {
    @apply inline-flex items-center justify-center px-4 py-2 rounded-lg
           bg-indigo-600 text-white font-medium text-sm
           hover:bg-indigo-700 active:bg-indigo-800
           transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed;
  }
  .btn-secondary {
    @apply inline-flex items-center justify-center px-4 py-2 rounded-lg
           bg-white text-slate-700 font-medium text-sm border border-slate-300
           hover:bg-slate-50 active:bg-slate-100
           transition-colors duration-150 disabled:opacity-50 disabled:cursor-not-allowed;
  }
  .input-field {
    @apply block w-full px-3 py-2 rounded-lg border border-slate-300
           bg-white text-slate-900 placeholder-slate-400 text-sm
           focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent
           transition duration-150;
  }
  .card {
    @apply bg-white rounded-xl shadow-sm border border-slate-200 p-6;
  }
  .label {
    @apply block text-sm font-medium text-slate-700 mb-1;
  }
}

/* Smooth scrollbar for chat */
.chat-scroll::-webkit-scrollbar { width: 4px; }
.chat-scroll::-webkit-scrollbar-track { background: transparent; }
.chat-scroll::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

/* Typing animation dots */
@keyframes bounce-dot {
  0%, 80%, 100% { transform: translateY(0); opacity: .5; }
  40%           { transform: translateY(-6px); opacity: 1; }
}
.typing-dot { animation: bounce-dot 1.2s infinite ease-in-out; }
.typing-dot:nth-child(2) { animation-delay: .2s; }
.typing-dot:nth-child(3) { animation-delay: .4s; }
""")

print("✅  Vite + React + Tailwind scaffold written")
print(f"   {BASE}/package.json")
print(f"   {BASE}/vite.config.js")
print(f"   {BASE}/tailwind.config.js")
print(f"   {BASE}/postcss.config.js")
print(f"   {BASE}/index.html")
print(f"   {BASE}/src/main.jsx")
print(f"   {BASE}/src/index.css")
