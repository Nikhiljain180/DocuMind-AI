import { useState, useEffect, useRef } from 'react';
import { ChatMessage as ChatMessageComponent } from '../components/chat/ChatMessage';
import { ChatInput } from '../components/chat/ChatInput';
import { api } from '../services/api';
import { ChatMessage, Document } from '../types';
import toast from 'react-hot-toast';
import { v4 as uuidv4 } from 'uuid';

export const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loadingDocs, setLoadingDocs] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load messages from localStorage on mount
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const docs = await api.getDocuments();
        setDocuments(docs);
      } catch (error: any) {
        toast.error('Failed to fetch documents');
      } finally {
        setLoadingDocs(false);
      }
    };

    fetchDocuments();

    // Load chat history from localStorage
    const savedMessages = localStorage.getItem('chatHistory');
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        // Convert timestamp strings back to Date objects
        const messagesWithDates = parsed.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp),
        }));
        setMessages(messagesWithDates);
      } catch (error) {
        console.error('Failed to load chat history:', error);
        // If loading fails, show welcome message
        setMessages([
          {
            id: uuidv4(),
            role: 'assistant',
            content: 'Hello! I\'m your AI assistant. Upload some documents and ask me questions about them. I\'ll provide answers based on your document content.',
            timestamp: new Date(),
          },
        ]);
      }
    } else {
      // Add welcome message if no history
      setMessages([
        {
          id: uuidv4(),
          role: 'assistant',
          content: 'Hello! I\'m your AI assistant. Upload some documents and ask me questions about them. I\'ll provide answers based on your document content.',
          timestamp: new Date(),
        },
      ]);
    }
  }, []);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chatHistory', JSON.stringify(messages));
    }
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await api.chat({
        query: content,
        conversation_id: null,
      });

      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
        sources: response.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to get response');
      
      // Add error message
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const indexedDocsCount = documents.filter(doc => doc.vector_collection_id).length;

  const clearChatHistory = () => {
    if (window.confirm('Are you sure you want to clear all chat history?')) {
      localStorage.removeItem('chatHistory');
      setMessages([
        {
          id: uuidv4(),
          role: 'assistant',
          content: 'Hello! I\'m your AI assistant. Upload some documents and ask me questions about them. I\'ll provide answers based on your document content.',
          timestamp: new Date(),
        },
      ]);
      toast.success('Chat history cleared');
    }
  };

  return (
    <div className="max-w-6xl mx-auto h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="mb-4">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900">Chat with Your Documents</h1>
          {messages.length > 1 && (
            <button
              onClick={clearChatHistory}
              className="text-sm text-red-600 hover:text-red-700 hover:underline flex items-center space-x-1"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span>Clear History</span>
            </button>
          )}
        </div>
        <div className="flex items-center space-x-4 mt-2">
          {loadingDocs ? (
            <p className="text-sm text-gray-500">Loading documents...</p>
          ) : (
            <>
              <p className="text-sm text-gray-600">
                {indexedDocsCount} document{indexedDocsCount !== 1 ? 's' : ''} indexed
              </p>
              {documents.length === 0 && (
                <p className="text-sm text-orange-600">
                  ⚠️ No documents uploaded. Go to Documents page to upload some!
                </p>
              )}
              {documents.length > 0 && indexedDocsCount === 0 && (
                <p className="text-sm text-orange-600">
                  ⚠️ Documents are being processed. Please wait...
                </p>
              )}
            </>
          )}
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
                <p className="mt-2 text-sm text-gray-500">Start a conversation</p>
              </div>
            </div>
          ) : (
            <>
              {messages.map((message) => (
                <ChatMessageComponent key={message.id} message={message} />
              ))}
              {loading && (
                <div className="flex justify-start mb-4">
                  <div className="flex items-center space-x-2 bg-gray-100 rounded-lg px-4 py-3">
                    <svg className="animate-spin h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24">
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    <span className="text-sm text-gray-600">AI is thinking...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input */}
        <ChatInput onSendMessage={handleSendMessage} disabled={loading} />
      </div>

      {/* Helper Text */}
      {indexedDocsCount > 0 && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <p className="text-sm text-blue-800">
            💡 <strong>Tip:</strong> Ask specific questions about your documents. For example: "What is the main topic?", "Summarize the key points", or "What does it say about X?"
          </p>
        </div>
      )}
    </div>
  );
};

