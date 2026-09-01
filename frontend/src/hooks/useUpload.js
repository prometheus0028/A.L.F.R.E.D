import { useState, useRef } from 'react';
import { uploadFile } from '../services/api';

export const useUpload = (onSuccess) => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({ status: 'IDLE', file: null, message: null });
  const fileInputRef = useRef(null);

  const triggerUpload = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setUploadStatus({ status: 'UPLOADING', file: file.name, message: `UPLOADING...` });

    try {
      const response = await uploadFile(file);
      if (response && response.success) {
        setUploadStatus({ status: 'SUCCESS', file: file.name, message: `FILE ADDED` });
        if (onSuccess) {
          onSuccess(response.file);
        }
        // Auto-clear success message after 5 seconds
        setTimeout(() => {
          setUploadStatus(prev => prev.status === 'SUCCESS' ? { status: 'IDLE', file: null, message: null } : prev);
        }, 5000);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error("Upload error:", error);
      setUploadStatus({ 
        status: 'ERROR', 
        file: file.name, 
        message: error.response?.data?.detail?.error || 'UPLOAD FAILED' 
      });
    } finally {
      setIsUploading(false);
      // Reset input so the same file can be selected again
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return {
    isUploading,
    uploadStatus,
    fileInputRef,
    triggerUpload,
    handleFileChange
  };
};
