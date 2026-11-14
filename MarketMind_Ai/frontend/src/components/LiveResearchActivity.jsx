import React from 'react';

// 3D Glass Orb Badge Component
const Activity3DOrb = ({ isGreen, children }) => {
  return (
    <div
      className={`relative w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center shrink-0 z-10 transition-all duration-300 ${
        isGreen
          ? 'bg-gradient-to-b from-[#125342] via-[#082C21] to-[#031811] border border-[#3AD89A] shadow-[0_0_15px_rgba(58,216,154,0.45)]'
          : 'bg-gradient-to-b from-[#3B2F13] via-[#241A08] to-[#0D0A03] border border-[#D9B978]/70 shadow-[0_0_12px_rgba(217,185,120,0.35)]'
      }`}
    >
      {/* Top Glass Specular Refraction Arc */}
      <div className="absolute top-0.5 left-1.5 right-1.5 h-2 rounded-t-full bg-gradient-to-b from-white/30 to-transparent pointer-events-none" />

      {/* Center Icon */}
      <div
        className={`relative z-10 filter ${
          isGreen
            ? 'text-[#42E6A4] drop-shadow-[0_0_6px_rgba(66,230,164,0.7)]'
            : 'text-[#E2C284] drop-shadow-[0_0_6px_rgba(226,194,132,0.7)]'
        }`}
      >
        {children}
      </div>
    </div>
  );
};

export default function LiveResearchActivity({ currentStepIndex = 2 }) {
  const activities = [
    {
      title: 'Analyzing your request...',
      subtitle: 'Understanding market, segment & goals',
      timestamp: '02:14',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="9" />
          <path d="M9 12l2 2 4-4" />
        </svg>
      ),
    },
    {
      title: 'Planning research strategy...',
      subtitle: 'Generating research questions',
      timestamp: '02:16',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="9" />
          <path d="M9 12l2 2 4-4" />
        </svg>
      ),
    },
    {
      title: 'Searching information...',
      subtitle: 'Querying approved sources',
      timestamp: '02:18',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      ),
    },
    {
      title: 'Verifying evidence...',
      subtitle: 'Checking credibility & relevance',
      timestamp: '02:21',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
          <path d="M9 12l2 2 4-4" />
        </svg>
      ),
    },
    {
      title: 'Synthesizing findings...',
      subtitle: 'Comparing & analyzing data',
      timestamp: '02:25',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 2L2 7l10 5 10-5-10-5z" />
          <path d="M2 17l10 5 10-5" />
          <path d="M2 12l10 5 10-5" />
        </svg>
      ),
    },
    {
      title: 'Generating report...',
      subtitle: 'Building structured output',
      timestamp: '02:28',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <path d="M9 15l2 2 4-4" />
        </svg>
      ),
    },
  ];

  return (
    <div className="h-full relative rounded-3xl p-5 sm:p-6 bg-gradient-to-b from-[#061D16] via-[#041510] to-[#020B08] border border-[#0F3D30] shadow-[0_15px_40px_rgba(0,0,0,0.7)] overflow-hidden flex flex-col justify-between">
      {/* Top Ambient Glow Effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-20 bg-gradient-to-b from-emerald-500/10 to-transparent blur-xl pointer-events-none" />

      {/* Card Header */}
      <div className="flex items-center justify-between mb-4 relative z-10">
        <h3 className="font-serif text-base sm:text-lg font-normal text-warm-ivory tracking-wide">
          Live Research Activity
        </h3>
        <div className="flex items-center gap-1.5 text-xs font-medium text-[#3AD89A]">
          <span className="w-2 h-2 rounded-full bg-[#3AD89A] shadow-[0_0_8px_#3AD89A] animate-pulse" />
          <span>Agent Online</span>
        </div>
      </div>

      {/* Timeline List with Vertical Connecting Line */}
      <div className="relative z-10 space-y-3 flex-1 flex flex-col justify-between my-auto">
        {/* Continuous Vertical Connecting Line */}
        <div className="absolute left-[17px] sm:left-[19px] top-4 bottom-4 w-[2px] bg-gradient-to-b from-[#3AD89A] via-[#D9B978]/60 to-[#0F3D30] z-0" />

        {activities.map((act, idx) => {
          const isGreen = idx < (currentStepIndex > 0 ? currentStepIndex : 2);

          return (
            <div key={idx} className="relative flex items-center justify-between z-10 group">
              <div className="flex items-center gap-3 sm:gap-3.5 min-w-0">
                {/* 3D Glass Orb Badge */}
                <Activity3DOrb isGreen={isGreen}>
                  {act.icon}
                </Activity3DOrb>

                {/* Text Title & Subtitle */}
                <div className="flex flex-col min-w-0">
                  <h4 className="text-xs sm:text-[13px] font-bold text-warm-ivory leading-tight tracking-tight truncate">
                    {act.title}
                  </h4>
                  <p className="text-[10px] sm:text-[11px] text-[#8E9F97] font-normal mt-0.5 truncate">
                    {act.subtitle}
                  </p>
                </div>
              </div>

              {/* Timestamp */}
              <span className="text-[10px] sm:text-[11px] text-[#7A8C84] font-mono shrink-0 ml-3">
                {act.timestamp}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
