import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import { LoginForm, RegisterForm } from './components/Auth';
import { Dashboard } from './components/Dashboard';
import { BreathingExercise } from './components/Grounding';
import { Profile } from './components/Profile';
import apiClient from './api/client';
import { 
  MessageSquare, LayoutDashboard, LogOut, User as UserIcon, 
  ChevronRight, BrainCircuit, HeartHandshake, ShieldCheck, 
  Mic, MicOff, Sun, Moon, Wind, Send, Sparkles
} from 'lucide-react';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  risk?: string;
  emotion?: string;
  timestamp: Date;
}

const MainApp: React.FC = () => {
  const { userEmail, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [view, setView] = useState<'chat' | 'dashboard' | 'grounding' | 'profile'>('chat');
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  
  // User Data State
  const [userData, setUserData] = useState<any>(null);
  const [profilePic, setProfilePic] = useState<string | null>(null);

  // Chat State
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Helper to get base URL
  const getBaseUrl = () => import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '');

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load user data and history
  useEffect(() => {
    if (isAuthenticated) {
      const loadInitialData = async () => {
        try {
          // 1. Load Profile
          const profRes = await apiClient.get('/users/me');
          setUserData(profRes.data);
          if (profRes.data.profile_image) {
            setProfilePic(`${getBaseUrl()}/${profRes.data.profile_image}`);
          }

          // 2. Load History if in chat view
          if (view === 'chat') {
            const res = await apiClient.get('/moods/');
            const history: ChatMessage[] = [];
            res.data.slice(0, 10).reverse().forEach((log: any) => {
              history.push({ role: 'user', content: log.user_text, timestamp: new Date(log.created_at) });
              history.push({ 
                role: 'assistant', 
                content: log.ai_response, 
                risk: log.risk_level, 
                emotion: log.emotion,
                timestamp: new Date(log.created_at) 
              });
            });
            setMessages(history);
          }
        } catch (err) {
          console.error("Data loading error", err);
        }
      };
      void loadInitialData();
    }
  }, [isAuthenticated, view]);

  const startListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) return alert("Browser not supported.");
    const recognition = new SpeechRecognition();
    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event: any) => setInputText(prev => prev + " " + event.results[0][0].transcript);
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg: ChatMessage = { role: 'user', content: inputText, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = inputText;
    setInputText('');
    setLoading(true);

    try {
      const response = await apiClient.post('/predict', { text: currentInput });
      const aiMsg: ChatMessage = {
        role: 'assistant',
        content: response.data.ai_generated_response,
        risk: response.data.risk,
        emotion: response.data.emotion,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err: any) {
      console.error("AI connection interrupted.", err);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="auth-page">
        <div className="auth-container">
          <div className="brand-section">
            <BrainCircuit size={60} color="#3b82f6" />
            <h1>Sentimental AI</h1>
            <p>Enterprise-grade mental health monitoring & supportive AI.</p>
            <div className="feature-list">
              <div className="feature-item"><ShieldCheck size={18} /><span>Secure & Encrypted</span></div>
              <div className="feature-item"><BrainCircuit size={18} /><span>Hybrid AI Analysis</span></div>
              <div className="feature-item"><LayoutDashboard size={18} /><span>Mood Trend Tracking</span></div>
            </div>
          </div>
          {authMode === 'login' ? (
            <LoginForm onSuccess={() => setView('chat')} toggleForm={() => setAuthMode('register')} />
          ) : (
            <RegisterForm onSuccess={() => setAuthMode('login')} toggleForm={() => setAuthMode('login')} />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      {/* Mobile Top Header */}
      <header className="mobile-header">
        <div className="nav-brand">
          <BrainCircuit size={24} color="#3b82f6" />
          <span>Sentimental AI</span>
        </div>
        <button className="theme-icon-btn" onClick={toggleTheme}>
          {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
      </header>

      <nav className="side-nav">
        <div className="nav-brand">
          <BrainCircuit color="#3b82f6" />
          <span>Sentimental AI</span>
        </div>
        <div className="nav-links">
          <button className={view === 'chat' ? 'active' : ''} onClick={() => setView('chat')}>
            <MessageSquare size={20} /> <span>Support AI</span>
          </button>
          <button className={view === 'dashboard' ? 'active' : ''} onClick={() => setView('dashboard')}>
            <LayoutDashboard size={20} /> <span>My Journey</span>
          </button>
          <button className={view === 'grounding' ? 'active' : ''} onClick={() => setView('grounding')}>
            <Wind size={20} /> <span>Grounding</span>
          </button>
          <button className={view === 'profile' ? 'active' : ''} onClick={() => setView('profile')}>
            <UserIcon size={20} /> <span>My Profile</span>
          </button>
        </div>
        
        <div className="nav-user">
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === 'light' ? <><Moon size={18} /> Dark Mode</> : <><Sun size={18} /> Light Mode</>}
          </button>
          <div className="user-info">
            {profilePic ? (
              <img src={profilePic} alt="Avatar" className="nav-avatar" />
            ) : (
              <div className="nav-avatar-placeholder"><UserIcon size={16} /></div>
            )}
            <span className="user-name-nav">{userData?.full_name || userEmail?.split('@')[0]}</span>
          </div>
          <button onClick={logout} className="logout-btn">
            <LogOut size={18} /> <span>Logout</span>
          </button>
        </div>
      </nav>

      <main className="content-area">
        {view === 'chat' && (
          <div className="chat-interface">
            <div className="chat-window">
              {messages.length === 0 && (
                <div className="empty-chat">
                  <Sparkles size={48} color="#3b82f6" />
                  <h3>Welcome, {userData?.full_name || 'Friend'}.</h3>
                  <p>How are you feeling right now? Your safe space is open.</p>
                </div>
              )}
              {messages.map((msg, idx) => (
                <div key={idx} className={`message-bubble ${msg.role}`}>
                  <div className="bubble-wrapper">
                    {msg.role === 'assistant' ? (
                      <div className="bubble-avatar ai"><BrainCircuit size={16} /></div>
                    ) : (
                      <div className="bubble-avatar user">
                        {profilePic ? <img src={profilePic} alt="Me" /> : <UserIcon size={16} />}
                      </div>
                    )}
                    <div className="bubble-content">
                      <p>{msg.content}</p>
                      {msg.role === 'assistant' && msg.risk && (
                        <div className="bubble-meta">
                          <span className={`mini-badge risk-${msg.risk.toLowerCase()}`}>{msg.risk}</span>
                          <span className="mini-badge emotion">{msg.emotion}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message-bubble assistant loading">
                  <div className="bubble-wrapper">
                    <div className="bubble-avatar ai"><BrainCircuit size={16} /></div>
                    <div className="typing-dots"><span>.</span><span>.</span><span>.</span></div>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            <form className="chat-input-wrapper" onSubmit={handleSendMessage}>
              <div className="input-box">
                <textarea 
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Tell me what's on your mind..."
                  rows={1}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSendMessage(e); } }}
                />
                <div className="input-actions">
                  <button type="button" className={`icon-btn ${isListening ? 'listening' : ''}`} onClick={startListening}>
                    {isListening ? <MicOff size={18} /> : <Mic size={18} />}
                  </button>
                  <button type="submit" className="send-btn" disabled={loading || !inputText.trim()}>
                    <Send size={18} />
                  </button>
                </div>
              </div>
            </form>
          </div>
        )}
        {view === 'dashboard' && <Dashboard />}
        {view === 'grounding' && <BreathingExercise />}
        {view === 'profile' && <Profile />}
      </main>

      {/* Mobile Bottom Nav */}
      <nav className="mobile-bottom-nav">
        <button className={view === 'chat' ? 'active' : ''} onClick={() => setView('chat')}>
          <MessageSquare size={20} />
          <span>Support</span>
        </button>
        <button className={view === 'dashboard' ? 'active' : ''} onClick={() => setView('dashboard')}>
          <LayoutDashboard size={20} />
          <span>Journey</span>
        </button>
        <button className={view === 'profile' ? 'active' : ''} onClick={() => setView('profile')}>
          <div className="mobile-nav-avatar">
            {profilePic ? <img src={profilePic} alt="P" /> : <UserIcon size={20} />}
          </div>
          <span>Profile</span>
        </button>
        <button onClick={logout}>
          <LogOut size={20} />
          <span>Exit</span>
        </button>
      </nav>
    </div>
  );
};

const App: React.FC = () => (
  <ThemeProvider>
    <AuthProvider>
      <MainApp />
    </AuthProvider>
  </ThemeProvider>
);

export default App;
