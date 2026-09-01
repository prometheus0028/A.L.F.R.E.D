import React, { useState, useRef } from 'react';
import { useUpload } from '../hooks/useUpload';

const GoalInput = ({ onStartTask, isExecuting, audioEnabled, setAudioEnabled }) => {
  const [goal, setGoal] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  const { isUploading, uploadStatus, fileInputRef, triggerUpload, handleFileChange } = useUpload();

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder.current = new MediaRecorder(stream);
      audioChunks.current = [];
      
      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };
      
      mediaRecorder.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.webm');
        
        try {
          const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
          const response = await fetch(`${baseUrl}/api/speech/transcribe`, {
            method: 'POST',
            body: formData,
          });
          if (response.ok) {
            const data = await response.json();
            if (data.text) {
              setGoal(prev => (prev + " " + data.text).trim());
            }
          }
        } catch (error) {
          console.error("Transcription failed", error);
        }
        
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Failed to access microphone", error);
    }
  };
  
  const handleStopRecording = () => {
    if (mediaRecorder.current && isRecording) {
      mediaRecorder.current.stop();
      setIsRecording(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (goal.trim() && !isExecuting) {
      onStartTask(goal);
      setGoal("");
    }
  };

  return (
    <div>
      <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">What should ALFRED accomplish today?</div>
      
      <form onSubmit={handleSubmit} className="flex gap-4 items-stretch max-w-3xl">
        <div className="flex-1 flex items-center border border-border bg-surface-secondary relative font-mono">
          <span className="text-text-muted px-4 select-none">&gt;</span>
          <input 
            type="text"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
            placeholder="e.g. Prepare me for tomorrow's meeting with Rahul"
            disabled={isExecuting}
            className="flex-1 bg-transparent py-3 pr-4 text-text-primary text-sm focus:outline-none disabled:opacity-50"
          />
          <button
            type="button"
            onMouseDown={handleStartRecording}
            onMouseUp={handleStopRecording}
            onMouseLeave={handleStopRecording}
            className={`px-4 text-xl ${isRecording ? 'text-status-error' : 'text-text-muted hover:text-text-primary'} transition-colors`}
            title="Hold to speak"
          >
            🎤
          </button>
          <button
            type="button"
            onClick={() => setAudioEnabled(!audioEnabled)}
            className={`px-4 text-xl ${audioEnabled ? 'text-accent-amber' : 'text-text-muted hover:text-text-primary'} border-l border-border transition-colors`}
            title={audioEnabled ? "Disable Voice Output" : "Enable Voice Output"}
          >
            {audioEnabled ? "🔊" : "🔈"}
          </button>
          <button
            type="button"
            onClick={triggerUpload}
            disabled={isUploading}
            className={`px-4 text-xl font-mono border-l border-border transition-colors ${isUploading ? 'text-accent-amber opacity-50' : 'text-text-muted hover:text-text-primary'}`}
            title="Upload File"
          >
            +
          </button>
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            className="hidden" 
          />
        </div>
        
        <button 
          type="submit"
          disabled={!goal.trim() || isExecuting}
          className="flex items-center justify-center gap-2 bg-surface-secondary border border-border text-text-primary px-8 text-sm font-mono tracking-widest hover:bg-text-primary hover:text-surface-primary disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          &gt; RUN
        </button>
      </form>

      {uploadStatus.status !== 'IDLE' && (
        <div className={`mt-2 font-mono text-[10px] tracking-widest uppercase ${
          uploadStatus.status === 'ERROR' ? 'text-status-error' : 'text-accent-amber'
        }`}>
          &gt; {uploadStatus.message} {uploadStatus.file ? `- ${uploadStatus.file}` : ''}
        </div>
      )}
      
      <div className="mt-8">
        <div className="text-[10px] font-mono tracking-widest text-text-muted mb-4 uppercase">Try these:</div>
        <div className="flex gap-4">
          <button onClick={() => setGoal("Prepare me for tomorrow's meeting with Rahul")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            PREPARE MEETING
          </button>
          <button onClick={() => setGoal("Handle the pending invoice")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            HANDLE PENDING INVOICE
          </button>
          <button onClick={() => setGoal("Summarize project updates from last week")} className="px-4 py-1.5 border border-border text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:border-text-secondary transition-colors">
            PROJECT UPDATE
          </button>
        </div>
      </div>
    </div>
  );
};

export default GoalInput;
