import React, { useState } from 'react';
import './App.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LoginForm, RegisterForm } from './components/Auth';
import { Dashboard } from './components/Dashboard';
import apiClient from './api/client';
import { 
  MessageSquare, LayoutDashboard, LogOut, User as UserIcon, 
  ChevronRight, BrainCircuit, HeartHandshake, ShieldCheck, Mic, MicOff 
} from 'lucide-react';

const MainApp: React.FC = () => {
  const { userEmail, logout, isAuthenticated } = useAuth();
  const [view, setView] = useState<'chat' | 'dashboard'>('chat');
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  
  // Chat State
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Voice Recognition Setup
  const startListening = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support voice recognition. Please try Chrome or Edge.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setText(prev => prev + " " + transcript);
    };
    recognition.onend = () => setIsListening(false);
    recognition.start();
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiClient.post('/predict', { text });
      setResult(response.data);
      setText('');
    } catch (err: any) {
      console.error('Analysis Error:', err);
      if (err.response) {
        // Server responded with an error
        const detail = err.response.data?.detail;
        setError(Array.isArray(detail) ? detail[0].msg : (detail || `Server Error: ${err.response.status}`));
      } else if (err.request) {
        // Request made but no response (Network Error)
        setError('Network Error: The API is unreachable. Please ensure the backend is running on port 8001.');
      } else {
        setError(`Error: ${err.message}`);
      }
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
        </div>
        <div className="nav-user">
          <div className="user-info">
            <UserIcon size={18} />
            <span>{userEmail?.split('@')[0]}</span>
          </div>
          <button onClick={logout} className="logout-btn">
            <LogOut size={18} /> <span>Logout</span>
          </button>
        </div>
      </nav>

      <main className="content-area">
        <header className="content-header">
          <h2>{view === 'chat' ? 'AI Support Session' : 'Mental Health Dashboard'}</h2>
          <p>{view === 'chat' ? 'Share your thoughts with our hybrid AI system.' : 'Visualizing your emotional trends over time.'}</p>
        </header>

        {view === 'chat' ? (
          <div className="chat-container">
            <div className="chat-main">
              {result && (
                <div className="results-section fade-in">
                  <div className="results-grid">
                    <div className="result-card">
                      <h3>Risk Level</h3>
                      <div className={`risk-badge risk-${result.risk.toLowerCase()}`}>
                        {result.risk.toUpperCase()}
                      </div>
                      <p className="confidence">Confidence: {(result.score * 100).toFixed(0)}%</p>
                    </div>
                    <div className="result-card">
                      <h3>Detected Emotion</h3>
                      <div className="emotion-display">
                        <span className="emotion-text">{result.emotion.toUpperCase()}</span>
                      </div>
                    </div>
                  </div>

                  <div className="support-message ai-gen">
                    <h3>✨ AI Personalized Support</h3>
                    <p>{result.ai_generated_response}</p>
                  </div>

                  {result.resources && (
                    <div className="crisis-resources">
                      <h3>⚠️ Crisis Resources</h3>
                      <p>{result.resources}</p>
                    </div>
                  )}
                </div>
              )}

              <form className="chat-input-area" onSubmit={handlePredict}>
                <div className="textarea-wrapper">
                  <textarea 
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="How are you feeling right now?"
                    rows={3}
                  />
                  <button 
                    type="button" 
                    className={`mic-btn ${isListening ? 'listening' : ''}`}
                    onClick={startListening}
                  >
                    {isListening ? <MicOff size={20} /> : <Mic size={20} />}
                  </button>
                </div>
                <button type="submit" disabled={loading || !text.trim()}>
                  {loading ? 'Analyzing...' : <><ChevronRight /> <span>Analyze</span></>}
                </button>
              </form>
              {error && <p className="chat-error">{error}</p>}
            </div>
            
            <aside className="chat-info">
              <div className="info-card">
                <HeartHandshake color="#3b82f6" />
                <h4>How it works</h4>
                <p>We use a specialized classifier for risk and a transformer model for emotional nuance.</p>
              </div>
              <div className="info-card">
                <ShieldCheck color="#10b981" />
                <h4>Your Privacy</h4>
                <p>Your logs are encrypted and stored securely in your personal profile.</p>
              </div>
            </aside>
          </div>
        ) : (
          <Dashboard />
        )}
      </main>
    </div>
  );
};

const App: React.FC = () => (
  <AuthProvider>
    <MainApp />
  </AuthProvider>
);

export default App;
