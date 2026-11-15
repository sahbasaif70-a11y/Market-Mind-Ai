import React, { useState } from 'react';
import { Search, Bell, Sun, ChevronDown, Menu } from 'lucide-react';

export default function Header({ onSearchSubmit, user, onOpenLogin, onToggleMobileMenu }) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && searchQuery.trim()) {
      onSearchSubmit(searchQuery);
    }
  };

  const displayName = user?.name || 'Ayesha';
  const displayRole = user?.role || 'Student';

  return (
    <header className="h-16 shrink-0 border-b border-[#0F3D30] px-3 sm:px-6 flex items-center justify-between sticky top-0 z-30 bg-[#071B17]/95 backdrop-blur-xl gap-2 sm:gap-4">
      {/* Mobile Menu Toggle Button */}
      <button
        onClick={onToggleMobileMenu}
        className="md:hidden p-2 rounded-xl bg-[#051C16] border border-[#0F3D30] text-warm-ivory hover:text-[#3AD89A] hover:border-[#3AD89A]/50 transition-all shrink-0 cursor-pointer"
        aria-label="Toggle navigation menu"
      >
        <Menu className="w-5 h-5 text-warm-ivory" />
      </button>

      {/* Search Input Bar */}
      <div className="flex-1 max-w-xl relative min-w-0">
        <Search className="w-4 h-4 text-[#3AD89A] absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question..."
          className="w-full bg-[#051C16] border border-[#0F3D30] rounded-xl pl-9 sm:pl-10 pr-3 py-1.5 sm:py-2 text-xs text-warm-ivory placeholder-muted-emerald/70 focus:outline-none focus:border-[#3AD89A]/80 focus:ring-1 focus:ring-[#3AD89A]/80 transition-all font-medium truncate"
        />
      </div>

      {/* Right User Actions */}
      <div className="flex items-center gap-2 sm:gap-3.5 shrink-0">
        {/* Notification Bell */}
        <button className="w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-[#051C16] border border-[#0F3D30] flex items-center justify-center text-muted-emerald hover:text-warm-ivory hover:border-[#3AD89A]/50 transition-all relative cursor-pointer">
          <Bell className="w-4 h-4 text-warm-ivory" />
          <span className="absolute top-1.5 right-1.5 sm:top-2 sm:right-2 w-2 h-2 rounded-full bg-[#3AD89A] shadow-[0_0_8px_#3AD89A]" />
        </button>

        {/* Theme Toggle - Hidden on very small screens */}
        <button className="hidden xs:flex w-8 h-8 sm:w-9 sm:h-9 rounded-full bg-[#051C16] border border-[#0F3D30] items-center justify-center text-muted-emerald hover:text-warm-ivory hover:border-[#3AD89A]/50 transition-all cursor-pointer">
          <Sun className="w-4 h-4 text-warm-ivory" />
        </button>

        {/* Vertical Divider */}
        <div className="hidden sm:block h-6 w-[1px] bg-[#0F3D30]" />

        {/* Profile Card (Clickable to open Login / Profile Modal) */}
        <div
          onClick={onOpenLogin}
          title="Click to edit profile or set OpenAI API key"
          className="flex items-center gap-2 cursor-pointer group bg-[#051C16]/80 hover:bg-[#092B21] border border-[#0F3D30] hover:border-[#3AD89A]/60 px-2 sm:px-3 py-1 sm:py-1.5 rounded-2xl transition-all"
        >
          <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-tr from-[#3AD89A] via-[#D9B978] to-[#42E6A4] p-0.5 shadow-md shrink-0">
            <div className="w-full h-full rounded-full bg-[#071B17] flex items-center justify-center overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=150&q=80"
                alt="Profile Avatar"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
          <div className="text-left hidden sm:block">
            <h4 className="text-xs font-bold text-warm-ivory group-hover:text-[#3AD89A] transition-colors leading-tight">
              {displayName}
            </h4>
            <p className="text-[10px] text-[#8E9F97] font-semibold">{displayRole}</p>
          </div>
          <ChevronDown className="w-3.5 h-3.5 text-[#8E9F97] group-hover:text-warm-ivory transition-colors" />
        </div>
      </div>
    </header>
  );
}
