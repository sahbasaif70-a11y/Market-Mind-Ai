import React from 'react';
import { Search, Scale } from 'lucide-react';

export default function Brain3DVisualization() {
  return (
    <div className="relative w-full h-[300px] xs:h-[350px] sm:h-[400px] flex items-center justify-center select-none overflow-hidden rounded-3xl p-3">
      {/* Background Radial Emerald & Gold Ambient Glow */}
      <div className="absolute inset-0 bg-radial from-emerald-500/20 via-emerald-950/10 to-transparent blur-3xl pointer-events-none" />
      <div className="absolute bottom-4 w-80 h-36 bg-champagne-gold/20 rounded-full blur-2xl pointer-events-none" />

      {/* Orbital Glowing Rings encircling the Brain */}
      <div className="absolute top-[42%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-[220px] sm:w-[250px] h-[100px] sm:h-[120px] border border-champagne-gold/70 rounded-full pointer-events-none animate-spin-slow [transform:rotateX(72deg)] shadow-[0_0_20px_rgba(217,185,120,0.5)]" />
      <div className="absolute top-[42%] left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200px] sm:w-[230px] h-[90px] sm:h-[110px] border border-emerald-accent/70 rounded-full pointer-events-none animate-[spin_12s_linear_infinite_reverse] [transform:rotateX(72deg)] shadow-[0_0_20px_rgba(66,230,164,0.5)]" />

      {/* Holographic Base Platform Pedestal */}
      <div className="absolute bottom-1 w-80 h-28 pointer-events-none flex items-center justify-center">
        {/* Golden Outer Rim Platform Base */}
        <div className="absolute w-60 sm:w-68 h-16 sm:h-18 rounded-full border-2 border-champagne-gold shadow-[0_0_35px_rgba(217,185,120,0.7)] [transform:rotateX(75deg)] bg-gradient-to-t from-champagne-gold/40 via-emerald-950/50 to-transparent" />
        {/* Inner Glowing Green Ring */}
        <div className="absolute w-40 sm:w-48 h-10 sm:h-12 rounded-full border-2 border-emerald-accent shadow-[0_0_30px_rgba(66,230,164,0.8)] [transform:rotateX(75deg)]" />
        {/* Core Glowing Emerald Disk */}
        <div className="absolute w-28 sm:w-32 h-7 sm:h-9 rounded-full bg-gradient-to-t from-emerald-400/70 via-emerald-500/50 to-transparent blur-xs [transform:rotateX(75deg)]" />
        {/* Vertical Light Beam Cylinder */}
        <div className="absolute bottom-5 w-32 sm:w-40 h-36 sm:h-40 bg-gradient-to-t from-emerald-400/40 via-emerald-500/20 to-transparent [clip-path:polygon(15%_0%,85%_0%,100%_100%,0%_100%)] pointer-events-none blur-xs" />
      </div>

      {/* Main Centerpiece: Emerald Neural Brain PNG */}
      <div className="relative z-10 -mt-8 w-44 h-44 sm:w-52 sm:h-52 flex items-center justify-center animate-float">
        <img
          src="/assets/Emerald Neural Brain Trophy.png"
          alt="MarketMind AI Neural Brain"
          className="w-full h-full object-contain brain-glow filter drop-shadow-[0_0_45px_rgba(66,230,164,0.85)]"
        />
      </div>

      {/* Holographic Connecting Ray Lines */}
      <svg className="absolute inset-0 w-full h-full z-15 pointer-events-none stroke-champagne-gold/60 stroke-dasharray-[4_4]">
        <line x1="22%" y1="20%" x2="42%" y2="38%" className="animate-pulse" />
        <line x1="78%" y1="20%" x2="58%" y2="38%" className="animate-pulse" />
        <line x1="22%" y1="72%" x2="42%" y2="58%" className="animate-pulse" />
        <line x1="78%" y1="72%" x2="58%" y2="58%" className="animate-pulse" />
      </svg>

      {/* 4 Isometric 3D Angled Glass Cards positioned nicely near Brain without touching */}

      {/* Top Left Panel: Research */}
      <div
        style={{ transform: 'perspective(800px) rotateY(18deg) rotateX(-8deg) rotateZ(2deg)' }}
        className="absolute top-2 left-2 sm:left-4 z-20 w-18 sm:w-20 p-2 rounded-xl bg-gradient-to-br from-[#1E1B12]/70 via-[#102922]/80 to-[#071B17]/90 border border-champagne-gold/70 shadow-[0_10px_25px_rgba(0,0,0,0.8),0_0_15px_rgba(217,185,120,0.35)] flex flex-col items-center text-center transition-all duration-300 hover:scale-110 hover:border-champagne-gold backdrop-blur-xl group cursor-pointer"
      >
        <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-champagne-gold shadow-[0_0_8px_#D9B978]" />
        <div className="w-7 h-7 my-0.5 flex items-center justify-center text-champagne-gold filter drop-shadow-[0_0_8px_rgba(217,185,120,0.8)] group-hover:scale-110 transition-transform">
          <Search className="w-5 h-5 stroke-[2.2]" />
        </div>
        <span className="text-[10px] font-extrabold gold-gradient-text tracking-wide mt-0.5">Research</span>
      </div>

      {/* Top Right Panel: Analyze */}
      <div
        style={{ transform: 'perspective(800px) rotateY(-18deg) rotateX(-8deg) rotateZ(-2deg)' }}
        className="absolute top-2 right-2 sm:right-4 z-20 w-18 sm:w-20 p-2 rounded-xl bg-gradient-to-br from-[#1E1B12]/70 via-[#102922]/80 to-[#071B17]/90 border border-champagne-gold/70 shadow-[0_10px_25px_rgba(0,0,0,0.8),0_0_15px_rgba(217,185,120,0.35)] flex flex-col items-center text-center transition-all duration-300 hover:scale-110 hover:border-champagne-gold backdrop-blur-xl group cursor-pointer"
      >
        <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-champagne-gold shadow-[0_0_8px_#D9B978]" />
        {/* 3D Golden Bar Chart Icon */}
        <div className="w-7 h-7 my-0.5 flex items-end justify-center gap-1 filter drop-shadow-[0_0_8px_rgba(217,185,120,0.8)] group-hover:scale-110 transition-transform pb-0.5">
          <div className="w-1.5 h-3 bg-gradient-to-t from-champagne-gold to-[#FFFDF7] rounded-xs" />
          <div className="w-1.5 h-2 bg-gradient-to-t from-champagne-gold to-[#FFFDF7] rounded-xs" />
          <div className="w-1.5 h-5 bg-gradient-to-t from-champagne-gold to-[#FFFDF7] rounded-xs" />
        </div>
        <span className="text-[10px] font-extrabold gold-gradient-text tracking-wide mt-0.5">Analyze</span>
      </div>

      {/* Bottom Left Panel: Compare */}
      <div
        style={{ transform: 'perspective(800px) rotateY(18deg) rotateX(8deg) rotateZ(-2deg)' }}
        className="absolute bottom-6 left-2 sm:left-4 z-20 w-18 sm:w-20 p-2 rounded-xl bg-gradient-to-br from-[#1E1B12]/70 via-[#102922]/80 to-[#071B17]/90 border border-champagne-gold/70 shadow-[0_10px_25px_rgba(0,0,0,0.8),0_0_15px_rgba(217,185,120,0.35)] flex flex-col items-center text-center transition-all duration-300 hover:scale-110 hover:border-champagne-gold backdrop-blur-xl group cursor-pointer"
      >
        <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-champagne-gold shadow-[0_0_8px_#D9B978]" />
        <div className="w-7 h-7 my-0.5 flex items-center justify-center text-champagne-gold filter drop-shadow-[0_0_8px_rgba(217,185,120,0.8)] group-hover:scale-110 transition-transform">
          <Scale className="w-5 h-5 stroke-[2.2]" />
        </div>
        <span className="text-[10px] font-extrabold gold-gradient-text tracking-wide mt-0.5">Compare</span>
      </div>

      {/* Bottom Right Panel: Report */}
      <div
        style={{ transform: 'perspective(800px) rotateY(-18deg) rotateX(8deg) rotateZ(2deg)' }}
        className="absolute bottom-6 right-2 sm:right-4 z-20 w-18 sm:w-20 p-2 rounded-xl bg-gradient-to-br from-[#1E1B12]/70 via-[#102922]/80 to-[#071B17]/90 border border-champagne-gold/70 shadow-[0_10px_25px_rgba(0,0,0,0.8),0_0_15px_rgba(217,185,120,0.35)] flex flex-col items-center text-center transition-all duration-300 hover:scale-110 hover:border-champagne-gold backdrop-blur-xl group cursor-pointer"
      >
        <div className="absolute top-1 right-1 w-1.5 h-1.5 rounded-full bg-champagne-gold shadow-[0_0_8px_#D9B978]" />
        <div className="w-7 h-7 my-0.5 flex items-center justify-center text-champagne-gold filter drop-shadow-[0_0_8px_rgba(217,185,120,0.8)] group-hover:scale-110 transition-transform">
          <svg viewBox="0 0 24 24" className="w-5 h-5 fill-champagne-gold/20 stroke-champagne-gold stroke-[2.2]">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="8" y1="13" x2="16" y2="13" />
            <line x1="8" y1="17" x2="14" y2="17" />
          </svg>
        </div>
        <span className="text-[10px] font-extrabold gold-gradient-text tracking-wide mt-0.5">Report</span>
      </div>
    </div>
  );
}
