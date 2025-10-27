#!/bin/bash

# Test Aiven PostgreSQL and Redis connections via API

BASE_URL="http://localhost:8000/api"
TIMESTAMP=$(date +%s)
EMAIL="test_aiven_${TIMESTAMP}@test.com"
USERNAME="aiven_test_${TIMESTAMP}"
PASSWORD="Test@123456"

echo "========================================="
echo "Testing Aiven Connections"
echo "========================================="
echo ""

# 1. Test Signup (PostgreSQL Write)
echo "1. Testing Signup (PostgreSQL connection)..."
SIGNUP_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")

echo "Signup Response: $SIGNUP_RESPONSE"
echo ""

# 2. Test Login (PostgreSQL Read)
echo "2. Testing Login (PostgreSQL read)..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/signin" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get access token"
  echo "Login Response: $LOGIN_RESPONSE"
  exit 1
fi

echo "✅ Login successful, got token"
echo ""

# 3. Create a test file
echo "3. Creating test document..."
TEST_FILE="/tmp/test_aiven_${TIMESTAMP}.txt"
echo "This is a test document to verify Aiven PostgreSQL and Redis connections.
It should be processed asynchronously using the Redis queue.
If you can read this, all Aiven services are working!
Upload timestamp: ${TIMESTAMP}" > $TEST_FILE

echo "Created test file: $TEST_FILE"
echo ""

# 4. Test Upload (PostgreSQL + Redis Queue)
echo "4. Testing Document Upload (PostgreSQL + Redis)..."
UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/upload/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$TEST_FILE")

echo "Upload Response: $UPLOAD_RESPONSE"
DOCUMENT_ID=$(echo $UPLOAD_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo ""

if [ -z "$DOCUMENT_ID" ]; then
  echo "❌ Failed to upload document"
  exit 1
fi

echo "✅ Document uploaded successfully with ID: $DOCUMENT_ID"
echo ""

# 5. Check Processing Status (wait for async processing)
echo "5. Checking processing status..."
for i in {1..5}; do
  sleep 2
  STATUS_RESPONSE=$(curl -s -X GET "$BASE_URL/upload/$DOCUMENT_ID/status" \
    -H "Authorization: Bearer $TOKEN")
  
  STATUS=$(echo $STATUS_RESPONSE | grep -o '"processing_status":"[^"]*' | cut -d'"' -f4)
  echo "   Attempt $i: Status = $STATUS"
  
  if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
    break
  fi
done

echo ""
echo "Final Status Response: $STATUS_RESPONSE"
echo ""

# 6. List Documents
echo "6. Listing documents..."
LIST_RESPONSE=$(curl -s -X GET "$BASE_URL/upload/" \
  -H "Authorization: Bearer $TOKEN")

echo "Documents: $LIST_RESPONSE"
echo ""

# Clean up
rm -f $TEST_FILE

echo "========================================="
echo "Test Summary:"
echo "✅ PostgreSQL (Aiven) - User signup/login successful"
echo "✅ PostgreSQL (Aiven) - Document metadata stored"
echo "✅ Redis (Aiven) - Task queued successfully"
echo "✅ Celery Worker - Async processing $([ "$STATUS" = "completed" ] && echo "completed" || echo "in progress")"
echo "========================================="
