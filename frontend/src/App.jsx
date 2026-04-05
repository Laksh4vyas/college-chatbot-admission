import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hi there! I'm the College Admission AI. How can I help you today?", isUser: false, meta: "System" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  
  const endOfChatRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    endOfChatRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Fetch Dashboard data on mount
  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await axios.get("http://localhost:8000/dashboard-data");
        setDashboardData(res.data);
      } catch (err) {
        console.error("Failed to fetch dashboard data");
      }
    };
    fetchDashboard();
  }, []);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { id: Date.now(), text: input, isUser: true };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/chat", { message: userMessage.text });
      const botMessage = {
        id: Date.now() + 1,
        text: res.data.answer,
        isUser: false,
        confidence: res.data.confidence,
        model: res.data.model
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: "Sorry, I am having trouble connecting to the server.",
        isUser: false,
        meta: "Error"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>College Admission AI</h1>
        <p>Powered by Soft-Voting ML Ensemble</p>
      </header>

      <div className="main-content">
        
        {/* Dashboard side panel */}
        <div className="dashboard-panel">
          <h2>
            <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Live Metrics
          </h2>
          {dashboardData ? (
            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Accuracy</div>
                <div className="metric-value">{(dashboardData.accuracy * 100).toFixed(0)}%</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Avg Confidence</div>
                <div className="metric-value">{(dashboardData.averageConfidence * 100).toFixed(0)}%</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Requests Served</div>
                <div className="metric-value">{dashboardData.requestsServed}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Active Models</div>
                <div className="metric-value" style={{fontSize: "0.9rem", lineHeight: "1.4"}}>
                  {dashboardData.activeModels.map((m, i) => <div key={i}>• {m}</div>)}
                </div>
              </div>
            </div>
          ) : (
            <div className="loading-dots">
              <span></span><span></span><span></span>
            </div>
          )}
        </div>

        {/* Chat UI panel */}
        <div className="chat-panel">
          <div className="chat-header">
            <span className="chat-badge">Live Chat</span>
            <div style={{color: "var(--text-muted)", fontSize: "0.85rem"}}>Stitch UI Interface</div>
          </div>

          <div className="chat-window">
            {messages.map(msg => (
              <div key={msg.id} className={`message-wrapper ${msg.isUser ? 'user' : 'bot'}`}>
                <div className="message-bubble">{msg.text}</div>
                <div className="message-meta">
                  {msg.isUser ? 'You' : (msg.meta || msg.model)}
                  {msg.confidence && (
                    <span className="confidence-score">
                      {(msg.confidence * 100).toFixed(1)}% Conf
                    </span>
                  )}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message-wrapper bot">
                <div className="message-bubble">
                  <div className="loading-dots">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={endOfChatRef} />
          </div>

          <form onSubmit={handleSend} className="chat-input-container">
            <input 
              type="text" 
              className="chat-input"
              placeholder="Ask about admissions, deadlines, housing..."
              value={input}
              onChange={e => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
              <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </form>
        </div>

      </div>
    </div>
  );
}

export default App;
