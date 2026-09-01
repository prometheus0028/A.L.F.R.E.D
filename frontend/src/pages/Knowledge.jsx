import React, { useState, useEffect } from 'react';
import { getFiles } from '../services/api';
import { useUpload } from '../hooks/useUpload';

const Knowledge = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const { isUploading, uploadStatus, fileInputRef, triggerUpload, handleFileChange } = useUpload(() => {
    fetchFiles();
  });

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const data = await getFiles();
      if (data && data.items) {
        setFiles(data.items);
      }
    } catch (error) {
      console.error("Failed to fetch files", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">KNOWLEDGE / 05</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold tracking-tight uppercase">DOCUMENT REPOSITORY</h1>
          
          <div className="flex items-center gap-4">
            {uploadStatus.status !== 'IDLE' && (
              <span className={`font-mono text-[10px] tracking-widest uppercase ${
                uploadStatus.status === 'ERROR' ? 'text-status-error' : 'text-accent-amber'
              }`}>
                &gt; {uploadStatus.message}
              </span>
            )}
            <button 
              onClick={triggerUpload}
              disabled={isUploading}
              className="border border-border bg-surface-secondary text-text-primary hover:bg-border transition-colors px-4 py-1.5 font-mono text-xs tracking-widest uppercase disabled:opacity-50"
            >
              + ADD FILE
            </button>
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              className="hidden" 
            />
          </div>
        </div>
        
        {loading ? (
          <div className="font-mono text-sm text-text-muted uppercase">LOADING REPOSITORY...</div>
        ) : files.length === 0 ? (
          <div className="font-mono text-sm text-text-muted uppercase">REPOSITORY EMPTY.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {files.map((doc, idx) => (
              <div key={idx} className="border border-border p-4 hover:border-text-muted transition-colors cursor-pointer group bg-surface-secondary/20">
                <div className="font-mono text-[10px] tracking-widest text-text-muted mb-2 uppercase">{doc.type || 'DOCUMENT'}</div>
              <div className="font-mono text-sm text-text-primary mb-4 truncate group-hover:text-accent transition-colors" title={doc.name}>{doc.name}</div>
              <div className="flex justify-between items-center">
                <span className="font-mono text-xs text-text-secondary">{formatSize(doc.size)}</span>
                <span 
                  onClick={() => window.open(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/files/${doc.name}`, '_blank')}
                  className="font-mono text-[10px] tracking-widest text-text-primary uppercase border border-border px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  VIEW
                </span>
              </div>
            </div>
          ))}
        </div>
        )}
      </div>
    </div>
  );
};

export default Knowledge;
