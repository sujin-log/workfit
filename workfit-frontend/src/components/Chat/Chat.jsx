import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './Chat.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/chat/history`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setChatHistory(response.data.history || []);
    } catch (err) {
      console.error('채팅 이력 조회 실패:', err);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toLocaleTimeString('ko-KR')
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${API_URL}/api/chat`,
        { question: input },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      const assistantMessage = {
        role: 'assistant',
        content: response.data.answer || response.data.response,
        relatedLaws: response.data.related_laws || [],
        timestamp: new Date().toLocaleTimeString('ko-KR')
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('메시지 전송 실패:', err);
      setError('답변을 가져올 수 없습니다.');

      const errorMessage = {
        role: 'assistant',
        content: '죄송합니다. 답변을 생성하는 중 오류가 발생했습니다. 다시 시도해주세요.',
        timestamp: new Date().toLocaleTimeString('ko-KR')
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setShowHistory(false);
  };

  const loadChatFromHistory = (chat) => {
    setMessages(chat.messages || []);
    setShowHistory(false);
  };

  return (
    <div className="chat-container">
      <div className="chat-sidebar">
        <button className="btn-new-chat" onClick={startNewChat}>
          ✨ 새로운 대화
        </button>

        <div className="history-section">
          <button
            className={`btn-toggle-history ${showHistory ? 'active' : ''}`}
            onClick={() => setShowHistory(!showHistory)}
          >
            📋 대화 이력
          </button>

          {showHistory && (
            <div className="history-list">
              {chatHistory.length > 0 ? (
                chatHistory.map((chat, idx) => (
                  <div
                    key={idx}
                    className="history-item"
                    onClick={() => loadChatFromHistory(chat)}
                  >
                    <span className="history-title">
                      {chat.title || chat.messages?.[0]?.content?.substring(0, 30) || '새 대화'}
                    </span>
                    <span className="history-date">
                      {new Date(chat.created_at).toLocaleDateString('ko-KR')}
                    </span>
                  </div>
                ))
              ) : (
                <p className="no-history">대화 이력이 없습니다</p>
              )}
            </div>
          )}
        </div>
      </div>

      <div className="chat-main">
        <div className="chat-header">
          <h1>💬 워크챗</h1>
          <p>정책 관련 질문을 자유롭게 물어보세요</p>
        </div>

        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>👋 워크챗에 오신 것을 환영합니다</h2>
              <p>청년 정책에 대해 궁금한 점을 물어보세요!</p>
              <div className="suggested-questions">
                <p>💡 예시 질문:</p>
                <ul>
                  <li>"청년창업지원금은 어디서 신청하나요?"</li>
                  <li>"주택청약 자격 요건이 뭐예요?"</li>
                  <li>"실업급여는 어떻게 받나요?"</li>
                </ul>
              </div>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                {msg.relatedLaws && msg.relatedLaws.length > 0 && (
                  <div className="related-laws">
                    <strong>관련 법조항:</strong>
                    <ul>
                      {msg.relatedLaws.map((law, i) => (
                        <li key={i}>{law}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              <span className="message-time">{msg.timestamp}</span>
            </div>
          ))}

          {loading && (
            <div className="message assistant loading">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {error && <div className="error-message">{error}</div>}

        <form className="chat-input-form" onSubmit={sendMessage}>
          <input
            type="text"
            placeholder="질문을 입력하세요..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            className="chat-input"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="btn-send"
          >
            전송
          </button>
        </form>
      </div>
    </div>
  );
}
