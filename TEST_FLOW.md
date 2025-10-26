# ✅ Flow Verification Checklist

## 🎯 What We're Testing

1. **Async Document Upload** - Files process in background
2. **Chat History** - AI remembers previous conversations
3. **Combined Search** - Searches both documents + chat history

---

## 📋 Pre-Flight Check

### 1. Services Running ✓
```bash
# Check these are running:
✅ PostgreSQL (Aiven or Docker)
✅ Redis/Valkey (Aiven or Docker)  
✅ Qdrant (Docker)
✅ FastAPI Server (localhost:8000)
✅ Celery Worker (background)
✅ React Frontend (localhost:5173)
```

### 2. Database Migration ✓
```bash
# Already done:
alembic upgrade head
# ✅ Added processing_status, processing_error, task_id to documents
# ✅ Created chat_history table
```

### 3. Environment Variables ✓
```bash
# Check server/.env has:
DATABASE_URL=<your-aiven-postgres-url>
REDIS_URL=<your-aiven-valkey-url>
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=sk-your-key
```

---

## 🧪 Test Flow

### Test 1: Async Document Upload

**What to expect:**
- Upload returns immediately (HTTP 202)
- Document starts with status "pending"
- Background worker processes it
- Status changes to "processing" → "completed"

**Steps:**
1. Go to http://localhost:5173/documents
2. Upload a PDF file
3. Notice it appears immediately with status "pending"
4. Refresh every 2 seconds
5. Watch status change: `pending` → `processing` → `completed`

**API Test:**
```bash
# 1. Upload
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test.pdf"

# Response will have:
{
  "id": "doc-uuid",
  "processing_status": "pending",
  "task_id": "celery-task-id"
}

# 2. Check status
curl http://localhost:8000/api/upload/DOC_UUID/status \
  -H "Authorization: Bearer YOUR_TOKEN"

# Response:
{
  "status": "completed",  # or "processing" or "failed"
  "error": null
}
```

---

### Test 2: Chat History & Conversational Context

**What to expect:**
- First message creates conversation
- Follow-up messages use conversation context
- AI remembers previous questions
- Response includes `chat_context_used: true` for follow-ups

**Steps:**
1. Go to http://localhost:5173/chat
2. **First message:** "What is the revenue?"
3. **AI responds:** "Revenue is $5M..." (from your document)
4. **Follow-up:** "How does that compare to last year?"
5. **AI responds:** "Based on our previous discussion about revenue ($5M)..."
   - Notice it references the previous question!
   - Check `chat_context_used: true` in network tab

**API Test:**
```bash
# 1. First message
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the revenue?",
    "conversation_id": null
  }'

# Response:
{
  "answer": "Revenue is $5M...",
  "sources": [...],
  "conversation_id": "conv-uuid",
  "chat_context_used": false  // First message
}

# 2. Follow-up message (use same conversation_id)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does that compare to last year?",
    "conversation_id": "conv-uuid"
  }'

# Response:
{
  "answer": "Based on our previous discussion...",
  "sources": [...],
  "conversation_id": "conv-uuid",
  "chat_context_used": true  // ✨ Used previous conversation!
}
```

---

### Test 3: Multiple File Uploads (Async Power!)

**What to expect:**
- Upload 3 files simultaneously
- All return immediately
- All process in parallel
- No blocking, no timeouts

**Steps:**
1. Go to http://localhost:5173/documents
2. Select 3 PDF files and drop them all at once
3. All 3 appear immediately with status "pending"
4. Watch them all process in parallel
5. All become "completed" within ~30 seconds

---

## 🔍 Verification Points

### ✅ Check 1: Documents Table
```sql
SELECT id, filename, processing_status, task_id 
FROM documents 
WHERE user_id = 'your-user-id'
ORDER BY uploaded_at DESC;

-- Should show:
-- | filename  | processing_status | task_id        |
-- | test.pdf  | completed         | celery-uuid    |
```

### ✅ Check 2: Chat History Table
```sql
SELECT id, user_message, assistant_message, conversation_id 
FROM chat_history 
WHERE user_id = 'your-user-id'
ORDER BY created_at DESC 
LIMIT 5;

-- Should show your conversation pairs
```

### ✅ Check 3: Qdrant Collection
```bash
# Check vectors in Qdrant
curl http://localhost:6333/collections/user_YOUR_USER_ID/points

# Should contain:
# - Document chunks (payload.type not set)
# - Chat history (payload.type = "chat_history")
```

### ✅ Check 4: Celery Worker Logs
```bash
# Should see:
[2025-10-27 00:00:00] Task process_document_async[...] received
[2025-10-27 00:00:10] PROCESSING: Parsing document...
[2025-10-27 00:00:15] PROCESSING: Chunking text...
[2025-10-27 00:00:20] PROCESSING: Generating embeddings for 50 chunks...
[2025-10-27 00:00:30] Task process_document_async[...] succeeded
```

---

## 🐛 Troubleshooting

### Issue: Documents stuck in "pending"
**Solution:** Check if Celery worker is running
```bash
ps aux | grep celery
# If not running:
cd server && celery -A app.celery_app worker --loglevel=info
```

### Issue: "Connection refused" to Redis
**Solution:** Check Redis connection
```bash
# Test local Redis:
redis-cli ping
# Should return: PONG

# Test Aiven Redis:
redis-cli -u YOUR_REDIS_URL ping
# Should return: PONG
```

### Issue: Chat history not being used
**Solution:** Check Qdrant for chat history vectors
```bash
curl http://localhost:6333/collections/user_YOUR_ID/points
# Look for payload.type == "chat_history"
```

### Issue: Migration failed
**Solution:** Already fixed! But if needed:
```bash
# Rollback
alembic downgrade -1

# Re-run
alembic upgrade head
```

---

## 📊 Success Criteria

### ✅ Async Upload Working:
- [ ] Upload returns HTTP 202 (not 201)
- [ ] Document has `processing_status` field
- [ ] Status changes: pending → processing → completed
- [ ] Can upload multiple files simultaneously
- [ ] No blocking or timeouts

### ✅ Chat History Working:
- [ ] Conversations stored in database
- [ ] Follow-up questions get context
- [ ] Response includes `chat_context_used: true`
- [ ] AI references previous questions
- [ ] `conversation_id` maintained across messages

### ✅ Combined Search Working:
- [ ] Searches both documents (70%) and chat (30%)
- [ ] Chat history influences responses
- [ ] More natural conversation flow
- [ ] Better follow-up question handling

---

## 🎉 If Everything Works:

**Congratulations! You now have:**
1. ⚡ **Non-blocking async uploads** - Upload 10 files instantly
2. 💬 **Conversational AI** - Remembers previous questions
3. 🔍 **Context-aware search** - Uses both documents & chat history
4. 🚀 **Production-ready architecture** - Redis queue + Celery workers

---

## 📝 Next Steps

1. ✅ **All tests pass?** → Push to GitHub
2. 🚀 **Ready for production?** → Deploy to Render/Railway
3. 📊 **Want monitoring?** → Add Celery Flower
4. 🔧 **Need tuning?** → Adjust document/chat weight ratio

---

**Need help?** Check:
- `ASYNC_CHAT_GUIDE.md` - Comprehensive setup guide
- `WHATS_NEW.md` - Feature summary
- FastAPI docs: http://localhost:8000/docs

