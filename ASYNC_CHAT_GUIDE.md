# Async Processing & Chat History Guide

## 🎉 New Features

### 1. **Async Document Processing with Redis Queue**
Files are now processed in the background! Upload multiple documents without waiting.

### 2. **Chat History with Conversational Context**
The AI now remembers previous conversations and uses them for better responses.

---

## 📋 What Changed

### Backend Enhancements

#### 1. **Async Document Upload**
- **Before**: Blocking upload (user waits for parsing + embedding)
- **After**: Instant upload response, processing happens in background
- **Status**: `HTTP 202 ACCEPTED` (instead of `201 CREATED`)
- **Returns**: Document record with `task_id` and `processing_status`

#### 2. **Chat History Storage**
- Each conversation is stored in PostgreSQL **and** Qdrant
- AI searches both documents (70%) and chat history (30%)
- Conversational context improves response quality

#### 3. **New Database Tables**
```sql
-- New fields in documents table
ALTER TABLE documents ADD COLUMN processing_status VARCHAR(50);
ALTER TABLE documents ADD COLUMN processing_error VARCHAR(512);
ALTER TABLE documents ADD COLUMN task_id VARCHAR(255);

-- New chat_history table
CREATE TABLE chat_history (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    user_message TEXT,
    assistant_message TEXT,
    vector_id VARCHAR(255),
    conversation_id UUID,
    created_at TIMESTAMP
);
```

---

## 🚀 Setup Guide

### Prerequisites
- **Redis** running (localhost:6379 or Aiven)
- **Celery worker** running for background tasks

### Step 1: Install Dependencies
```bash
cd server
uv pip install -r requirements.txt
```

New dependencies added:
- `redis==5.0.1`
- `celery==5.3.6`

### Step 2: Update Environment Variables
```bash
# server/.env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# For Aiven Redis/Valkey:
# REDIS_URL=rediss://default:password@host:port/0
```

### Step 3: Run Database Migration
```bash
cd server
alembic upgrade head
```

This will:
- Add `processing_status`, `processing_error`, `task_id` to `documents` table
- Create `chat_history` table

### Step 4: Start Redis (if not running)
```bash
# Docker
docker-compose up redis -d

# Or locally
redis-server
```

### Step 5: Start Celery Worker
```bash
cd server
source .venv/bin/activate

# Start Celery worker
celery -A app.celery_app worker --loglevel=info
```

**Keep this running in a separate terminal!**

### Step 6: Start FastAPI Server
```bash
cd server
source .venv/bin/activate
uvicorn app.main:app --reload
```

---

## 📤 Async Document Upload Flow

### 1. **Upload Document**
```bash
POST /api/upload/
```

**Response (HTTP 202 ACCEPTED):**
```json
{
  "id": "doc-uuid",
  "filename": "report.pdf",
  "processing_status": "pending",
  "task_id": "celery-task-id",
  "uploaded_at": "2025-10-26T..."
}
```

### 2. **Check Processing Status**
```bash
GET /api/upload/{document_id}/status
```

**Response:**
```json
{
  "document_id": "doc-uuid",
  "filename": "report.pdf",
  "status": "processing",  // pending | processing | completed | failed
  "error": null,
  "task": {
    "task_state": "PROCESSING",
    "task_info": {"status": "Generating embeddings for 150 chunks..."}
  }
}
```

### 3. **Processing States**
- **`pending`**: Queued, waiting for worker
- **`processing`**: Currently being processed
- **`completed`**: Ready for chat
- **`failed`**: Error occurred (check `processing_error`)

### 4. **Frontend Integration**
```javascript
// Upload file
const response = await api.uploadDocument(file);
const documentId = response.id;

// Poll status until complete
const checkStatus = async () => {
  const status = await api.getDocumentStatus(documentId);
  
  if (status.status === 'completed') {
    console.log('✅ Document ready!');
  } else if (status.status === 'failed') {
    console.error('❌ Error:', status.error);
  } else {
    // Still processing, check again in 2 seconds
    setTimeout(checkStatus, 2000);
  }
};

checkStatus();
```

---

## 💬 Chat History & Conversational Context

### How It Works

1. **User sends a message**
   ```json
   POST /api/chat/
   {
     "query": "What is the revenue?",
     "conversation_id": "optional-conv-uuid"
   }
   ```

2. **System searches:**
   - **70%**: Document chunks (existing behavior)
   - **30%**: Previous conversations (NEW!)

3. **AI generates response** using both contexts

4. **Conversation is stored:**
   - PostgreSQL: User message + AI response
   - Qdrant: Embedded conversation for future searches

5. **Response includes:**
   ```json
   {
     "answer": "According to our previous discussion and the Q3 report...",
     "sources": [...],
     "conversation_id": "conv-uuid",
     "chat_context_used": true
   }
   ```

### Benefits
- ✅ AI remembers previous questions
- ✅ Better context for follow-up questions
- ✅ More natural conversations
- ✅ Automatic conversation grouping

### Example Conversation
```
User: "What is our Q3 revenue?"
AI: "According to the Q3 report, revenue was $5M."

[Later in the same conversation_id]

User: "How does that compare to Q2?"
AI: "Based on our previous discussion about Q3 revenue ($5M) 
     and the Q2 report, Q2 revenue was $4.2M. 
     That's a 19% increase."
     [chat_context_used: true]
```

---

## 🛠️ Development Workflow

### Running Locally (Development)
```bash
# Terminal 1: Infrastructure
docker-compose up postgres qdrant redis -d

# Terminal 2: Celery Worker
cd server && source .venv/bin/activate
celery -A app.celery_app worker --loglevel=info

# Terminal 3: FastAPI Server
cd server && source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 4: React Frontend
cd client && nvm use 20
pnpm run dev
```

### Monitoring Celery Tasks
```bash
# View task status
celery -A app.celery_app inspect active

# View registered tasks
celery -A app.celery_app inspect registered

# Purge all tasks
celery -A app.celery_app purge
```

### Debugging
```bash
# Check Redis connection
redis-cli ping
# Expected: PONG

# Monitor Redis keys
redis-cli monitor

# Check Celery queue
redis-cli LLEN celery

# View Celery logs
celery -A app.celery_app worker --loglevel=debug
```

---

## 🚢 Production Deployment

### Option 1: Aiven (Recommended)
- **PostgreSQL**: Aiven PostgreSQL service
- **Redis/Valkey**: Aiven Valkey service (100% Redis-compatible)
- **Qdrant**: Qdrant Cloud (free tier)
- **Backend**: Render/Railway
- **Frontend**: Vercel

### Environment Variables
```bash
# Production .env
DATABASE_URL=postgresql+psycopg://user:pass@host:port/db?sslmode=require
REDIS_URL=rediss://default:pass@host:port/0
QDRANT_URL=https://your-cluster.qdrant.io
OPENAI_API_KEY=sk-your-key
```

### Scaling Considerations
1. **Multiple Celery Workers**: Scale horizontally
   ```bash
   celery -A app.celery_app worker --concurrency=4
   ```

2. **Task Priority Queues**: Separate fast/slow tasks
3. **Result Backend**: Use PostgreSQL instead of Redis for persistence

---

## 🧪 Testing

### Test Async Upload
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test.pdf"
```

### Test Status Check
```bash
curl http://localhost:8000/api/upload/{doc_id}/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test Chat with History
```bash
# First message
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the revenue?",
    "conversation_id": null
  }'

# Follow-up (use conversation_id from response)
curl -X POST http://localhost:8000/api/chat/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "And the profit?",
    "conversation_id": "CONVERSATION_ID_FROM_ABOVE"
  }'
```

---

## 🔍 Troubleshooting

### Issue: "Celery worker not processing tasks"
```bash
# Check if worker is running
ps aux | grep celery

# Check Redis connection
redis-cli ping

# Restart worker
celery -A app.celery_app worker --loglevel=debug
```

### Issue: "Document stuck in 'pending' status"
```bash
# Check Celery queue
redis-cli LLEN celery

# Inspect active tasks
celery -A app.celery_app inspect active

# Check for failed tasks
celery -A app.celery_app events
```

### Issue: "Chat history not being used"
```bash
# Check Qdrant for chat history vectors
# They should have payload.type == "chat_history"

# Verify in Qdrant dashboard or:
curl http://localhost:6333/collections/user_{user_id}/points
```

---

## 📊 Architecture Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   FastAPI   │◄──────┐
└──────┬──────┘       │
       │              │
       ├──────────────┤
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│  PostgreSQL │  │   Qdrant    │
│  (Metadata) │  │  (Vectors)  │
└─────────────┘  └─────────────┘
       ▲              ▲
       │              │
       ▼              ▼
┌─────────────┐  ┌─────────────┐
│    Redis    │  │   Celery    │
│   (Queue)   │◄─┤   Worker    │
└─────────────┘  └─────────────┘
                      │
                      ▼
                 ┌─────────────┐
                 │   OpenAI    │
                 │ (Embeddings)│
                 └─────────────┘
```

---

## 🎯 Next Steps

1. ✅ **Test async uploads** with multiple files
2. ✅ **Test chat history** with follow-up questions
3. ✅ **Monitor Celery** performance
4. 🔜 **Deploy to production** (Checkpoint 14)
5. 🔜 **Add rate limiting** (optional)
6. 🔜 **Add progress webhooks** (optional)

---

## 📚 Additional Resources

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)

---

**Questions? Open an issue on GitHub!** 🚀

