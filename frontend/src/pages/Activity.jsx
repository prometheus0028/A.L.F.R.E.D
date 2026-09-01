import React from 'react';

const Activity = () => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">ACTIVITY / 04</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">SYSTEM EVENT LOG</h1>
        
        <div className="max-w-4xl border-l border-border/50 ml-4 pl-8 space-y-6">
          {[
            { time: '[20:41:02]', action: 'GOAL_RECEIVED', details: 'Prepare me for tomorrow\'s meeting' },
            { time: '[20:41:03]', action: 'PLAN_CREATED', details: '5 actions identified' },
            { time: '[20:41:05]', action: 'CALENDAR_SEARCH', details: '1 meeting found' },
            { time: '[20:41:06]', action: 'EMAIL_SEARCH', details: '4 relevant messages' },
            { time: '[20:41:08]', action: 'FILE_SEARCH', details: 'No exact result' },
            { time: '[20:41:09]', action: 'REPLANNING', details: 'Alternative search initiated' },
            { time: '[20:41:11]', action: 'FILE_SEARCH', details: '2 documents found' },
            { time: '[20:41:14]', action: 'DOCUMENT_CREATE', details: 'meeting_brief.md' },
            { time: '[20:41:16]', action: 'VERIFICATION', details: 'PASSED', isSuccess: true }
          ].map((log, idx) => (
            <div key={idx} className="relative">
              <div className={`absolute -left-[37px] top-1.5 w-1.5 h-1.5 ${log.isSuccess ? 'bg-accent' : 'bg-text-muted'}`} />
              <div className="font-mono text-xs flex gap-4">
                <span className="text-text-muted">{log.time}</span>
                <span className={log.isSuccess ? 'text-accent' : 'text-text-secondary'}>{log.action}</span>
              </div>
              <div className="font-mono text-sm text-text-primary mt-1">{log.details}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Activity;
