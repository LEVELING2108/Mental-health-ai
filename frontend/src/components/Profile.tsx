import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import { User, MapPin, FileText, Camera, Save, CheckCircle } from 'lucide-react';

export const Profile: React.FC = () => {
  const { userEmail } = useAuth();
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  
  // Form State
  const [fullName, setFullName] = useState('');
  const [location, setLocation] = useState('');
  const [bio, setBio] = useState('');
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await apiClient.get('/users/me');
      setProfile(res.data);
      setFullName(res.data.full_name || '');
      setLocation(res.data.location || '');
      setBio(res.data.bio || '');
      if (res.data.profile_image) {
        const baseUrl = import.meta.env.VITE_API_BASE_URL.replace('/api/v1', '');
        setPreview(`${baseUrl}/${res.data.profile_image}`);
      }
    } catch (err) {
      console.error("Failed to fetch profile", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePhotoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Show preview
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result as string);
    reader.readAsDataURL(file);

    // Upload to server
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await apiClient.post('/users/me/photo', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setProfile(res.data);
    } catch (err) {
      alert("Failed to upload photo.");
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await apiClient.patch('/users/me', {
        full_name: fullName,
        location: location,
        bio: bio
      });
      setProfile(res.data);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      alert("Failed to update profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="spinner-container"><div className="spinner"></div></div>;

  return (
    <div className="profile-container fade-in">
      <div className="profile-card">
        <div className="profile-photo-section">
          <div className="photo-wrapper">
            {preview ? (
              <img src={preview} alt="Profile" className="profile-img" />
            ) : (
              <div className="photo-placeholder"><User size={64} /></div>
            )}
            <label className="photo-upload-btn">
              <Camera size={18} />
              <input type="file" hidden accept="image/*" onChange={handlePhotoUpload} />
            </label>
          </div>
          <h3>{fullName || userEmail?.split('@')[0]}</h3>
          <p className="profile-email">{userEmail}</p>
        </div>

        <form onSubmit={handleUpdate} className="profile-form">
          <div className="form-grid">
            <div className="input-field">
              <label>Full Name</label>
              <div className="input-group">
                <User size={18} className="field-icon" />
                <input 
                  type="text" 
                  value={fullName} 
                  onChange={(e) => setFullName(e.target.value)} 
                  placeholder="John Doe" 
                />
              </div>
            </div>

            <div className="input-field">
              <label>Location</label>
              <div className="input-group">
                <MapPin size={18} className="field-icon" />
                <input 
                  type="text" 
                  value={location} 
                  onChange={(e) => setLocation(e.target.value)} 
                  placeholder="New York, USA" 
                />
              </div>
            </div>

            <div className="input-field full-width">
              <label>Bio</label>
              <div className="input-group text-area-group">
                <FileText size={18} className="field-icon top" />
                <textarea 
                  value={bio} 
                  onChange={(e) => setBio(e.target.value)} 
                  placeholder="Tell us a bit about yourself..."
                  rows={4}
                />
              </div>
            </div>
          </div>

          <div className="profile-actions">
            <button type="submit" disabled={saving} className={`save-btn ${success ? 'success' : ''}`}>
              {saving ? <span className="spinner-small"></span> : (
                success ? <><CheckCircle size={18} /> Saved!</> : <><Save size={18} /> Save Changes</>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
