import React from 'react';

export default function SmarterInsightsCard({ onStartNewResearch }) {
  return (
    <div
      onClick={onStartNewResearch}
      className="relative rounded-2xl sm:rounded-3xl bg-gradient-to-r from-[#061D16] via-[#041510] to-[#020D09] border border-[#D9B978]/70 hover:border-[#FFF1B8] p-3 sm:px-5 sm:py-3.5 shadow-[0_12px_35px_rgba(0,0,0,0.6)] overflow-hidden cursor-pointer group transition-all duration-300 hover:scale-[1.01] flex items-center justify-between"
    >
      {/* Top-Right Specular Gold Light Flare */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-[#FFF1B8]/35 via-[#D9B978]/10 to-transparent rounded-tr-3xl pointer-events-none blur-xs" />

      {/* 3D Faceted Emerald Mountain & Golden Sunbeam Artwork */}
      <svg
        viewBox="0 0 300 120"
        className="absolute right-0 top-0 bottom-0 w-1/2 h-full pointer-events-none object-cover z-0"
        preserveAspectRatio="none"
      >
        <defs>
          <radialGradient id="sunGlow" cx="85%" cy="20%" r="75%">
            <stop offset="0%" stopColor="#FFF2BF" stopOpacity="0.85" />
            <stop offset="30%" stopColor="#D9B978" stopOpacity="0.5" />
            <stop offset="65%" stopColor="#2E6B56" stopOpacity="0.25" />
            <stop offset="100%" stopColor="#041812" stopOpacity="0" />
          </radialGradient>

          <linearGradient id="emeraldPeakLight" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#A7F3D0" />
            <stop offset="40%" stopColor="#34D399" />
            <stop offset="80%" stopColor="#059669" />
            <stop offset="100%" stopColor="#064E3B" />
          </linearGradient>

          <linearGradient id="emeraldPeakShadow" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#065F46" />
            <stop offset="50%" stopColor="#043E2E" />
            <stop offset="100%" stopColor="#021E16" />
          </linearGradient>

          <linearGradient id="goldRidge" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#FFF1B8" />
            <stop offset="50%" stopColor="#D9B978" />
            <stop offset="100%" stopColor="#7A590A" />
          </linearGradient>
        </defs>

        <rect x="0" y="0" width="300" height="120" fill="url(#sunGlow)" />
        <path d="M150,120 L220,40 L300,120 Z" fill="url(#goldRidge)" opacity="0.5" />

        <path d="M170,120 L210,12 L235,120 Z" fill="url(#emeraldPeakLight)" />
        <path d="M210,12 L285,120 L235,120 Z" fill="url(#emeraldPeakShadow)" />
        <line x1="210" y1="12" x2="235" y2="120" stroke="#E6FFFA" strokeWidth="1.5" strokeLinecap="round" opacity="0.9" />

        <path d="M130,120 L180,50 L215,120 Z" fill="url(#emeraldPeakLight)" opacity="0.8" />
        <path d="M180,50 L245,120 L215,120 Z" fill="url(#emeraldPeakShadow)" opacity="0.8" />
        <line x1="180" y1="50" x2="215" y2="120" stroke="#A7F3D0" strokeWidth="1.2" opacity="0.8" />

        <circle cx="210" cy="12" r="3" fill="#FFFFFF" />
        <circle cx="210" cy="12" r="8" fill="#FFEAA7" opacity="0.5" />
      </svg>

      {/* Left Text + Circular Arrow Button */}
      <div className="relative z-10 flex items-center gap-3.5">
        {/* Title & Subtitle */}
        <div className="flex flex-col">
          <h4 className="font-serif text-xs sm:text-sm font-normal text-warm-ivory tracking-wide leading-tight">
            Smarter Insights
          </h4>
          <p className="font-serif text-xs sm:text-sm font-normal text-warm-ivory tracking-wide leading-tight mt-0.5">
            Bigger Opportunities
          </p>
        </div>

        {/* Circular Arrow Button */}
        <div className="w-8 h-8 rounded-full bg-gradient-to-b from-[#D9B978]/30 to-[#061D16]/80 border border-[#D9B978] shadow-[0_0_10px_rgba(217,185,120,0.4)] flex items-center justify-center text-warm-ivory group-hover:bg-[#D9B978] group-hover:text-[#041812] group-hover:scale-105 transition-all duration-300 shrink-0">
          <svg
            className="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <line x1="5" y1="12" x2="19" y2="12" />
            <polyline points="12 5 19 12 12 19" />
          </svg>
        </div>
      </div>
    </div>
  );
}
