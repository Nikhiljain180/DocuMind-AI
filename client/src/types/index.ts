// User types
export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupData {
  email: string;
  username: string;
  password: string;
}

// Document types
export interface Document {
  id: string;
  user_id: string;
  filename: string;
  file_size: number;
  mime_type: string;
  vector_collection_id: string | null;
  uploaded_at: string;
}

// Chat types
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  sources?: ChatSource[];
}

export interface ChatSource {
  document_id: string;
  filename: string;
  chunk_index: number;
  relevance_score: number;
}

export interface ChatRequest {
  query: string;
  conversation_id: string | null;
}

export interface ChatResponse {
  answer: string;
  sources: ChatSource[];
  conversation_id: string | null;
}

// API Error type
export interface APIError {
  detail: string;
}

