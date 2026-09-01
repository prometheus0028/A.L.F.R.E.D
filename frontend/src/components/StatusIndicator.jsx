import React from 'react';
import { motion } from 'framer-motion';

const StatusIndicator = ({ status }) => {
  const getStatusConfig = () => {
    switch(status) {
      case 'created':
      case 'planning':
      case 'executing':
      case 'verifying':
      case 'running': // Added based on ui
        return { color: 'bg-text-primary', blink: true };
      case 'waiting_approval':
      case 'replanning':
        return { color: 'bg-accent-amber', blink: true };
      case 'completed':
        return { color: 'bg-status-success', blink: false };
      case 'failed':
        return { color: 'bg-status-error', blink: false };
      case 'paused':
        return { color: 'bg-text-muted', blink: false };
      default:
        return { color: 'bg-text-secondary', blink: false };
    }
  };

  const config = getStatusConfig();

  return (
    <motion.span 
      className={`inline-block w-2.5 h-2.5 rounded-full ${config.color}`}
      animate={config.blink ? { opacity: [1, 0.4, 1] } : {}}
      transition={config.blink ? { duration: 1.5, repeat: Infinity, ease: "linear" } : {}}
    />
  );
};

export default StatusIndicator;
