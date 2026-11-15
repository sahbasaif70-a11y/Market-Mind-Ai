import React, { useState, useEffect } from 'react';
import { X, User, ShieldCheck, Key, LogIn, CheckCircle2 } from 'lucide-react';

export default function LoginModal({ isOpen, onClose, user, onSaveUser }) {
  const [name, setName] = useState('');
  const [role, setRole] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [savedSuccess, setSavedSuccess] = useState(false);

  useEffect(() => {
    if (user) {
      setName(user.name || 'Ayesha');
      setRole(user.role || 'Student');
      setApiKey(user.apiKey || '');
    }
  }, [user, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const updatedUser = {
      name: name.trim() || 'Ayesha',
      role: role.trim() || 'Student',
      apiKey: apiKey.trim()
    };
    onSaveUser(updatedUser);
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 900);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-[#020D09]/85 backdrop-blur-xl animate-fade-in overflow-y-auto">
      <div className="relative rounded-3xl w-full max-w-md p-5 sm:p-6 bg-gradient-to-b from-[#06241B] via-[#041913] to-[#020F0B] border border-[#D9B978]/70 shadow-[0_25px_60px_rgba(0,0,0,0.85),0_0_30px_rgba(217,185,120,0.3)] overflow-hidden my-auto">

        {/* Top Specular Glow */}
        <div className="absolute top-0 right-0 w-36 h-36 bg-gradient-to-bl from-[#FFF1B8]/30 via-[#D9B978]/15 to-transparent rounded-tr-3xl pointer-events-none blur-sm" />

        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-[#0F3D30] pb-3 mb-4 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-2xl bg-gradient-to-b from-[#125342] via-[#082C21] to-[#031811] border border-[#3AD89A] shadow-[0_0_12px_rgba(58,216,154,0.35)] flex items-center justify-center text-[#3AD89A] shrink-0">
              <LogIn className="w-4.5 h-4.5" />
            </div>
            <div>
              <h2 className="font-serif text-base sm:text-lg font-normal text-warm-ivory tracking-wide">
                User Login & API Profile
              </h2>
              <p className="text-[11px] text-[#8E9F97]">Set your display name and OpenAI testing credits</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-[#031811] border border-[#0F3D30] flex items-center justify-center text-[#8E9F97] hover:text-warm-ivory hover:border-[#D9B978] transition-colors cursor-pointer shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 relative z-10">
          {/* User Name */}
          <div>
            <label className="block text-xs font-semibold text-warm-ivory mb-1 flex items-center gap-1.5">
              <User className="w-3.5 h-3.5 text-[#3AD89A]" />
              <span>Full Name / Display Name:</span>
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Ayesha, Ali, Sara..."
              className="w-full bg-[#031811] border border-[#0F3D30] rounded-xl px-3.5 py-2.5 text-xs text-warm-ivory placeholder-[#8E9F97]/40 focus:outline-none focus:border-[#3AD89A] transition-all"
              required
            />
          </div>

          {/* User Role */}
          <div>
            <label className="block text-xs font-semibold text-warm-ivory mb-1 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-[#D9B978]" />
              <span>Role / Designation:</span>
            </label>
            <input
              type="text"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              placeholder="e.g. Student, AI Researcher, Product Lead..."
              className="w-full bg-[#031811] border border-[#0F3D30] rounded-xl px-3.5 py-2.5 text-xs text-warm-ivory placeholder-[#8E9F97]/40 focus:outline-none focus:border-[#3AD89A] transition-all"
              required
            />
          </div>

          {/* OpenAI API Key */}
          <div>
            <label className="block text-xs font-semibold text-warm-ivory mb-1 flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <Key className="w-3.5 h-3.5 text-[#D9B978]" />
                <span>OpenAI API Key (For Testing Credits):</span>
              </span>
              <span className="text-[10px] text-[#8E9F97]">sk-proj-...</span>
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter your sk-proj-... API Key (optional)"
              className="w-full bg-[#031811] border border-[#0F3D30] rounded-xl px-3.5 py-2.5 text-xs text-warm-ivory placeholder-[#8E9F97]/40 focus:outline-none focus:border-[#D9B978] transition-all"
            />
            <p className="text-[10px] text-[#8E9F97] mt-1">
              * Enter your API Key so research queries run using your personal credits during testing.
            </p>
          </div>

          {/* Success Banner */}
          {savedSuccess && (
            <div className="p-2.5 rounded-xl bg-[#3AD89A]/20 border border-[#3AD89A] flex items-center justify-center gap-2 text-xs font-semibold text-[#3AD89A] animate-fade-in">
              <CheckCircle2 className="w-4 h-4" />
              <span>Profile & API Key Saved Successfully!</span>
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-[#0F3D30]">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-medium text-[#8E9F97] hover:text-warm-ivory transition-colors cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-2.5 rounded-2xl bg-gradient-to-r from-[#F5D782] via-[#D9B978] to-[#C4A35F] text-[#020B08] font-extrabold text-xs flex items-center gap-2 shadow-[0_8px_25px_rgba(217,185,120,0.45)] hover:scale-[1.02] transition-all cursor-pointer border border-[#FFFDF7]/40"
            >
              <span>Save & Login Profile</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
