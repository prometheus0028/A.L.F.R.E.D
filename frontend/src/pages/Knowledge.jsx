import React from 'react';

const Knowledge = () => {
  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      <div className="h-16 flex items-center px-8 border-b border-border shrink-0">
        <span className="font-mono text-xs tracking-widest text-text-secondary uppercase">KNOWLEDGE / 05</span>
      </div>
      
      <div className="p-8 flex-1 overflow-y-auto">
        <h1 className="text-2xl font-bold tracking-tight mb-8 uppercase">DOCUMENT REPOSITORY</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { title: 'Project_Alpha_Requirements.pdf', type: 'PDF DOCUMENT', size: '2.4 MB' },
            { title: 'Q3_Financial_Summary.xlsx', type: 'SPREADSHEET', size: '1.1 MB' },
            { title: 'ACME_Invoice_1042.pdf', type: 'INVOICE', size: '450 KB' },
            { title: 'meeting_brief_rahul.md', type: 'GENERATED ARTIFACT', size: '12 KB' },
            { title: 'Employee_Handbook.pdf', type: 'POLICY', size: '5.6 MB' }
          ].map((doc, idx) => (
            <div key={idx} className="border border-border p-4 hover:border-text-muted transition-colors cursor-pointer group bg-surface-secondary/20">
              <div className="font-mono text-[10px] tracking-widest text-text-muted mb-2 uppercase">{doc.type}</div>
              <div className="font-mono text-sm text-text-primary mb-4 truncate group-hover:text-accent transition-colors">{doc.title}</div>
              <div className="flex justify-between items-center">
                <span className="font-mono text-xs text-text-secondary">{doc.size}</span>
                <span className="font-mono text-[10px] tracking-widest text-text-primary uppercase border border-border px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity">VIEW</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Knowledge;
