import React, { useState } from 'react';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import { LogIn, Mail, Lock } from 'lucide-react';

interface AuthFormProps {
  onSuccess: () => void;
  toggleForm: () => void;
}

export const LoginForm: React.FC<AuthFormProps> = ({ onSuccess, toggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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
        setError(detail || 'Login failed. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card fade-in">
      <div className="auth-header">
        <LogIn size={40} className="auth-icon" />
        <h2>Welcome Back</h2>
        <p>Login to track your mental health journey</p>
      </div>
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="input-group">
          <Mail size={18} />
          <input 
            type="email" 
            placeholder="Email Address" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div className="input-group">
          <Lock size={18} />
          <input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        
        {error && <p className="auth-error">{error}</p>}
        
        <button type="submit" disabled={loading} className="auth-btn">
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      
      <p className="auth-footer">
        Don't have an account? <span onClick={toggleForm}>Register here</span>
      </p>
    </div>
  );
};

export const RegisterForm: React.FC<AuthFormProps> = ({ onSuccess, toggleForm }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      await apiClient.post('/auth/register', { email, password });
      alert('Registration successful! Please login.');
      toggleForm();
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail[0].msg);
      } else {
        setError(detail || 'Registration failed.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card fade-in">
      <div className="auth-header">
        <LogIn size={40} className="auth-icon" />
        <h2>Create Account</h2>
        <p>Start your personalized support journey</p>
      </div>
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="input-group">
          <Mail size={18} />
          <input 
            type="email" 
            placeholder="Email Address" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div className="input-group">
          <Lock size={18} />
          <input 
            type="password" 
            placeholder="Password (min 8 chars)" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        
        {error && <p className="auth-error">{error}</p>}
        
        <button type="submit" disabled={loading} className="auth-btn">
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      
      <p className="auth-footer">
        Already have an account? <span onClick={toggleForm}>Login here</span>
      </p>
    </div>
  );
};
