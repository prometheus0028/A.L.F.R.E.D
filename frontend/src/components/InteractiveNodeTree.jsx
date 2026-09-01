import React from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';

const DraggableNode = ({ label, desc, angle, distance, sizeClass }) => {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  
  // Convert angle to radians and calculate base position relative to center
  const rad = (angle * Math.PI) / 180;
  const baseX = Math.cos(rad) * distance;
  const baseY = Math.sin(rad) * distance;

  return (
    <>
      {/* Dynamic SVG Line */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none z-0" viewBox="-300 -300 600 600" style={{ overflow: 'visible' }}>
        <motion.line 
          x1={0} 
          y1={0} 
          x2={useTransform(x, (latest) => baseX + latest)}
          y2={useTransform(y, (latest) => baseY + latest)}
          stroke="rgba(255,255,255,0.15)" 
          strokeWidth={1}
        />
      </svg>

      {/* Draggable Node Wrapper (Handles centering and base position) */}
      <div 
        className="absolute top-1/2 left-1/2 z-10"
        style={{ transform: `translate(calc(-50% + ${baseX}px), calc(-50% + ${baseY}px))` }}
      >
        <motion.div
          drag
          dragSnapToOrigin
          dragElastic={0.4}
          dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
          style={{ x, y }}
          whileHover={{ scale: 1.05 }}
          whileDrag={{ scale: 1.05, zIndex: 50 }}
          className={`border border-border/50 bg-[#060807] p-4 cursor-grab active:cursor-grabbing backdrop-blur-sm ${sizeClass}`}
        >
          <div className="text-xs font-mono tracking-widest text-[#5ca833] mb-2 uppercase">{label}</div>
          <div className="text-[10px] text-text-muted">{desc}</div>
        </motion.div>
      </div>
    </>
  );
};

const InteractiveNodeTree = () => {
  const nodes = [
    { label: 'PLAN', desc: 'Determines steps.', angle: -90, distance: 180, sizeClass: 'w-36 h-20' },
    { label: 'ACT', desc: 'Executes tools.', angle: -18, distance: 220, sizeClass: 'w-32 h-20' },
    { label: 'VERIFY', desc: 'Validates results.', angle: 54, distance: 200, sizeClass: 'w-36 h-20' },
    { label: 'OBSERVE', desc: 'Learns from results.', angle: 126, distance: 190, sizeClass: 'w-32 h-24' },
    { label: 'ADAPT', desc: 'Replans on failure.', angle: 198, distance: 210, sizeClass: 'w-32 h-20' }
  ];

  return (
    <div className="relative w-full h-[600px] flex items-center justify-center">
      {/* Background faint circle as seen in reference */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-white/5 rounded-full pointer-events-none" />

      {/* Center ALFRED Node */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-28 h-28 bg-[#060807] border border-border/50 flex items-center justify-center z-20 shadow-2xl">
        <span className="font-mono tracking-widest text-sm text-text-primary uppercase font-bold">ALFRED</span>
      </div>

      {/* Surrounding Interactive Nodes */}
      {nodes.map(node => (
        <DraggableNode key={node.label} {...node} />
      ))}
    </div>
  );
};

export default InteractiveNodeTree;
