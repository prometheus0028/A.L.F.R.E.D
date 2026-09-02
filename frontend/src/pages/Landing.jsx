import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import WiregridBackground from '../components/WiregridBackground';
import InteractiveNodeTree from '../components/InteractiveNodeTree';
import { useAuth } from '../hooks/useAuth';

// We'll create a reusable ProfileMenu component to place in the header
import ProfileMenu from '../components/ProfileMenu';
const Landing = () => {
  const { isAuthenticated, isLoading } = useAuth();
  
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  const loginUrl = `${baseUrl}/auth/google/login`;

  return (
    <div className="min-h-screen bg-transparent text-text-primary overflow-hidden relative flex flex-col font-sans">
      <WiregridBackground intensity="high" />

      {/* Top Navigation */}
      <header className="relative z-50 border-b border-border h-16 flex items-center px-8 justify-between bg-surface-primary/80">
        <div className="font-mono text-lg font-bold tracking-widest text-text-primary">
          ALFRED_
        </div>
        
        <nav className="hidden md:flex items-center gap-8 text-xs font-mono tracking-widest text-text-secondary">
          <a href="#" className="hover:text-text-primary transition-colors">PRODUCT</a>
          <a href="#" className="hover:text-text-primary transition-colors">CAPABILITIES</a>
          <a href="#" className="hover:text-text-primary transition-colors">HOW IT WORKS</a>
          <a href="#" className="hover:text-text-primary transition-colors">SECURITY</a>
          <a href="#" className="hover:text-text-primary transition-colors">DOCS</a>
        </nav>

        {!isLoading && (
          isAuthenticated ? (
            <ProfileMenu />
          ) : (
            <a 
              href={loginUrl}
              className="border border-border px-6 py-3 text-xs font-mono tracking-widest hover:bg-text-primary hover:text-surface-primary transition-colors flex items-center gap-2"
            >
              LOGIN WITH GOOGLE
            </a>
          )
        )}
      </header>

      {/* Main Content */}
      <main className="relative z-10 flex-1 flex flex-col md:flex-row items-center px-12 md:px-24 py-16 md:py-24 max-w-7xl mx-auto w-full gap-16">
        
        {/* Left Side: Typography & CTA */}
        <div className="flex-1 flex flex-col justify-center space-y-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="space-y-4"
          >
            <div className="text-xs font-mono tracking-widest text-text-secondary border-b border-border pb-2 inline-block">
              AUTONOMOUS EXECUTION SYSTEM / 01
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold leading-[1.1] tracking-tight text-text-primary">
              GIVE ALFRED<br />
              A GOAL.<br />
              <span className="text-text-muted">LET IT HANDLE<br />THE WORK.</span>
            </h1>
          </motion.div>

          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-text-secondary text-lg max-w-md"
          >
            An autonomous agent that plans, acts, adapts, and verifies outcomes across your digital workspace.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex items-center gap-4 pt-4"
          >
            {!isLoading && (
              isAuthenticated ? (
                <Link 
                  to="/dashboard"
                  className="bg-accent text-surface-primary px-8 py-4 text-sm font-mono tracking-widest hover:bg-accent-hover transition-colors inline-flex items-center gap-2 leading-none"
                >
                  LAUNCH ALFRED_ <span className="opacity-50">→</span>
                </Link>
              ) : (
                <a 
                  href={loginUrl}
                  className="bg-accent text-surface-primary px-8 py-4 text-sm font-mono tracking-widest hover:bg-accent-hover transition-colors inline-flex items-center gap-2 leading-none"
                >
                  LAUNCH ALFRED_ <span className="opacity-50">→</span>
                </a>
              )
            )}
            <a 
              href="#how-it-works"
              onClick={(e) => { 
                e.preventDefault(); 
                document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' }); 
              }}
              className="border border-border px-8 py-4 text-sm font-mono tracking-widest hover:bg-surface-secondary transition-colors text-text-secondary leading-none"
            >
              SEE HOW IT WORKS
            </a>
          </motion.div>
        </div>

        {/* Right Side: Interactive Node Tree */}
        <div className="flex-1 flex items-center justify-center relative min-h-[500px]">
          <motion.div 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            className="w-full"
          >
            <InteractiveNodeTree />
          </motion.div>
        </div>

      </main>

      {/* How it Works Section */}
      <section id="how-it-works" className="relative z-10 border-t border-border bg-surface-primary/95 py-32 px-8">
        <div className="max-w-7xl mx-auto w-full">
          <div className="text-xs font-mono tracking-widest text-text-secondary mb-16 border-b border-border pb-4 uppercase">
            HOW ALFRED WORKS
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-16">
            {[
              { num: '01', title: 'GOAL', desc: 'You describe the outcome you want.' },
              { num: '02', title: 'PLAN', desc: 'ALFRED determines the steps required.' },
              { num: '03', title: 'ACT', desc: 'It uses the available tools.' },
              { num: '04', title: 'OBSERVE', desc: 'It evaluates the results.' },
              { num: '05', title: 'ADAPT', desc: 'If an action fails or information is missing, ALFRED can replan.' },
              { num: '06', title: 'VERIFY', desc: 'ALFRED checks whether the intended outcome was achieved.' }
            ].map((step, i) => (
              <div key={step.num} className="relative group">
                <div className="flex gap-4">
                  <div className="text-accent font-mono text-sm mt-1">{step.num}</div>
                  <div>
                    <h3 className="text-xl font-bold tracking-tight text-text-primary mb-2 uppercase">{step.title}</h3>
                    <p className="text-sm text-text-secondary">{step.desc}</p>
                  </div>
                </div>
                {/* Thin connecting line for layout feel */}
                {i % 3 !== 2 && (
                  <div className="hidden lg:block absolute top-4 left-[calc(100%-2rem)] w-12 h-px bg-border group-hover:bg-accent/50 transition-colors" />
                )}
              </div>
            ))}
          </div>

          <div className="mt-32 pt-16 border-t border-border flex flex-col md:flex-row justify-between items-start md:items-end gap-8">
            <div className="max-w-xl">
              <h3 className="text-3xl font-bold text-text-primary mb-4 uppercase">AUTONOMOUS DOES NOT MEAN UNCONTROLLED.</h3>
              <p className="text-text-secondary text-sm">
                With approval gates, strict policy checks, deterministic verification, and visible execution, 
                ALFRED ensures you maintain oversight while it handles the execution.
              </p>
            </div>
            {!isLoading && (
              isAuthenticated ? (
                <Link 
                  to="/dashboard"
                  className="bg-accent text-surface-primary px-8 py-4 text-sm font-mono tracking-widest hover:bg-accent-hover transition-colors inline-flex items-center gap-2 leading-none shrink-0"
                >
                  GIVE ALFRED A GOAL <span className="opacity-50">→</span>
                </Link>
              ) : (
                <a 
                  href={loginUrl}
                  className="bg-accent text-surface-primary px-8 py-4 text-sm font-mono tracking-widest hover:bg-accent-hover transition-colors inline-flex items-center gap-2 leading-none shrink-0"
                >
                  GIVE ALFRED A GOAL <span className="opacity-50">→</span>
                </a>
              )
            )}
          </div>
        </div>
      </section>

      {/* Footer / Status Area */}
      <footer className="relative z-10 border-t border-border bg-surface-primary/90 p-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <div className="text-[10px] font-mono tracking-widest text-text-secondary mb-4 uppercase">System Status</div>
          <div className="space-y-1 font-mono text-xs">
            <div className="flex justify-between"><span className="text-text-muted">AGENT CORE</span> <span className="text-accent">ONLINE</span></div>
            <div className="flex justify-between"><span className="text-text-muted">PLANNER</span> <span className="text-text-primary">READY</span></div>
            <div className="flex justify-between"><span className="text-text-muted">TOOL ADAPTERS</span> <span className="text-text-primary">05 ACTIVE</span></div>
            <div className="flex justify-between"><span className="text-text-muted">POLICY ENGINE</span> <span className="text-text-primary">ACTIVE</span></div>
            <div className="flex justify-between"><span className="text-text-muted">VERIFIER</span> <span className="text-text-primary">READY</span></div>
          </div>
        </div>
        
        <div className="col-span-2 flex items-center justify-center opacity-20">
          {/* ASCII art world map or abstract grid could go here */}
          <pre className="text-[8px] leading-[8px] font-mono text-text-muted overflow-hidden">
{`      .  . .    .       .      .   .      .       .  .      .       .      .
    .         .       .      .       .  .       .      .       .      .      
 .     .   .     .  .      .       .      .       .      .       .      .    
   .     .      .       .      .       .      .       .      .       .      .
 .    .      .       .      .       .      .       .      .       .      .   
`}
          </pre>
        </div>

        <div className="flex flex-col justify-end items-end text-right">
          <div className="text-[10px] font-mono tracking-widest text-text-secondary mb-2 uppercase">Secure Execution</div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-accent" />
            <span className="font-mono text-xs text-text-primary">ENABLED</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
