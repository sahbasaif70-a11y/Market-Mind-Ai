import React from 'react';
import {
  Home,
  Plus,
  FileText,
  History,
  BookOpen,
  Settings,
  X
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, onStartNewResearch, isOpen, onClose }) {
  const menuItems = [
    { id: 'dashboard', label: 'Home', icon: Home },
    { id: 'new-research', label: 'New Research', icon: Plus, action: onStartNewResearch },
    { id: 'reports', label: 'My Reports', icon: FileText },
    { id: 'history', label: 'Research History', icon: History },
    { id: 'knowledge', label: 'Knowledge Base', icon: BookOpen },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className={`fixed inset-y-0 left-0 z-50 w-64 h-screen bg-gradient-to-b from-[#051C16] via-[#031510] to-[#020D09] border-r border-[#D9B978]/40 shadow-[10px_0_35px_rgba(0,0,0,0.8)] flex flex-col justify-between p-4 transition-transform duration-300 ease-in-out md:static md:translate-x-0 ${
      isOpen ? 'translate-x-0' : '-translate-x-full'
    } shrink-0 select-none overflow-y-auto`}>
      {/* Top-Left Specular Light Flare */}
      <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-[#FFF1B8]/30 via-[#D9B978]/10 to-transparent rounded-tl-3xl pointer-events-none blur-sm" />

      {/* Top Section: Logo Branding & Navigation */}
      <div className="relative z-10">
        {/* Branding Header with 3D Emerald Gem Logo & Mobile Close Button */}
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center gap-3">
            {/* 3D Faceted Emerald Gem Logo Mark */}
            <svg viewBox="0 0 40 40" className="w-9 h-9 shrink-0 filter drop-shadow-[0_0_12px_rgba(58,216,154,0.6)]">
              <defs>
                <linearGradient id="logoGemLight" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#A7F3D0" />
                  <stop offset="50%" stopColor="#34D399" />
                  <stop offset="100%" stopColor="#059669" />
                </linearGradient>
                <linearGradient id="logoGemDark" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#047857" />
                  <stop offset="100%" stopColor="#022C22" />
                </linearGradient>
                <linearGradient id="logoGold" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#FFF1B8" />
                  <stop offset="100%" stopColor="#D9B978" />
                </linearGradient>
              </defs>
              <path d="M5,10 L15,30 L20,18 L25,30 L35,10 L28,6 L20,22 L12,6 Z" fill="url(#logoGemLight)" stroke="url(#logoGold)" strokeWidth="0.8" />
              <path d="M15,30 L20,18 L20,38 Z" fill="url(#logoGemDark)" />
              <path d="M25,30 L20,18 L20,38 Z" fill="url(#logoGemLight)" opacity="0.85" />
            </svg>

            <div>
              <h1 className="font-serif font-semibold text-base text-warm-ivory tracking-wide leading-tight">
                MarketMind AI
              </h1>
              <p className="text-[9.5px] text-[#8E9F97] font-normal mt-0.5">Smarter Research. Better Decisions.</p>
            </div>
          </div>

          {/* Close button for mobile drawer */}
          <button
            onClick={onClose}
            className="md:hidden p-1.5 rounded-lg text-[#8E9F97] hover:text-warm-ivory hover:bg-[#07241B] transition-colors cursor-pointer"
            aria-label="Close menu"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Menu */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;

            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.action) {
                    item.action();
                  } else {
                    setActiveTab(item.id);
                  }
                  if (onClose) onClose();
                }}
                className={`w-full flex items-center gap-3 px-3.5 py-2 rounded-xl text-xs transition-all duration-300 cursor-pointer relative group ${
                  isActive
                    ? 'bg-gradient-to-r from-[#0E4838] via-[#093528] to-[#041D16] border border-[#3AD89A] shadow-[0_0_15px_rgba(58,216,154,0.35)] text-warm-ivory font-serif font-medium'
                    : 'text-[#8E9F97] hover:text-warm-ivory hover:bg-emerald-950/30 border border-transparent font-normal'
                }`}
              >
                {/* Active Top Glass Specular Arc */}
                {isActive && (
                  <div className="absolute top-0.5 left-3 right-3 h-1.5 rounded-t-full bg-gradient-to-b from-white/25 to-transparent pointer-events-none" />
                )}

                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-[#E2C284]' : 'text-[#E2C284]/80 group-hover:text-[#E2C284]'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Middle/Lower Background Wave Graphic */}
      <div className="absolute bottom-16 left-0 right-0 h-36 pointer-events-none overflow-hidden opacity-30">
        <svg viewBox="0 0 200 150" className="w-full h-full object-cover">
          <defs>
            <linearGradient id="bgWaveGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3AD89A" stopOpacity="0.6" />
              <stop offset="50%" stopColor="#D9B978" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#041812" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path d="M-20 100 Q40 40 100 80 T220 50" fill="none" stroke="url(#bgWaveGrad)" strokeWidth="3" />
          <path d="M-20 115 Q40 55 100 95 T220 65" fill="none" stroke="#3AD89A" strokeWidth="1.5" opacity="0.6" strokeDasharray="5 3" />
        </svg>
      </div>

      {/* Bottom Section: Promo Card + System Status */}
      <div className="space-y-3 pt-2 relative z-10">
        {/* Promo Card: "Turning Questions into Market Insights" */}
        <div className="relative rounded-2xl p-4 bg-gradient-to-b from-[#06241B] via-[#041913] to-[#020F0B] border border-[#3AD89A]/80 shadow-[0_15px_40px_rgba(0,0,0,0.8),0_0_20px_rgba(58,216,154,0.3)] overflow-hidden group">
          {/* Top-Right Specular Gold Light Flare */}
          <div className="absolute top-0 right-0 w-28 h-28 bg-gradient-to-bl from-[#FFF1B8]/40 via-[#D9B978]/15 to-transparent rounded-tr-2xl pointer-events-none blur-sm" />

          {/* Serif Title */}
          <h3 className="font-serif text-xs sm:text-sm font-normal text-[#E2C284] leading-tight tracking-wide relative z-10">
            Turning<br />Questions into<br />Market Insights
          </h3>

          {/* Subtitle */}
          <p className="text-[10px] text-[#8E9F97] font-normal leading-relaxed mt-1.5 relative z-10 max-w-[170px]">
            AI-powered research for smarter business decisions.
          </p>

          {/* 3D Flowing Gold-Emerald Silk Wave & Stardust Artwork */}
          <div className="-mx-4 -mb-4 relative z-0">
            <svg viewBox="0 0 240 100" className="w-full h-20 mt-1 pointer-events-none object-cover">
              <defs>
                <linearGradient id="silkEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#3AD89A" stopOpacity="0.85" />
                  <stop offset="50%" stopColor="#0E5E48" stopOpacity="0.95" />
                  <stop offset="100%" stopColor="#04281E" stopOpacity="0.9" />
                </linearGradient>

                <linearGradient id="silkGold" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FFF1B8" stopOpacity="0.9" />
                  <stop offset="40%" stopColor="#D9B978" stopOpacity="0.85" />
                  <stop offset="80%" stopColor="#3AD89A" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#041E16" stopOpacity="0" />
                </linearGradient>

                <linearGradient id="ridgeGlow" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FFFFFF" stopOpacity="0.9" />
                  <stop offset="50%" stopColor="#FFF1B8" stopOpacity="0.95" />
                  <stop offset="80%" stopColor="#3AD89A" stopOpacity="0.8" />
                  <stop offset="100%" stopColor="#FFFFFF" stopOpacity="0" />
                </linearGradient>
              </defs>

              <path d="M0 50 Q60 90 120 55 T240 40 L240 100 L0 100 Z" fill="url(#silkEmerald)" />
              <path d="M0 75 Q70 25 140 65 T240 30 L240 100 L0 100 Z" fill="url(#silkGold)" opacity="0.75" />
              <path d="M0 45 Q60 85 120 50 T240 35" fill="none" stroke="url(#ridgeGlow)" strokeWidth="2" />

              {/* Gold Stardust Particles */}
              <circle cx="35" cy="65" r="1.5" fill="#FFF1B8" />
              <circle cx="75" cy="35" r="2" fill="#FFEAA7" />
              <circle cx="130" cy="28" r="2.5" fill="#FFF1B8" />
              <circle cx="185" cy="32" r="1" fill="#FFFFFF" />
            </svg>
          </div>
        </div>

        {/* System Status Footer */}
        <div className="flex flex-col gap-0.5 px-1">
          <div className="flex items-center gap-2 text-xs font-medium text-[#3AD89A]">
            <span className="w-2 h-2 rounded-full bg-[#3AD89A] shadow-[0_0_8px_#3AD89A] animate-pulse" />
            <span>System Online</span>
          </div>
          <span className="text-[10px] text-[#7A8C84] font-mono pl-4">v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
