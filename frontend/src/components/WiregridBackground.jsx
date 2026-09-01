import React, { useEffect, useRef } from 'react';

const WiregridBackground = ({ intensity = 'medium' }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    let width = window.innerWidth;
    let height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;

    // Handle Resize
    const handleResize = () => {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;
    };
    window.addEventListener('resize', handleResize);

    // Prefers reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Intensity Opacity
    let baseOpacity = 0.4;
    if (intensity === 'high') baseOpacity = 0.8;
    if (intensity === 'low') baseOpacity = 0.15;
    
    let time = 0;
    let animationFrameId;

    // Grid configuration
    const gridSize = 40; // Number of steps in X and Z
    const rangeX = 3000;
    const rangeZ = 2000;
    
    // Wave parameters (more dramatic hills for new reference)
    const waves = [
      { fX: 0.0015, fZ: 0.002, speed: 0.005, amp: 250 },
      { fX: 0.003, fZ: 0.0015, speed: 0.003, amp: 120 },
      { fX: 0.001, fZ: 0.004, speed: -0.004, amp: 80 }
    ];

    const getElevation = (x, z, t) => {
      let y = 0;
      for (const wave of waves) {
        y += Math.sin(x * wave.fX + z * wave.fZ + t * wave.speed) * wave.amp;
      }
      return y;
    };

    const project = (x, y, z) => {
      // Perspective projection
      const fov = 400; // Field of view equivalent scale
      const zOffset = 300; // Camera distance offset
      const zScale = fov / (z + zOffset);
      
      const px = width / 2 + x * zScale;
      // Tilt camera slightly down by adjusting Y offset based on Z
      const py = height / 2 + (y + 150) * zScale + (z * 0.15); 
      
      return { px, py, zScale };
    };

    const render = () => {
      ctx.clearRect(0, 0, width, height);
      
      // Calculate vertices
      const vertices = [];
      const stepsX = gridSize;
      const stepsZ = gridSize;
      
      const stepSizeX = (rangeX * 2) / stepsX;
      const stepSizeZ = rangeZ / stepsZ;

      // Build 2D array of projected points
      for (let zi = 0; zi <= stepsZ; zi++) {
        const row = [];
        for (let xi = 0; xi <= stepsX; xi++) {
          const x = -rangeX + xi * stepSizeX;
          const z = zi * stepSizeZ;
          const y = getElevation(x, z, time);
          
          const p = project(x, y, z);
          row.push({ ...p, origZ: z });
        }
        vertices.push(row);
      }

      ctx.lineWidth = 1;
      // Draw grid
      for (let zi = 0; zi < stepsZ; zi++) {
        for (let xi = 0; xi < stepsX; xi++) {
          const v00 = vertices[zi][xi];
          const v10 = vertices[zi][xi + 1];
          const v01 = vertices[zi + 1][xi];
          const v11 = vertices[zi + 1][xi + 1];

          // Fade out based on distance
          const depthAlpha = Math.max(0, 1 - (v00.origZ / rangeZ));
          // Fade edges horizontally to prevent harsh cutoffs
          const edgeFade = 1 - Math.pow(Math.abs((xi / stepsX) * 2 - 1), 3);
          
          const finalAlpha = depthAlpha * edgeFade * baseOpacity;
          if (finalAlpha <= 0.01) continue;

          // Draw lines
          ctx.strokeStyle = `rgba(180, 190, 185, ${finalAlpha * 0.5})`; // Slightly brighter line
          ctx.beginPath();
          ctx.moveTo(v00.px, v00.py);
          ctx.lineTo(v10.px, v10.py);
          ctx.moveTo(v00.px, v00.py);
          ctx.lineTo(v01.px, v01.py);
          ctx.stroke();

          // Draw vertex dot
          const dotSize = Math.max(0.5, 2 * v00.zScale);
          ctx.fillStyle = `rgba(255, 255, 255, ${finalAlpha * 0.9})`; 
          ctx.beginPath();
          ctx.arc(v00.px, v00.py, dotSize, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      // Advance time
      if (!prefersReducedMotion) {
        time += 1;
      } else {
        time += 0.05; // Almost static
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [intensity]);

  return (
    <div className="fixed inset-0 pointer-events-none bg-surface-primary z-0">
      <canvas 
        ref={canvasRef} 
        className="block w-full h-full"
        style={{ opacity: intensity === 'high' ? 1 : 0.6 }}
      />
    </div>
  );
};

export default WiregridBackground;
