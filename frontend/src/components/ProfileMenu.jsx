import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { Link } from 'react-router-dom';

const ProfileMenu = () => {
  const { user, services, logout } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) return null;

  return (
    <div className="relative z-50">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-3 hover:bg-surface-secondary/50 p-2 border border-transparent hover:border-border transition-colors outline-none focus:outline-none"
      >
        <img 
          src={user.picture} 
          alt={user.name} 
          className="w-8 h-8 rounded-full border border-border"
          referrerPolicy="no-referrer"
        />
        <div className="hidden md:flex flex-col items-start">
          <span className="text-xs font-mono font-bold tracking-widest uppercase">{user.name}</span>
          <span className="text-[10px] text-text-muted font-mono tracking-widest">{user.email}</span>
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-surface-primary border border-border shadow-lg">
          <div className="py-1">
            <Link 
              to="/dashboard"
              className="block px-4 py-2 text-xs font-mono tracking-widest text-text-secondary hover:text-text-primary hover:bg-surface-secondary uppercase"
            >
              Dashboard
            </Link>

            {services && (
              <div className="border-t border-b border-border my-1 py-1">
                <div className="px-4 py-1 text-[10px] text-text-muted font-mono tracking-widest uppercase mb-1">Services</div>
                {Object.entries(services).map(([service, isConnected]) => (
                  <div key={service} className="px-4 py-1 flex justify-between items-center text-[10px] font-mono uppercase tracking-widest">
                    <span className="text-text-secondary capitalize">{service}</span>
                    <span className={isConnected ? "text-accent" : "text-text-muted opacity-50"}>
                      {isConnected ? "CONNECTED" : "OFF"}
                    </span>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={() => {
                setIsOpen(false);
                logout();
              }}
              className="w-full text-left block px-4 py-2 text-xs font-mono tracking-widest text-status-error hover:bg-surface-secondary uppercase"
            >
              Disconnect Google
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileMenu;
