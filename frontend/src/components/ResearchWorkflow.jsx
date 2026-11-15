import React from 'react';

// Sub-component rendering the 3D Glass Dome & Gold Pedestal Icon
const WorkflowDomeIcon = ({ type, isActive, isCompleted }) => {
  const uid = type;

  return (
    <div className="relative w-28 h-28 sm:w-32 sm:h-32 flex items-center justify-center group cursor-pointer">
      {/* Background Radial Ambient Glow */}
      <div
        className={`absolute inset-0 rounded-full blur-xl transition-all duration-500 ${
          isActive
            ? 'bg-emerald-400/35 scale-110 shadow-[0_0_30px_rgba(66,230,164,0.5)]'
            : isCompleted
            ? 'bg-emerald-500/15 group-hover:bg-emerald-400/25'
            : 'bg-emerald-500/5 group-hover:bg-champagne-gold/20'
        }`}
      />

      <svg
        viewBox="0 0 120 115"
        className="w-full h-full filter drop-shadow-[0_10px_20px_rgba(0,0,0,0.7)] transition-transform duration-300 group-hover:scale-105 group-hover:-translate-y-1 z-10"
      >
        <defs>
          {/* Floor Shadow Gradient */}
          <radialGradient id={`floorShadow_${uid}`} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#000000" stopOpacity="0.85" />
            <stop offset="100%" stopColor="#000000" stopOpacity="0" />
          </radialGradient>

          {/* Golden Pedestal Bevel Gradient */}
          <linearGradient id={`goldBaseGrad_${uid}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFF1B8" />
            <stop offset="25%" stopColor="#E5C158" />
            <stop offset="65%" stopColor="#94742A" />
            <stop offset="100%" stopColor="#3B2B0A" />
          </linearGradient>

          {/* Inner Pedestal Emerald Deck Surface */}
          <radialGradient id={`emeraldSurface_${uid}`} cx="50%" cy="40%" r="50%">
            <stop offset="0%" stopColor="#0F4D38" />
            <stop offset="70%" stopColor="#062218" />
            <stop offset="100%" stopColor="#020E0A" />
          </radialGradient>

          {/* Golden Rim Accent */}
          <linearGradient id={`goldRimGrad_${uid}`} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#C49B38" />
            <stop offset="50%" stopColor="#FFF2BF" />
            <stop offset="100%" stopColor="#8A671B" />
          </linearGradient>

          {/* Glass Dome Shell Gradient */}
          <linearGradient id={`glassDomeGrad_${uid}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.38" />
            <stop offset="20%" stopColor="#A7F3D0" stopOpacity="0.2" />
            <stop offset="60%" stopColor="#065F46" stopOpacity="0.12" />
            <stop offset="100%" stopColor="#022C22" stopOpacity="0.6" />
          </linearGradient>

          {/* Glass Top Specular Refraction Highlight */}
          <linearGradient id={`glassHighlight_${uid}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.9" />
            <stop offset="50%" stopColor="#6EE7B7" stopOpacity="0.45" />
            <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0" />
          </linearGradient>

          {/* Gold Icon 3D Metallic Gradient */}
          <linearGradient id={`goldIconGrad_${uid}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#FFFDF0" />
            <stop offset="30%" stopColor="#F5D061" />
            <stop offset="70%" stopColor="#C49A28" />
            <stop offset="100%" stopColor="#7A590A" />
          </linearGradient>

          {/* Secondary Light Gold Gradient */}
          <linearGradient id={`goldIconGrad2_${uid}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#FFEAA7" />
            <stop offset="50%" stopColor="#D4AF37" />
            <stop offset="100%" stopColor="#AA7C11" />
          </linearGradient>

          {/* Icon Drop Shadow */}
          <filter id={`iconShadow_${uid}`} x="-30%" y="-30%" width="160%" height="160%">
            <feDropShadow dx="0" dy="4" stdDeviation="3" floodColor="#000000" floodOpacity="0.8" />
            <feDropShadow dx="0" dy="0" stdDeviation="6" floodColor="#D9B978" floodOpacity="0.5" />
          </filter>
        </defs>

        {/* 1. Floor Drop Shadow */}
        <ellipse cx="60" cy="98" rx="44" ry="11" fill={`url(#floorShadow_${uid})`} />

        {/* 2. Golden Metallic Pedestal Base */}
        <path d="M16,84 C16,92 104,92 104,84 L104,88 C104,96 16,96 16,88 Z" fill={`url(#goldBaseGrad_${uid})`} />
        <ellipse cx="60" cy="84" rx="44" ry="12" fill={`url(#goldBaseGrad_${uid})`} stroke="#FFEAA7" strokeWidth="0.75" />
        <ellipse cx="60" cy="82" rx="38" ry="9.5" fill={`url(#emeraldSurface_${uid})`} stroke={`url(#goldRimGrad_${uid})`} strokeWidth="1" />
        <ellipse cx="60" cy="81" rx="32" ry="7.5" fill="none" stroke="#42E6A4" strokeWidth="0.8" opacity="0.7" />

        {/* 3. 3D Metallic Golden Icon Inside Dome */}
        <g filter={`url(#iconShadow_${uid})`}>
          {type === 1 && (
            <g transform="translate(60, 47)">
              <path d="M-9,18 L0,8 L9,18" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2.2" strokeLinecap="round" fill="none" />
              <path d="M0,8 L0,22" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2.2" strokeLinecap="round" />
              <rect x="-18" y="-18" width="36" height="26" rx="3.5" fill={`url(#goldIconGrad_${uid})`} stroke="#FFF8E1" strokeWidth="0.8" />
              <rect x="-15" y="-15" width="30" height="20" rx="2" fill="#031A12" />
              <text x="0" y="-1" textAnchor="middle" dominantBaseline="middle" fill={`url(#goldIconGrad_${uid})`} fontSize="16" fontWeight="900" fontFamily="serif">?</text>
            </g>
          )}

          {type === 2 && (
            <g transform="translate(60, 47)">
              <rect x="-15" y="-18" width="30" height="34" rx="3.5" fill={`url(#goldIconGrad_${uid})`} stroke="#FFF8E1" strokeWidth="0.8" />
              <rect x="-12" y="-14" width="24" height="27" rx="1.5" fill="#031A12" />
              <rect x="-7" y="-21" width="14" height="6" rx="1.5" fill={`url(#goldIconGrad2_${uid})`} stroke="#FFFDF0" strokeWidth="0.8" />
              <line x1="-8" y1="-8" x2="6" y2="-8" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2" strokeLinecap="round" />
              <line x1="-8" y1="-2" x2="4" y2="-2" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2" strokeLinecap="round" />
              <line x1="-8" y1="4" x2="6" y2="4" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2" strokeLinecap="round" />
              <line x1="-8" y1="10" x2="1" y2="10" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2" strokeLinecap="round" />
            </g>
          )}

          {type === 3 && (
            <g transform="translate(60, 46)">
              <path
                d="M0,-18 L3,-18 L4,-14 L8,-12 L12,-14 L14,-12 L12,-8 L14,-4 L18,-3 L18,0 L18,3 L14,4 L12,8 L14,12 L12,14 L8,12 L4,14 L3,18 L0,18 L-3,18 L-4,14 L-8,12 L-12,14 L-14,12 L-12,8 L-14,4 L-18,3 L-18,0 L-18,-3 L-14,-4 L-12,-8 L-14,-12 L-12,-14 L-8,-12 L-4,-14 L-3,-18 Z"
                fill={`url(#goldIconGrad_${uid})`}
                stroke="#FFFDF0"
                strokeWidth="0.8"
              />
              <circle cx="0" cy="0" r="10" fill={`url(#goldIconGrad2_${uid})`} />
              <circle cx="0" cy="0" r="5" fill="#031A12" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
            </g>
          )}

          {type === 4 && (
            <g transform="translate(60, 47)">
              <path d="M-15,6 C-15,12 15,12 15,6 L15,12 C15,18 -15,18 -15,12 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#3B2B0A" strokeWidth="0.5" />
              <ellipse cx="0" cy="6" rx="15" ry="5" fill={`url(#goldIconGrad2_${uid})`} stroke="#FFFDF0" strokeWidth="0.8" />
              <path d="M-15,-3 C-15,3 15,3 15,-3 L15,3 C15,9 -15,9 -15,3 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#3B2B0A" strokeWidth="0.5" />
              <ellipse cx="0" cy="-3" rx="15" ry="5" fill={`url(#goldIconGrad2_${uid})`} stroke="#FFFDF0" strokeWidth="0.8" />
              <path d="M-15,-12 C-15,-6 15,-6 15,-12 L15,-6 C15,0 -15,0 -15,-6 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#3B2B0A" strokeWidth="0.5" />
              <ellipse cx="0" cy="-12" rx="15" ry="5" fill={`url(#goldIconGrad2_${uid})`} stroke="#FFFDF0" strokeWidth="0.8" />
            </g>
          )}

          {type === 5 && (
            <g transform="translate(60, 46)">
              <ellipse cx="0" cy="15" rx="10" ry="3" fill={`url(#goldIconGrad_${uid})`} />
              <path d="M0,15 L0,-14" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2.5" strokeLinecap="round" />
              <path d="M-16,-10 L16,-10" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="2.5" strokeLinecap="round" />
              <circle cx="0" cy="-14" r="3" fill={`url(#goldIconGrad2_${uid})`} />
              <line x1="-16" y1="-10" x2="-20" y2="2" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
              <line x1="-16" y1="-10" x2="-12" y2="2" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
              <path d="M-22,2 C-22,8 -10,8 -10,2 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#FFFDF0" strokeWidth="0.6" />
              <line x1="16" y1="-10" x2="12" y2="2" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
              <line x1="16" y1="-10" x2="20" y2="2" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
              <path d="M10,2 C10,8 22,8 22,2 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#FFFDF0" strokeWidth="0.6" />
            </g>
          )}

          {type === 6 && (
            <g transform="translate(60, 46)">
              <path
                d="M0,-18 C8,-18 16,-14 16,-8 C16,6 8,14 0,18 C-8,14 -16,6 -16,-8 C-16,-14 -8,-18 0,-18 Z"
                fill={`url(#goldIconGrad_${uid})`}
                stroke="#FFFDF0"
                strokeWidth="0.8"
              />
              <path
                d="M0,-15 C6,-15 13,-12 13,-7 C13,4 6,11 0,15 C-6,11 -13,4 -13,-7 C-13,-12 -6,-15 0,-15 Z"
                fill="#031A12"
              />
              <path
                d="M-6,0 L-1,5 L7,-5"
                fill="none"
                stroke={`url(#goldIconGrad_${uid})`}
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>
          )}

          {type === 7 && (
            <g transform="translate(60, 47)">
              <circle cx="0" cy="0" r="17" fill="none" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1.5" strokeDasharray="3 2" />
              <circle cx="0" cy="0" r="14" fill="#031A12" stroke={`url(#goldIconGrad_${uid})`} strokeWidth="1" />
              <circle cx="0" cy="-4" r="5" fill={`url(#goldIconGrad_${uid})`} />
              <path d="M-9,10 C-9,4 9,4 9,10 Z" fill={`url(#goldIconGrad_${uid})`} />
            </g>
          )}

          {type === 8 && (
            <g transform="translate(60, 47)">
              <path d="M-14,-18 L4,-18 L14,-8 L14,16 C14,18 -14,18 -14,16 Z" fill={`url(#goldIconGrad_${uid})`} stroke="#FFFDF0" strokeWidth="0.8" />
              <path d="M-11,-15 L2,-15 L11,-6 L11,13 C11,15 -11,15 -11,13 Z" fill="#031A12" />
              <path d="M4,-18 L4,-8 L14,-8" fill={`url(#goldIconGrad2_${uid})`} stroke="#3B2B0A" strokeWidth="0.5" />
              <rect x="-7" y="2" width="3.5" height="8" rx="0.5" fill={`url(#goldIconGrad_${uid})`} />
              <rect x="-2" y="-2" width="3.5" height="12" rx="0.5" fill={`url(#goldIconGrad_${uid})`} />
              <rect x="3" y="-7" width="3.5" height="17" rx="0.5" fill={`url(#goldIconGrad_${uid})`} />
              <path d="M-6,0 L0,-4 L6,-9" fill="none" stroke="#42E6A4" strokeWidth="1.8" strokeLinecap="round" />
            </g>
          )}
        </g>

        {/* 4. Glass Dome Cap over Icon */}
        <path
          d="M20,82 C20,32 100,32 100,82 C100,82.5 20,82.5 20,82 Z"
          fill={`url(#glassDomeGrad_${uid})`}
          stroke={`url(#glassHighlight_${uid})`}
          strokeWidth="1.2"
        />
        <path
          d="M32,58 C32,38 52,24 72,24"
          fill="none"
          stroke="#FFFFFF"
          strokeWidth="2"
          strokeLinecap="round"
          opacity="0.65"
        />
        <ellipse cx="60" cy="82" rx="40" ry="2" fill="none" stroke="#A7F3D0" strokeWidth="0.8" opacity="0.5" />
      </svg>
    </div>
  );
};

export default function ResearchWorkflow({ activeStep = 3 }) {
  const steps = [
    {
      number: 1,
      title: 'Request Analysis',
      subtitle: 'Understand your needs',
    },
    {
      number: 2,
      title: 'Research Planning',
      subtitle: 'Create objectives & questions',
    },
    {
      number: 3,
      title: 'Tool Calling',
      subtitle: 'Search, retrieve, calculate',
    },
    {
      number: 4,
      title: 'Evidence Management',
      subtitle: 'Validate & store sources',
    },
    {
      number: 5,
      title: 'Comparison & Synthesis',
      subtitle: 'Analyze competitors & trends',
    },
    {
      number: 6,
      title: 'Quality Control',
      subtitle: 'Check claims & contradictions',
    },
    {
      number: 7,
      title: 'Human Approval',
      subtitle: 'Review & approve',
    },
    {
      number: 8,
      title: 'Final Report',
      subtitle: 'Generate complete report',
    },
  ];

  return (
    <div className="h-full relative rounded-3xl p-4 sm:p-6 md:p-7 bg-gradient-to-b from-[#061D16] via-[#041510] to-[#020B08] border border-[#0F3D30] shadow-[0_15px_40px_rgba(0,0,0,0.7)] overflow-hidden flex flex-col justify-between">
      {/* Top Ambient Glow Effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-28 bg-gradient-to-b from-emerald-500/15 via-emerald-500/5 to-transparent blur-2xl pointer-events-none" />

      {/* Header Title */}
      <div className="mb-4 relative z-10">
        <h3 className="font-serif text-lg sm:text-xl font-normal text-warm-ivory tracking-wide">
          The Research Workflow
        </h3>
      </div>

      {/* Grid of 8 Steps (2 Rows of 4) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-y-6 gap-x-2 lg:gap-x-4 relative z-10 my-auto">
        {steps.map((step, idx) => {
          const isActive = activeStep === step.number;
          const isCompleted = activeStep > step.number;
          const isEndOfRow = (idx + 1) % 4 === 0;

          return (
            <div key={step.number} className="flex flex-col items-center text-center relative group">
              {/* Top Row: Dome Icon & Directional Arrow */}
              <div className="relative flex items-center justify-center w-full">
                <WorkflowDomeIcon
                  type={step.number}
                  isActive={isActive}
                  isCompleted={isCompleted}
                />

                {!isEndOfRow && (
                  <div className="hidden lg:flex absolute -right-3 sm:-right-4 top-1/2 -translate-y-1/2 z-20 items-center justify-center opacity-80 group-hover:opacity-100 transition-opacity">
                    <svg
                      className="w-4 h-4 text-emerald-400 filter drop-shadow-[0_0_8px_rgba(66,230,164,0.7)]"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2.2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <line x1="4" y1="12" x2="20" y2="12" />
                      <polyline points="13 5 20 12 13 19" />
                    </svg>
                  </div>
                )}
              </div>

              {/* Step Title & Subtitle */}
              <div className="mt-2 flex flex-col items-center">
                <h4 className="text-xs sm:text-[13px] font-bold text-warm-ivory flex items-center gap-1 tracking-tight">
                  <span className="text-warm-ivory font-bold">{step.number}.</span>
                  <span className={isActive ? 'text-emerald-300 font-extrabold' : ''}>{step.title}</span>
                </h4>
                <p className="text-[11px] text-[#8E9F97] font-normal mt-0.5 max-w-[160px] leading-snug">
                  {step.subtitle}
                </p>

                {isActive && (
                  <div className="w-16 h-0.5 mt-1.5 bg-gradient-to-r from-emerald-400 via-champagne-gold to-emerald-400 rounded-full shadow-[0_0_12px_#42E6A4] animate-pulse" />
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
