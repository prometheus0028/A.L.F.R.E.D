import { Link, Outlet, useLocation } from 'react-router-dom';
import WiregridBackground from './WiregridBackground';
import ProfileMenu from './ProfileMenu';

const DashboardLayout = () => {
  const location = useLocation();

  const getNavClass = (path) => {
    const isActive = location.pathname === path;
    return `block px-4 py-2 uppercase ${
      isActive
        ? 'bg-surface-secondary text-text-primary border border-border'
        : 'text-text-secondary hover:text-text-primary hover:bg-surface-secondary/50'
    }`;
  };

  return (
    <div className="flex h-screen bg-transparent text-text-primary font-sans overflow-hidden">
      <WiregridBackground intensity="medium" />

      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-surface-primary/95 flex flex-col relative z-10">
        <div className="h-16 flex items-center px-6 border-b border-border">
          <Link to="/" className="font-mono text-lg font-bold tracking-widest text-text-primary">ALFRED_</Link>
        </div>
        
        <nav className="flex-1 py-6 px-4 space-y-1 font-mono text-sm tracking-wide">
          <Link to="/dashboard" className={getNavClass('/dashboard')}> &gt; DASHBOARD</Link>
          <Link to="/dashboard/tasks" className={getNavClass('/dashboard/tasks')}> &gt; TASKS</Link>
          <Link to="/dashboard/approvals" className={getNavClass('/dashboard/approvals')}> &gt; APPROVALS </Link>
          <Link to="/dashboard/activity" className={getNavClass('/dashboard/activity')}> &gt; ACTIVITY</Link>
          <Link to="/dashboard/knowledge" className={getNavClass('/dashboard/knowledge')}> &gt; KNOWLEDGE</Link>
          <Link to="/dashboard/finance" className={getNavClass('/dashboard/finance')}> &gt; FINANCE</Link>
          <Link to="/dashboard/settings" className={getNavClass('/dashboard/settings')}> &gt; SETTINGS</Link>
        </nav>

        <div className="p-6 border-t border-border">
          <div className="text-[10px] font-mono tracking-widest text-text-muted mb-2 uppercase">AGENT STATUS</div>
          <div className="flex items-center gap-2 mb-4">
            <span className="w-2 h-2 bg-accent" />
            <span className="font-mono text-sm tracking-wide text-text-primary uppercase">READY</span>
          </div>
          <div className="text-xs text-text-secondary">All systems operational.</div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col relative z-10 overflow-hidden bg-transparent">
        <header className="h-16 border-b border-border flex items-center justify-end px-8 bg-surface-primary/80">
          <ProfileMenu />
        </header>
        <div className="flex-1 overflow-hidden flex flex-col">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
