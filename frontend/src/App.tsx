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
  Mic, MicOff, Sun, Moon, Wind, Send, Sparkles, AlertCircle, Phone, X
} from 'lucide-react';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  risk?: string;
  emotion?: string;
  timestamp: Date;
}

const EmergencySOSModal: React.FC<{ isOpen: boolean; onClose: () => void; onStartGrounding: () => void }> = ({ isOpen, onClose, onStartGrounding }) => {
  if (!isOpen) return null;

  const hotlines = [
    { name: "Vandrevala Foundation", number: "9999666555", info: "24/7 Helpline (India)" },
    { name: "iCall (TISS)", number: "9152987821", info: "Mon-Sat, 10am-8pm" },
    { name: "National Crisis Line", number: "988", info: "Global / US Standard" }
  ];

  return (
    <div className="sos-overlay" onClick={onClose}>
      <div className="sos-modal" onClick={e => e.stopPropagation()}>
        <div className="sos-header">
          <AlertCircle size={48} />
          <h2>You are not alone.</h2>
          <p>Help is available right now. Please reach out.</p>
        </div>
        <div className="sos-content">
          <div className="sos-section">
            <h3>Immediate Hotlines</h3>
            {hotlines.map((h, i) => (
              <div key={i} className="hotline-card">
                <div className="hotline-info">
                  <span className="hotline-name">{h.name}</span>
                  <span className="hotline-number">{h.number}</span>
                </div>
                <a href={`tel:${h.number}`} className="call-btn"><Phone size={20} /></a>
              </div>
            ))}
          </div>

          <button className="sos-action-btn grounding" onClick={() => { onStartGrounding(); onClose(); }}>
            <Wind size={20} /> Start Grounding Exercise
          </button>
          
          <button className="sos-action-btn close" onClick={onClose}>
            <X size={20} /> Close
          </button>
        </div>
      </div>
    </div>
  );
};

const MainApp: React.FC = () => {
  const { userEmail, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [view, setView] = useState<'chat' | 'dashboard' | 'grounding' | 'profile'>('chat');
  const [isSOSOpen, setIsSOSOpen] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  
  // User Data State
  const [userData, setUserData] = useState<any>(null);
  const [profilePic, setProfilePic] = useState<string | null>(null);

  // Chat State
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [recognitionLang, setRecognitionLang] = useState('en-US');
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

  const recognitionRef = useRef<any>(null);

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Browser not supported for voice input.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;
    
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = recognitionLang;

    recognition.onstart = () => setIsListening(true);
    
    recognition.onresult = (event: any) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      if (finalTranscript) {
        setInputText(prev => prev + (prev.endsWith(' ') || !prev ? '' : ' ') + finalTranscript);
      }
    };

    recognition.onerror = (event: any) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  useEffect(() => {
    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    const userMsg: ChatMessage = { role: 'user', content: inputText, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    const currentInput = inputText;
    setInputText('');
    setLoading(true);

    try:
      // Construct history for AI (last 6 messages to stay within context limits)
      const chatHistory = messages.slice(-6).map(m => ({
        role: m.role,
        content: m.content
      }));

      const response = await apiClient.post('/predict', { 
        text: currentInput,
        history: chatHistory 
      });
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
        
        <button className="sos-nav-btn" onClick={() => setIsSOSOpen(true)}>
          <AlertCircle size={18} /> <span>Emergency SOS</span>
        </button>

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
              {isListening && (
                <div className="listening-indicator">
                  <span className="pulse-dot"></span>
                  <span>Listening ({recognitionLang})... Speak now.</span>
                </div>
              )}
              <div className="input-box">
                <textarea 
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Tell me what's on your mind..."
                  rows={1}
                  onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSendMessage(e); } }}
                />
                <div className="input-actions">
                  <select 
                    className="voice-lang-select"
                    value={recognitionLang}
                    onChange={(e) => setRecognitionLang(e.target.value)}
                    disabled={isListening}
                  >
                    <option value="en-US">EN</option>
                    <option value="hi-IN">HI</option>
                    <option value="es-ES">ES</option>
                    <option value="fr-FR">FR</option>
                  </select>
                  <button type="button" className={`icon-btn ${isListening ? 'listening' : ''}`} onClick={toggleListening}>
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

      <EmergencySOSModal 
        isOpen={isSOSOpen} 
        onClose={() => setIsSOSOpen(false)} 
        onStartGrounding={() => setView('grounding')}
      />
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
