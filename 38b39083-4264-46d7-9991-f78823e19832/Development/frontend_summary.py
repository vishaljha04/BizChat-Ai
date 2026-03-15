
import os

# Verify all expected files exist
expected = [
    "frontend/package.json",
    "frontend/vite.config.js",
    "frontend/tailwind.config.js",
    "frontend/postcss.config.js",
    "frontend/index.html",
    "frontend/public/widget.js",
    "frontend/src/main.jsx",
    "frontend/src/index.css",
    "frontend/src/App.jsx",
    "frontend/src/context/AuthContext.jsx",
    "frontend/src/services/api.js",
    "frontend/src/components/Spinner.jsx",
    "frontend/src/components/Navbar.jsx",
    "frontend/src/components/Layout.jsx",
    "frontend/src/components/ProtectedRoute.jsx",
    "frontend/src/components/ChatWidget.jsx",
    "frontend/src/pages/Login.jsx",
    "frontend/src/pages/Register.jsx",
    "frontend/src/pages/Dashboard.jsx",
    "frontend/src/pages/AdminPanel.jsx",
]

print("=" * 60)
print("  BizChat AI — Frontend Scaffold Complete!")
print("=" * 60)
print()
print("  frontend/")
print("  ├── package.json          (Vite + React 18 + Tailwind + axios)")
print("  ├── vite.config.js        (dev server + /api proxy)")
print("  ├── tailwind.config.js    (indigo/slate palette, Inter font)")
print("  ├── postcss.config.js")
print("  ├── index.html            (Inter Google Font, root mount)")
print("  ├── public/")
print("  │   └── widget.js         ★ standalone embed snippet")
print("  └── src/")
print("      ├── main.jsx          (React root)")
print("      ├── index.css         (Tailwind layers + custom classes)")
print("      ├── App.jsx           (React Router: Login|Register|Dashboard|Admin)")
print("      ├── context/")
print("      │   └── AuthContext.jsx  (JWT + register/login/logout)")
print("      ├── services/")
print("      │   └── api.js           (axios: authApi|businessApi|adminApi|chatApi)")
print("      ├── components/")
print("      │   ├── Spinner.jsx")
print("      │   ├── Navbar.jsx")
print("      │   ├── Layout.jsx")
print("      │   ├── ProtectedRoute.jsx")
print("      │   └── ChatWidget.jsx   ★ embeddable React component")
print("      └── pages/")
print("          ├── Login.jsx")
print("          ├── Register.jsx")
print("          ├── Dashboard.jsx    (business info form — all fields)")
print("          └── AdminPanel.jsx   (tabbed: Chat History | FAQ Editor | Biz Info)")
print()
print("─" * 60)
print("  File check:")
all_ok = True
for path in expected:
    exists = os.path.isfile(path)
    status = "✅" if exists else "❌"
    if not exists:
        all_ok = False
    print(f"  {status}  {path}")

print()
if all_ok:
    print("  All 20 files verified ✅")
else:
    print("  ⚠️  Some files missing — check above")

print()
print("─" * 60)
print("  🚀  Getting started:")
print()
print("  cd frontend")
print("  npm install")
print("  npm run dev        →  http://localhost:3000")
print()
print("  🔌  Embed widget on any website:")
print()
print("  <script")
print('    src="https://your-domain.com/widget.js"')
print('    data-business-id="<YOUR_MONGO_ID>"')
print('    data-api-base="https://your-api.com/api"')
print('    data-title="Chat with us"')
print('    data-primary-color="#4f46e5"')
print("  ></script>")
