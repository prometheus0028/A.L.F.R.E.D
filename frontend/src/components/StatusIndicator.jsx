import React from 'react';

const StatusIndicator = ({ status }) => {
  const getStatusConfig = () => {
    switch(status) {
      case 'created':
      case 'planning':
      case 'executing':
      case 'verifying':
        return { color: 'text-accent', bg: 'bg-accent/10', label: 'Active' };
      case 'waiting_approval':
      case 'replanning':
        return { color: 'text-status-warning', bg: 'bg-status-warning/10', label: 'Action Needed' };
      case 'completed':
        return { color: 'text-status-success', bg: 'bg-status-success/10', label: 'Completed' };
      case 'failed':
        return { color: 'text-status-error', bg: 'bg-status-error/10', label: 'Failed' };
      case 'paused':
        return { color: 'text-text-muted', bg: 'bg-surface-tertiary', label: 'Paused' };
      default:
        return { color: 'text-text-secondary', bg: 'bg-surface-secondary', label: status || 'Unknown' };
    }
  };

  const config = getStatusConfig();

  return (
    <span className={`px-2 py-1 text-xs font-medium uppercase rounded-sm ${config.color} ${config.bg}`}>
      {config.label}
    </span>
  );
};

export default StatusIndicator;
