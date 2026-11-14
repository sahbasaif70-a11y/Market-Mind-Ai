import React from 'react';

// Circular 3D Glass Emerald Orb Badge component
const OrbIconBadge = ({ children }) => {
  return (
    <div className="relative w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center shrink-0 bg-gradient-to-b from-[#125342] via-[#082C21] to-[#031811] border border-[#3AD89A]/60 shadow-[0_0_10px_rgba(58,216,154,0.35),inset_0_2px_4px_rgba(255,255,255,0.25)] group-hover:scale-105 transition-transform duration-300">
      {/* Top Glass Refraction Arc */}
      <div className="absolute top-0.5 left-1.5 right-1.5 h-2 rounded-t-full bg-gradient-to-b from-white/30 to-transparent pointer-events-none" />
      {/* Icon */}
      <div className="relative z-10 text-[#E2C284] filter drop-shadow-[0_0_5px_rgba(226,194,132,0.6)]">
        {children}
      </div>
    </div>
  );
};

export default function MetricsFooter() {
  const metrics = [
    {
      value: '15+',
      label: 'Test Cases',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="8" y="2" width="8" height="4" rx="1" fill="currentColor" fillOpacity="0.2" />
          <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
          <path d="M9 12l2 2 4-4" />
        </svg>
      ),
    },
    {
      value: '100',
      label: 'Marks',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" fill="currentColor" fillOpacity="0.15" />
        </svg>
      ),
    },
    {
      value: '24–32 hrs',
      label: 'Estimated Effort',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <polyline points="12 6 12 12 16 14" />
        </svg>
      ),
    },
    {
      value: 'Python + OpenAI',
      label: 'Tech Stack',
      icon: (
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="16 18 22 12 16 6" />
          <polyline points="8 6 2 12 8 18" />
        </svg>
      ),
    },
  ];

  return (
    <div className="relative rounded-2xl sm:rounded-3xl bg-gradient-to-r from-[#051C16] via-[#031510] to-[#020D09] border border-[#0F3D30] p-3 sm:px-4 sm:py-3.5 shadow-[0_12px_35px_rgba(0,0,0,0.6)] overflow-hidden">
      {/* Bottom Gold Ambient Sheen */}
      <div className="absolute -bottom-4 -left-4 w-36 h-14 bg-champagne-gold/10 rounded-full blur-xl pointer-events-none" />

      {/* Content-based Flexible Horizontal Container */}
      <div className="flex flex-wrap sm:flex-nowrap items-center justify-between gap-y-3 gap-x-1 sm:gap-x-2">
        {metrics.map((metric, idx) => (
          <React.Fragment key={idx}>
            <div className="flex items-center gap-2 sm:gap-2.5 px-1 sm:px-2 py-0.5 group cursor-default shrink-0">
              {/* 3D Circular Emerald Glass Orb Badge */}
              <OrbIconBadge>{metric.icon}</OrbIconBadge>

              {/* Label & Value */}
              <div className="flex flex-col">
                <span className="text-xs sm:text-[13px] font-bold text-warm-ivory tracking-tight whitespace-nowrap">
                  {metric.value}
                </span>
                <span className="text-[10px] sm:text-[11px] text-[#8E9F97] font-normal leading-tight whitespace-nowrap">
                  {metric.label}
                </span>
              </div>
            </div>

            {/* Vertical Divider (between items on desktop) */}
            {idx < metrics.length - 1 && (
              <div className="hidden sm:block h-7 w-[1px] bg-[#0F3D30] shrink-0" />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
