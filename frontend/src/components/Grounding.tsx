import React, { useState, useEffect } from 'react';
import { Wind, Play, Square, RefreshCcw } from 'lucide-react';

export const BreathingExercise: React.FC = () => {
  const [isActive, setIsListening] = useState(false);
  const [phase, setPhase] = useState<'Inhale' | 'Hold' | 'Exhale' | 'Rest'>('Inhale');
  const [seconds, setSeconds] = useState(4);

  useEffect(() => {
    let interval: any;
    if (isActive) {
      interval = setInterval(() => {
        setSeconds((prev) => {
          if (prev <= 1) {
            // Cycle through Box Breathing (4-4-4-4)
            if (phase === 'Inhale') { setPhase('Hold'); return 4; }
            if (phase === 'Hold') { setPhase('Exhale'); return 4; }
            if (phase === 'Exhale') { setPhase('Rest'); return 4; }
            if (phase === 'Rest') { setPhase('Inhale'); return 4; }
            return 4;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      setPhase('Inhale');
      setSeconds(4);
    }
    return () => clearInterval(interval);
  }, [isActive, phase]);

  const toggle = () => setIsListening(!isActive);

  return (
    <div className="grounding-card fade-in">
      <div className="grounding-header">
        <Wind className="stat-icon blue" />
        <h3>Grounding Exercise</h3>
        <p>Follow the rhythm to calm your nervous system (Box Breathing)</p>
      </div>

      <div className="breathing-circle-container">
        <div className={`breathing-circle ${isActive ? phase.toLowerCase() : ''}`}>
          <div className="breathing-inner">
            <span className="phase-text">{phase}</span>
            <span className="seconds-text">{seconds}s</span>
          </div>
        </div>
      </div>

      <div className="grounding-controls">
        <button onClick={toggle} className={`action-btn ${isActive ? 'stop' : 'start'}`}>
          {isActive ? <><Square size={18} /> Stop</> : <><Play size={18} /> Start Session</>}
        </button>
        <button onClick={() => {setIsListening(false); setSeconds(4);}} className="secondary-btn">
          <RefreshCcw size={18} /> Reset
        </button>
      </div>
    </div>
  );
};
