import React, { useEffect, useState } from 'react';
import { 
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  AreaChart, Area, BarChart, Bar, Cell 
} from 'recharts';
import apiClient from '../api/client';
import { Brain, ShieldAlert, History } from 'lucide-react';

interface MoodLog {
  id: string;
  risk_level: string;
  confidence_score: number;
  emotion: string;
  created_at: string;
}

const RISK_MAP: { [key: string]: number } = { low: 1, medium: 2, high: 3 };
const EMOTION_COLORS: { [key: string]: string } = {
  joy: '#10b981',
  sadness: '#3b82f6',
  fear: '#f59e0b',
  anger: '#ef4444',
  surprise: '#8b5cf6',
  love: '#ec4899'
};

export const Dashboard: React.FC = () => {
  const [logs, setLogs] = useState<MoodLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await apiClient.get('/moods/');
        setLogs(response.data.reverse()); // Show oldest to newest for chart
      } catch (err) {
        console.error('Failed to fetch mood history', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const chartData = logs.map(log => ({
    date: new Date(log.created_at).toLocaleDateString(),
    risk: RISK_MAP[log.risk_level.toLowerCase()] || 0,
    confidence: log.confidence_score * 100,
    emotion: log.emotion
  }));

  const emotionCounts = logs.reduce((acc: any, log) => {
    const e = log.emotion.toLowerCase();
    acc[e] = (acc[e] || 0) + 1;
    return acc;
  }, {});

  const barData = Object.keys(emotionCounts).map(name => ({
    name: name.toUpperCase(),
    value: emotionCounts[name]
  }));

  if (loading) return <div className="spinner-container"><div className="spinner"></div></div>;

  return (
    <div className="dashboard-container fade-in">
      <div className="stats-grid">
        <div className="stat-card">
          <History className="stat-icon blue" />
          <div className="stat-content">
            <span className="stat-label">Total Entries</span>
            <span className="stat-value">{logs.length}</span>
          </div>
        </div>
        <div className="stat-card">
          <Brain className="stat-icon green" />
          <div className="stat-content">
            <span className="stat-label">Common Emotion</span>
            <span className="stat-value">
              {barData.length > 0 ? barData.reduce((a, b) => a.value > b.value ? a : b).name : 'N/A'}
            </span>
          </div>
        </div>
        <div className="stat-card">
          <ShieldAlert className="stat-icon red" />
          <div className="stat-content">
            <span className="stat-label">Recent Risk</span>
            <span className="stat-value">
              {logs.length > 0 ? logs[logs.length-1].risk_level.toUpperCase() : 'N/A'}
            </span>
          </div>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-wrapper">
          <h3>Mental Health Risk Trend</h3>
          <p className="chart-sub">1: Low, 2: Medium, 3: High</p>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="date" />
                <YAxis ticks={[1, 2, 3]} domain={[0, 4]} />
                <Tooltip />
                <Area type="monotone" dataKey="risk" stroke="#3b82f6" fillOpacity={1} fill="url(#colorRisk)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="chart-wrapper">
          <h3>Emotional Distribution</h3>
          <p className="chart-sub">Frequency of detected emotions</p>
          <div style={{ width: '100%', height: 300 }}>
            <ResponsiveContainer>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value">
                  {barData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={EMOTION_COLORS[entry.name.toLowerCase()] || '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
