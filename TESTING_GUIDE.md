# DocuMind AI - Testing Guide

## Current Status: Checkpoint 7 Complete ✅

Both frontend and backend are running and ready for testing!

### Services Running

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **PostgreSQL**: localhost:5432
- **Qdrant**: http://localhost:6333
- **Redis**: localhost:6379

---

## 🧪 Checkpoint 8: Authentication Flow Testing

### Test 1: User Signup (Frontend + Backend)

1. **Open browser** → http://localhost:5173
2. **Click "Sign Up"** in navbar
3. **Fill in the form**:
   - Email: `test2@example.com`
   - Username: `testuser2`
   - Password: `password123`
   - Confirm Password: `password123`
4. **Click "Sign up"** button
5. **Expected Result**:
   - ✅ Success toast notification
   - ✅ Automatically redirected to Dashboard
   - ✅ Navbar shows username
   - ✅ JWT token stored in localStorage

### Test 2: User Logout

1. **Click "Logout"** in navbar
2. **Expected Result**:
   - ✅ Redirected to login page
   - ✅ Token cleared from localStorage
   - ✅ Navbar shows "Login" and "Sign Up" buttons

### Test 3: User Login

1. **Click "Login"** in navbar
2. **Enter credentials**:
   - Email: `test2@example.com`
   - Password: `password123`
3. **Click "Sign in"** button
4. **Expected Result**:
   - ✅ Success toast: "Welcome back!"
   - ✅ Redirected to Dashboard
   - ✅ User info displayed

### Test 4: Protected Routes

1. **Logout** if logged in
2. **Try to access** http://localhost:5173/dashboard directly
3. **Expected Result**:
   - ✅ Automatically redirected to login page
   - ✅ Cannot access protected pages without auth

### Test 5: Auto-redirect When Logged In

1. **Login** first
2. **Try to access** http://localhost:5173/login
3. **Expected Result**:
   - ✅ Automatically redirected to dashboard
   - ✅ Cannot access login/signup when authenticated

---

## 🔧 Backend API Testing (via Swagger UI)

### Option 1: Using Swagger UI

1. Open http://localhost:8000/docs
2. Test endpoints directly in browser

### Option 2: Using curl

```bash
# Health check
curl http://localhost:8000/

# Create user
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test3@example.com",
    "username": "testuser3",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test3@example.com",
    "password": "password123"
  }'

# Get current user (replace TOKEN with actual token)
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🐛 Common Issues & Solutions

### Issue: CORS errors in browser console
**Solution**: Backend CORS is configured for http://localhost:5173. Make sure you're accessing from that exact URL.

### Issue: "Network Error" in frontend
**Solution**: 
1. Check backend is running: `curl http://localhost:8000/`
2. Check VITE_API_URL in `client/.env`
3. Restart frontend if needed

### Issue: 401 Unauthorized
**Solution**: Token might be expired or invalid. Logout and login again.

### Issue: Database connection errors
**Solution**: 
```bash
# Restart Docker services
docker-compose down
docker-compose up postgres qdrant redis -d
```

---

## ✅ What's Working

- [x] User signup with validation
- [x] User login with JWT tokens
- [x] Token persistence in localStorage
- [x] Protected routes
- [x] Auto-redirect logic
- [x] Logout functionality
- [x] Responsive navbar
- [x] Toast notifications
- [x] Error handling

---

## 🚀 Next Steps (Checkpoint 9)

Once authentication is verified:
- Document upload UI
- Document list view
- File drag-and-drop
- Upload progress
- Delete documents

---

## 📝 Developer Notes

### Frontend Stack
- React 18 + TypeScript
- Vite for dev server
- Redux Toolkit for state
- React Router v6
- Tailwind CSS
- Axios for API calls
- React Hot Toast

### Backend Stack
- FastAPI + Python 3.12
- PostgreSQL for data
- Qdrant for vectors
- Redis for caching
- OpenAI for embeddings & LLM
- JWT for auth
- Alembic for migrations

### Environment Variables
- Frontend: `client/.env` (VITE_API_URL)
- Backend: `server/.env` (all configs)

