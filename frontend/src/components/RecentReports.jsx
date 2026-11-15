import React from 'react';
import { ChevronRight } from 'lucide-react';

// 3D Glass Document Orb Badge Component
const Document3DOrb = ({ status, children }) => {
  const isCompleted = status?.toLowerCase() === 'completed' || status === true || status === 'true';
  const isInProgress = status?.toLowerCase() === 'in progress' || status === false || status === 'false';

  return (
    <div
      className={`relative w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center shrink-0 z-10 transition-transform duration-300 group-hover:scale-105 ${
        isCompleted
          ? 'bg-gradient-to-b from-[#125342] via-[#082C21] to-[#031811] border border-[#3AD89A] shadow-[0_0_12px_rgba(58,216,154,0.35)]'
          : isInProgress
          ? 'bg-gradient-to-b from-[#0F354A] via-[#082230] to-[#03131C] border border-[#38BDF8] shadow-[0_0_12px_rgba(56,189,248,0.35)]'
          : 'bg-gradient-to-b from-[#3B2F13] via-[#241A08] to-[#0D0A03] border border-[#D9B978]/70 shadow-[0_0_12px_rgba(217,185,120,0.35)]'
      }`}
    >
      {/* Top Glass Refraction Arc */}
      <div className="absolute top-0.5 left-1.5 right-1.5 h-2 rounded-t-full bg-gradient-to-b from-white/30 to-transparent pointer-events-none" />

      {/* Icon */}
      <div
        className={`relative z-10 filter ${
          isCompleted
            ? 'text-[#42E6A4] drop-shadow-[0_0_5px_rgba(66,230,164,0.6)]'
            : isInProgress
            ? 'text-[#38BDF8] drop-shadow-[0_0_5px_rgba(56,189,248,0.6)]'
            : 'text-[#E2C284] drop-shadow-[0_0_5px_rgba(226,194,132,0.6)]'
        }`}
      >
        {children}
      </div>
    </div>
  );
};

export default function RecentReports({ reports = [], onViewAll, onSelectReport }) {
  const defaultReports = [
    {
      run_id: 'run_38423825',
      title: 'AI Customer Support Software Market',
      date: 'Apr 27, 2026 • 14:32',
      status: 'Completed',
    },
    {
      run_id: 'run_38423826',
      title: 'Fintech Market Analysis',
      date: 'Apr 26, 2026 • 11:20',
      status: 'In Progress',
    },
    {
      run_id: 'run_38423827',
      title: 'E-commerce Competitor Analysis',
      date: 'Apr 25, 2026 • 16:45',
      status: 'Completed',
    },
    {
      run_id: 'run_38423828',
      title: 'SaaS Pricing Comparison',
      date: 'Apr 24, 2026 • 09:12',
      status: 'Pending Approval',
    },
    {
      run_id: 'run_38423829',
      title: 'Healthcare AI Solutions',
      date: 'Apr 23, 2026 • 13:37',
      status: 'Completed',
    },
  ];

  const displayList = reports.length > 0 ? reports : defaultReports;

  const getStatusBadge = (status) => {
    const s = status?.toString().toLowerCase();
    if (s === 'completed' || s === 'true') {
      return (
        <span className="px-3 py-1 rounded-full text-[10px] font-medium bg-gradient-to-r from-[#0E4435] to-[#05261D] border border-[#3AD89A]/80 text-[#3AD89A] shadow-[0_0_10px_rgba(58,216,154,0.3)]">
          Completed
        </span>
      );
    }
    if (s === 'in progress' || s === 'false') {
      return (
        <span className="px-3 py-1 rounded-full text-[10px] font-medium bg-gradient-to-r from-[#0F354A] to-[#051C29] border border-[#38BDF8]/80 text-[#38BDF8] shadow-[0_0_10px_rgba(56,189,248,0.3)]">
          In Progress
        </span>
      );
    }
    return (
      <span className="px-3 py-1 rounded-full text-[10px] font-medium bg-gradient-to-r from-[#42300E] to-[#241904] border border-[#D9B978]/80 text-[#E2C284] shadow-[0_0_10px_rgba(217,185,120,0.3)]">
        Pending Approval
      </span>
    );
  };

  return (
    <div className="h-full relative rounded-3xl p-4 sm:p-6 bg-gradient-to-b from-[#061D16] via-[#041510] to-[#020B08] border border-[#0F3D30] shadow-[0_15px_40px_rgba(0,0,0,0.7)] overflow-hidden flex flex-col justify-between">
      {/* Top Ambient Glow Effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-20 bg-gradient-to-b from-emerald-500/10 to-transparent blur-xl pointer-events-none" />

      {/* Card Header */}
      <div className="flex items-center justify-between mb-3 relative z-10 border-b border-[#0F3D30]/60 pb-2.5">
        <h3 className="font-serif text-base sm:text-lg font-normal text-warm-ivory tracking-wide">
          Recent Reports
        </h3>
        <button
          onClick={onViewAll}
          className="text-xs text-[#3AD89A] hover:text-warm-ivory font-medium flex items-center gap-1 transition-colors cursor-pointer"
        >
          <span>View All</span>
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Reports List */}
      <div className="relative z-10 space-y-1 flex-1 flex flex-col justify-between my-auto">
        {displayList.slice(0, 5).map((item, idx) => {
          const itemStatus = item.status || (item.is_completed ? 'Completed' : 'Pending Approval');

          return (
            <div
              key={idx}
              onClick={() => onSelectReport && onSelectReport(item.run_id)}
              className="flex items-center justify-between p-2 sm:p-2.5 rounded-xl hover:bg-emerald-950/30 transition-all cursor-pointer group border-b border-[#0F3D30]/40 last:border-0"
            >
              {/* Left Side: 3D Orb Badge + Title & Date */}
              <div className="flex items-center gap-3 sm:gap-3.5 min-w-0 pr-2">
                <Document3DOrb status={itemStatus}>
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="8" y1="13" x2="16" y2="13" />
                    <line x1="8" y1="17" x2="14" y2="17" />
                  </svg>
                </Document3DOrb>

                <div className="flex flex-col min-w-0">
                  <h4 className="text-xs sm:text-[13px] font-bold text-warm-ivory truncate group-hover:text-[#3AD89A] transition-colors leading-tight">
                    {item.title || item.objective || `Research Run ${item.run_id}`}
                  </h4>
                  <p className="text-[10px] sm:text-[11px] text-[#8E9F97] font-normal mt-0.5 truncate">
                    {item.date || 'Apr 27, 2026 • 14:32'}
                  </p>
                </div>
              </div>

              {/* Right Side: 3D Status Badge + Chevron */}
              <div className="flex items-center gap-2 shrink-0">
                {getStatusBadge(itemStatus)}
                <ChevronRight className="w-3.5 h-3.5 text-[#8E9F97] group-hover:text-warm-ivory transition-colors" />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
