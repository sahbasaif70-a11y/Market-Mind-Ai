import React, { useState } from 'react';
import { X, Sparkles, ArrowRight, Loader2, Key, HelpCircle, ShieldCheck } from 'lucide-react';

export default function NewResearchModal({ isOpen, onClose, onRunResearch }) {
  const [query, setQuery] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const sampleQueries = [
    "Research the AI customer support software market, compare pricing and features for Zendesk and Intercom.",
    "Calculate CAGR and growth rate for global customer support automation through 2028.",
    "Identify key features, limits, and recommendations for a new AI startup."
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsSubmitting(true);
    await onRunResearch(query, apiKey);
    setIsSubmitting(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-[#020D09]/85 backdrop-blur-xl animate-fade-in overflow-y-auto">
      <div className="relative rounded-3xl w-full max-w-2xl p-4 sm:p-6 bg-gradient-to-b from-[#06241B] via-[#041913] to-[#020F0B] border border-[#D9B978]/70 shadow-[0_25px_60px_rgba(0,0,0,0.85),0_0_30px_rgba(217,185,120,0.3)] overflow-hidden max-h-[92vh] flex flex-col my-auto">
        {/* Top-Right Specular Gold Light Flare */}
        <div className="absolute top-0 right-0 w-44 h-44 bg-gradient-to-bl from-[#FFF1B8]/35 via-[#D9B978]/15 to-transparent rounded-tr-3xl pointer-events-none blur-sm" />

        {/* Top Header */}
        <div className="flex items-center justify-between border-b border-[#0F3D30] pb-3 mb-3 relative z-10 shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-b from-[#125342] via-[#082C21] to-[#031811] border border-[#3AD89A] shadow-[0_0_12px_rgba(58,216,154,0.35)] flex items-center justify-center text-[#3AD89A] shrink-0">
              <Sparkles className="w-4.5 h-4.5 animate-pulse" />
            </div>
            <div>
              <h2 className="font-serif text-base sm:text-lg font-normal text-warm-ivory tracking-wide">
                Start Autonomous AI Research
              </h2>
              <p className="text-[11px] text-[#8E9F97] font-normal">Enter your target industry or competitor question</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-[#031811] border border-[#0F3D30] flex items-center justify-center text-[#8E9F97] hover:text-warm-ivory hover:border-[#D9B978] transition-colors cursor-pointer shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body - Scrollable if needed */}
        <form onSubmit={handleSubmit} className="space-y-3 relative z-10 overflow-y-auto pr-1">
          {/* Main Query Text Area */}
          <div>
            <label className="block text-xs font-semibold text-warm-ivory mb-1.5 flex items-center gap-2">
              <HelpCircle className="w-3.5 h-3.5 text-[#D9B978]" />
              <span>Research Objective / Query:</span>
            </label>
            <textarea
              rows={3}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Research the AI-powered customer support software market, compare major competitors, analyze pricing..."
              className="w-full bg-[#031811] border border-[#0F3D30] rounded-2xl p-3 sm:p-3.5 text-xs text-warm-ivory placeholder-[#8E9F97]/50 focus:outline-none focus:border-[#3AD89A] focus:ring-1 focus:ring-[#3AD89A] transition-all resize-none shadow-inner"
              required
            />
          </div>

          {/* Sample Questions Chips */}
          <div>
            <span className="text-[10px] font-medium text-[#8E9F97] mb-1.5 block">Try Sample Questions:</span>
            <div className="space-y-1.5">
              {sampleQueries.map((sample, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setQuery(sample)}
                  className="w-full text-left px-3 py-1.5 rounded-xl bg-gradient-to-r from-[#052118] to-[#031610] border border-[#0F3D30] text-[11px] text-[#8E9F97] hover:text-warm-ivory hover:border-[#D9B978]/60 transition-all truncate cursor-pointer"
                >
                  "{sample}"
                </button>
              ))}
            </div>
          </div>

          {/* Optional API Key Input */}
          <div className="pt-2 border-t border-[#0F3D30]">
            <label className="block text-[11px] font-semibold text-warm-ivory mb-1 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Key className="w-3.5 h-3.5 text-[#D9B978]" />
                <span>OpenAI API Key (Optional if set in server .env):</span>
              </span>
              <span className="text-[9.5px] text-[#8E9F97] font-normal">sk-proj-...</span>
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your sk-proj-... key or leave blank to use server environment key"
              className="w-full bg-[#031811] border border-[#0F3D30] rounded-xl px-3.5 py-2 text-xs text-warm-ivory placeholder-[#8E9F97]/40 focus:outline-none focus:border-[#D9B978] transition-all"
            />
          </div>

          {/* Guardrails Info Banner */}
          <div className="p-2.5 sm:p-3 rounded-xl bg-gradient-to-r from-[#072B20] to-[#031B14] border border-[#3AD89A]/40 flex items-center justify-between text-[11px] text-[#8E9F97]">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-[#3AD89A] shrink-0" />
              <span>Bounded Loop Guardrails: Max 10 Iterations • Max $1.00 Cost Ceiling</span>
            </div>
            <span className="text-[#3AD89A] font-semibold text-[10px]">100% Provenance Grounded</span>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-2.5 pt-2 border-t border-[#0F3D30] shrink-0">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 rounded-xl text-xs font-medium text-[#8E9F97] hover:text-warm-ivory transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !query.trim()}
              className="px-6 py-2.5 rounded-2xl bg-gradient-to-r from-[#F5D782] via-[#D9B978] to-[#C4A35F] text-[#020B08] font-extrabold text-xs flex items-center gap-2 shadow-[0_8px_25px_rgba(217,185,120,0.45)] hover:shadow-[0_12px_35px_rgba(217,185,120,0.65)] hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 cursor-pointer border border-[#FFFDF7]/40"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin text-[#020B08]" />
                  <span>Agent Planning & Researching...</span>
                </>
              ) : (
                <>
                  <span>Launch Research Agent</span>
                  <ArrowRight className="w-3.5 h-3.5 stroke-[3]" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
