import React from 'react';
import { Bot, Wrench, Code2, ShieldCheck, ArrowRight, Sparkles } from 'lucide-react';
import Brain3DVisualization from './Brain3DVisualization';

export default function DashboardHero({ onStartNewResearch }) {
  const featurePills = [
    {
      icon: Bot,
      isGold: false,
      title: 'AI Agents',
      desc: 'Multi-step research',
    },
    {
      icon: Wrench,
      isGold: true,
      title: 'Tool Calling',
      desc: 'Real-time data & analysis',
    },
    {
      icon: Code2,
      isGold: false,
      title: 'Structured Output',
      desc: 'JSON + Validated Schema',
    },
    {
      icon: ShieldCheck,
      isGold: true,
      title: 'Evidence Based',
      desc: 'With sources & confidence',
    },
  ];

  return (
    <div className="h-full relative rounded-3xl p-4 sm:p-6 md:p-7 bg-gradient-to-b from-[#061D16] via-[#041510] to-[#020B08] border border-[#0F3D30] shadow-[0_15px_45px_rgba(0,0,0,0.6)] overflow-hidden flex flex-col justify-between">
      {/* Background Radial Ambient Glow */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-radial from-emerald-500/15 via-emerald-900/10 to-transparent blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-radial from-champagne-gold/15 via-champagne-gold/5 to-transparent blur-3xl pointer-events-none" />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center relative z-10 h-full">
        {/* Left Column Text & Controls */}
        <div className="lg:col-span-6 xl:col-span-7 space-y-5">
          {/* Autonomous Tag Pill */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-950/80 border border-emerald-accent/50 text-[11px] font-bold text-emerald-accent shadow-[0_0_12px_rgba(66,230,164,0.2)]">
            <Sparkles className="w-3.5 h-3.5 text-emerald-accent animate-pulse" />
            <span>Autonomous Agentic AI Platform</span>
          </div>

          {/* Heading */}
          <div className="space-y-1">
            <h1 className="text-2xl sm:text-3xl lg:text-3xl xl:text-4xl font-black tracking-tight text-warm-ivory leading-tight">
              Welcome to <span className="emerald-gradient-text">MarketMind AI</span>
            </h1>
            <h2 className="text-base sm:text-lg font-extrabold gold-gradient-text">
              Autonomous Business Research Agent
            </h2>
          </div>

          {/* Description */}
          <p className="text-xs sm:text-sm text-muted-emerald leading-relaxed max-w-xl font-medium">
            Turn your business questions into detailed, evidence-backed market research reports. Our AI agent plans, researches, verifies and delivers — all automatically.
          </p>

          {/* Feature Badges */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
            {featurePills.map((pill, idx) => {
              const Icon = pill.icon;
              return (
                <div key={idx} className="flex flex-col items-start space-y-1.5">
                  <div
                    className={`w-9 h-9 rounded-xl flex items-center justify-center border shadow-md transition-transform hover:scale-105 ${
                      pill.isGold
                        ? 'bg-gradient-to-br from-[#2A2312] to-[#1A160A] border-champagne-gold/60 text-champagne-gold shadow-[0_0_12px_rgba(217,185,120,0.3)]'
                        : 'bg-gradient-to-br from-emerald-950 to-emerald-900 border-emerald-accent/60 text-emerald-accent shadow-[0_0_12px_rgba(66,230,164,0.3)]'
                    }`}
                  >
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <div>
                    <h4 className="text-[11px] font-bold text-warm-ivory leading-snug">{pill.title}</h4>
                    <p className="text-[9px] text-muted-emerald/80 font-medium leading-tight mt-0.5">{pill.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Action Button */}
          <div className="pt-2">
            <button
              onClick={onStartNewResearch}
              className="px-7 py-3 rounded-2xl bg-gradient-to-r from-[#F5D782] via-[#D9B978] to-[#C4A35F] text-obsidian font-extrabold text-xs flex items-center gap-2.5 shadow-[0_8px_25px_rgba(217,185,120,0.45)] hover:shadow-[0_12px_35px_rgba(217,185,120,0.65)] hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer border border-[#FFFDF7]/40"
            >
              <span>Start New Research</span>
              <ArrowRight className="w-4 h-4 stroke-[3]" />
            </button>
          </div>
        </div>

        {/* Right Column 3D Visualization */}
        <div className="lg:col-span-6 xl:col-span-5 flex justify-center w-full min-w-0">
          <Brain3DVisualization />
        </div>
      </div>
    </div>
  );
}
