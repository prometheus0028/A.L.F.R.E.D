import React from 'react';
import { motion } from 'framer-motion';

const TunnelBackground = ({ subtle = false }) => {
  const numRings = 8;
  const numLines = 12;

  // Reduced opacity if we want it subtle on dashboard/execution
  const opacityClass = subtle ? 'opacity-10' : 'opacity-40';

  return (
    <div className={`fixed inset-0 pointer-events-none flex items-center justify-center overflow-hidden bg-surface-primary ${opacityClass} transition-opacity duration-1000`}>
      <motion.svg
        viewBox="-500 -500 1000 1000"
        className="w-[150vw] h-[150vh] max-w-none max-h-none opacity-60"
        initial={{ rotate: 0 }}
        animate={{ rotate: 360 }}
        transition={{ duration: 200, repeat: Infinity, ease: "linear" }}
      >
        <g stroke="#1c2420" strokeWidth="1" fill="none">
          {/* Concentric rings */}
          {Array.from({ length: numRings }).map((_, i) => (
            <motion.circle
              key={`ring-${i}`}
              cx="0"
              cy="0"
              r={50 + i * 80}
              strokeDasharray={i % 2 === 0 ? '4 8' : 'none'}
              initial={{ scale: 0.95 }}
              animate={{ scale: 1.05 }}
              transition={{
                duration: 10 + i * 2,
                repeat: Infinity,
                repeatType: 'reverse',
                ease: 'easeInOut',
              }}
            />
          ))}

          {/* Radial lines */}
          {Array.from({ length: numLines }).map((_, i) => {
            const angle = (i * 360) / numLines;
            return (
              <line
                key={`line-${i}`}
                x1="0"
                y1="0"
                x2="1000"
                y2="0"
                transform={`rotate(${angle})`}
                strokeDasharray="2 12"
              />
            );
          })}
        </g>
        
        {/* Nodes */}
        <g fill="#111613" stroke="#1c2420" strokeWidth="1">
          {Array.from({ length: numRings }).map((_, i) => {
            const r = 50 + i * 80;
            return Array.from({ length: 4 }).map((_, j) => {
              const angle = (j * 90) + (i * 15);
              const x = r * Math.cos((angle * Math.PI) / 180);
              const y = r * Math.sin((angle * Math.PI) / 180);
              return (
                <motion.circle
                  key={`node-${i}-${j}`}
                  cx={x}
                  cy={y}
                  r="3"
                  initial={{ opacity: 0.2 }}
                  animate={{ opacity: [0.2, 0.8, 0.2] }}
                  transition={{
                    duration: 3 + Math.random() * 4,
                    repeat: Infinity,
                    delay: Math.random() * 2,
                  }}
                />
              );
            });
          })}
        </g>
      </motion.svg>
    </div>
  );
};

export default TunnelBackground;
