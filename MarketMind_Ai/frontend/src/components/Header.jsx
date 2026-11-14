import React, { useState } from 'react';
import { Search, Bell, Sun, ChevronDown } from 'lucide-react';

export default function Header({ onSearchSubmit }) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      onSearchSubmit(searchQuery);
    }
  };

  return (
    <header className="h-16 shrink-0 border-b border-[#0F3D30] px-6 flex items-center justify-between sticky top-0 z-30 bg-[#071B17]/95 backdrop-blur-xl">
      {/* Search Input Bar */}
      <div className="flex-1 max-w-xl relative">
        <Search className="w-4 h-4 text-[#3AD89A] absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a research question... (e.g. Analyze AI customer support market)"
          className="w-full bg-[#051C16] border border-[#0F3D30] rounded-xl pl-10 pr-4 py-2 text-xs text-warm-ivory placeholder-muted-emerald/70 focus:outline-none focus:border-[#3AD89A]/80 focus:ring-1 focus:ring-[#3AD89A]/80 transition-all font-medium"
        />
      </div>

      {/* Right User Actions */}
      <div className="flex items-center gap-3.5">
        {/* Notification Bell */}
        <button className="w-9 h-9 rounded-full bg-[#051C16] border border-[#0F3D30] flex items-center justify-center text-muted-emerald hover:text-warm-ivory hover:border-[#3AD89A]/50 transition-all relative cursor-pointer">
          <Bell className="w-4 h-4 text-warm-ivory" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-[#3AD89A] shadow-[0_0_8px_#3AD89A]" />
        </button>

        {/* Theme Toggle */}
        <button className="w-9 h-9 rounded-full bg-[#051C16] border border-[#0F3D30] flex items-center justify-center text-muted-emerald hover:text-warm-ivory hover:border-[#3AD89A]/50 transition-all cursor-pointer">
          <Sun className="w-4 h-4 text-warm-ivory" />
        </button>

        {/* Vertical Divider */}
        <div className="h-6 w-[1px] bg-[#0F3D30]" />

        {/* Profile Card */}
        <div className="flex items-center gap-2.5 cursor-pointer group">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-[#3AD89A] via-[#D9B978] to-[#42E6A4] p-0.5 shadow-md shrink-0">
            <div className="w-full h-full rounded-full bg-[#071B17] flex items-center justify-center overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
                alt="Ayesha Profile"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          <div className="text-left hidden sm:block">
            <h4 className="text-xs font-bold text-warm-ivory group-hover:text-[#3AD89A] transition-colors leading-tight">Ayesha</h4>
            <p className="text-[10px] text-[#8E9F97] font-semibold">Student</p>
          </div>
          <ChevronDown className="w-3.5 h-3.5 text-[#8E9F97] group-hover:text-warm-ivory transition-colors" />
        </div>
      </div>
    </header>
  );
}
