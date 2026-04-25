import React, { useState, useEffect } from 'react';
import apiClient from '../api/client';
import { useAuth } from '../context/AuthContext';
import { User, MapPin, FileText, Camera, Save, CheckCircle, Mail, Phone, Users } from 'lucide-react';

export const Profile: React.FC = () => {
  const { userEmail } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  
  // Form State
  const [fullName, setFullName] = useState('');
  const [location, setLocation] = useState('');
  const [phone, setPhone] = useState('');
  const [gender, setGender] = useState('');
  const [bio, setBio] = useState('');
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    void fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await apiClient.get('/users/me');
      setFullName(res.data.full_name || '');
      setLocation(res.data.location || '');
      setPhone(res.data.phone_number || '');
      setGender(res.data.gender || '');
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

    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result as string);
    reader.readAsDataURL(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
      await apiClient.post('/users/me/photo', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
    } catch (err) {
      alert("Failed to upload photo.");
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await apiClient.patch('/users/me', {
        full_name: fullName,
        location: location,
        phone_number: phone,
        gender: gender,
        bio: bio
      });
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
          <h3>{fullName || "Add Your Name"}</h3>
          <p className="profile-email-badge">{userEmail}</p>
        </div>

        <form onSubmit={handleUpdate} className="profile-form">
          <div className="form-grid">
            {/* Full Name */}
            <div className="input-field">
              <label>Full Name</label>
              <div className="input-group">
                <User size={18} className="field-icon" />
                <input 
                  type="text" 
                  value={fullName} 
                  onChange={(e) => setFullName(e.target.value)} 
                  placeholder="e.g. Aarav Sharma" 
                />
              </div>
            </div>

            {/* Location */}
            <div className="input-field">
              <label>Location</label>
              <div className="input-group">
                <MapPin size={18} className="field-icon" />
                <input 
                  type="text" 
                  value={location} 
                  onChange={(e) => setLocation(e.target.value)} 
                  placeholder="e.g. Mumbai, Maharashtra" 
                />
              </div>
            </div>

            {/* Gender Selection */}
            <div className="input-field">
              <label>Gender</label>
              <div className="input-group">
                <Users size={18} className="field-icon" />
                <select 
                  value={gender} 
                  onChange={(e) => setGender(e.target.value)}
                  className="select-field"
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                  <option value="prefer not to say">Prefer not to say</option>
                </select>
              </div>
            </div>

            {/* Phone Number */}
            <div className="input-field">
              <label>Phone Number</label>
              <div className="input-group">
                <Phone size={18} className="field-icon" />
                <input 
                  type="tel" 
                  value={phone} 
                  onChange={(e) => setPhone(e.target.value)} 
                  placeholder="e.g. +91 98765 43210" 
                />
              </div>
            </div>

            {/* Email (Read Only) */}
            <div className="input-field full-width">
              <label>Email Address (Account ID)</label>
              <div className="input-group disabled">
                <Mail size={18} className="field-icon" />
                <input 
                  type="email" 
                  value={userEmail || ''} 
                  readOnly 
                />
              </div>
            </div>

            {/* Bio */}
            <div className="input-field full-width">
              <label>Bio</label>
              <div className="input-group text-area-group">
                <FileText size={18} className="field-icon top" />
                <textarea 
                  value={bio} 
                  onChange={(e) => setBio(e.target.value)} 
                  placeholder="Share a bit about your journey..."
                  rows={4}
                />
              </div>
            </div>
          </div>

          <div className="profile-actions">
            <button type="submit" disabled={saving} className={`save-btn ${success ? 'success' : ''}`}>
              {saving ? <span className="spinner-small"></span> : (
                success ? <><CheckCircle size={18} /> Saved Successfully</> : <><Save size={18} /> Update Profile</>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
