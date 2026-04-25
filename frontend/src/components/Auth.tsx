import React, { useState } from 'react';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import { BrainCircuit, Mail, Lock, Eye, EyeOff, UserPlus, LogIn } from 'lucide-react';

interface AuthFormProps {
  onSuccess: () => void;
  toggleForm: () => void;
}

export const LoginForm: React.FC<AuthFormProps> = ({ onSuccess, toggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      login(response.data.access_token, email);
      onSuccess();
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail[0].msg);
      } else {
        setError(detail || 'Incorrect email or password.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card fade-in">
      <div className="auth-header">
        <div className="auth-icon-wrapper">
          <LogIn size={32} />
        </div>
        <h2>Welcome Back</h2>
        <p>Your mental health journey continues here.</p>
      </div>
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="input-field">
          <label>Email Address</label>
          <div className="input-group">
            <Mail size={18} className="field-icon" />
            <input 
              type="email" 
              placeholder="name@company.com" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required 
            />
          </div>
        </div>

        <div className="input-field">
          <label>Password</label>
          <div className="input-group">
            <Lock size={18} className="field-icon" />
            <input 
              type={showPassword ? "text" : "password"} 
              placeholder="••••••••" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
            <button 
              type="button" 
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>
        
        {error && <div className="auth-error-box">{error}</div>}
        
        <button type="submit" disabled={loading} className="auth-btn">
          {loading ? <span className="spinner-small"></span> : 'Sign In'}
        </button>
      </form>
      
      <div className="auth-divider">
        <span>OR</span>
      </div>
      
      <p className="auth-footer">
        New to Sentimental AI? <span onClick={toggleForm} className="link">Create an account</span>
      </p>
    </div>
  );
};

export const RegisterForm: React.FC<AuthFormProps> = ({ onSuccess, toggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await apiClient.post('/auth/register', { email, password });
      
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      const loginRes = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      login(loginRes.data.access_token, email);
      onSuccess();
    } catch (err: any) {
      if (!err.response) {
        setError('Server Unreachable. Please try again later.');
      } else {
        const detail = err.response?.data?.detail;
        setError(Array.isArray(detail) ? detail[0].msg : (detail || 'Registration failed.'));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card fade-in">
      <div className="auth-header">
        <div className="auth-icon-wrapper signup">
          <UserPlus size={32} />
        </div>
        <h2>Join Sentimental AI</h2>
        <p>A safe space for your thoughts and growth.</p>
      </div>
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="input-field">
          <label>Email Address</label>
          <div className="input-group">
            <Mail size={18} className="field-icon" />
            <input 
              type="email" 
              placeholder="name@company.com" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              required 
            />
          </div>
        </div>

        <div className="input-field">
          <label>Password</label>
          <div className="input-group">
            <Lock size={18} className="field-icon" />
            <input 
              type={showPassword ? "text" : "password"} 
              placeholder="min. 8 characters" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
            />
            <button 
              type="button" 
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>
        
        {error && <div className="auth-error-box">{error}</div>}
        
        <button type="submit" disabled={loading} className="auth-btn">
          {loading ? <span className="spinner-small"></span> : 'Get Started'}
        </button>
      </form>
      
      <div className="auth-divider">
        <span>OR</span>
      </div>
      
      <p className="auth-footer">
        Already have an account? <span onClick={toggleForm} className="link">Sign In</span>
      </p>
    </div>
  );
};
