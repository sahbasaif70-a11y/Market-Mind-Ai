import React, { useState } from 'react';
import { ShieldCheck, CheckCircle2, XCircle, RotateCcw, Download, X } from 'lucide-react';

export default function HumanApprovalModal({ isOpen, onClose, runId, onDecision }) {
  const [selectedDecision, setSelectedDecision] = useState('approve');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const decisions = [
    {
      id: 'approve',
      title: 'APPROVE',
      desc: 'Publish report and save final output files permanently.',
      icon: CheckCircle2,
      color: 'emerald',
    },
    {
      id: 'reject',
      title: 'REJECT',
      desc: 'Reject report findings and discard generated draft.',
      icon: XCircle,
      color: 'red',
    },
    {
      id: 'return_for_revision',
      title: 'REVISION',
      desc: 'Return report with requested additional research subquestions.',
      icon: RotateCcw,
      color: 'amber',
    },
    {
      id: 'export',
      title: 'EXPORT LOG',
      desc: 'Export research state JSON log for inspection.',
      icon: Download,
      color: 'blue',
    },
  ];

  const handleSubmit = async () => {
    setIsSubmitting(true);
    await onDecision(selectedDecision);
    setIsSubmitting(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#020D09]/85 backdrop-blur-xl animate-fade-in">
      <div className="relative rounded-3xl w-full max-w-lg p-6 sm:p-7 bg-gradient-to-b from-[#06241B] via-[#041913] to-[#020F0B] border border-[#D9B978]/70 shadow-[0_25px_60px_rgba(0,0,0,0.85),0_0_30px_rgba(217,185,120,0.3)] space-y-5 overflow-hidden">
        {/* Top-Right Specular Gold Light Flare */}
        <div className="absolute top-0 right-0 w-36 h-36 bg-gradient-to-bl from-[#FFF1B8]/35 via-[#D9B978]/15 to-transparent rounded-tr-3xl pointer-events-none blur-sm" />

        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#0F3D30] pb-3 relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-b from-[#3B2F13] via-[#241A08] to-[#0D0A03] border border-[#D9B978] shadow-[0_0_12px_rgba(217,185,120,0.35)] flex items-center justify-center text-[#E2C284]">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-serif text-base sm:text-lg font-normal text-warm-ivory tracking-wide">Human Approval Gate</h3>
              <p className="text-[11px] text-[#8E9F97]">Review run ID: <code className="text-[#3AD89A]">{runId}</code></p>
            </div>
          </div>
          <button onClick={onClose} className="w-8 h-8 rounded-full bg-[#031811] border border-[#0F3D30] flex items-center justify-center text-[#8E9F97] hover:text-warm-ivory hover:border-[#D9B978] transition-colors cursor-pointer">
            <X className="w-4 h-4" />
          </button>
        </div>

        <p className="text-xs text-[#8E9F97] leading-relaxed relative z-10">
          As required by Agentic AI safety rules, final research reports require explicit human approval before being published.
        </p>

        {/* Decision Radio Grid */}
        <div className="space-y-2.5 relative z-10">
          {decisions.map((d) => {
            const Icon = d.icon;
            const isSelected = selectedDecision === d.id;

            return (
              <div
                key={d.id}
                onClick={() => setSelectedDecision(d.id)}
                className={`p-3.5 rounded-2xl border cursor-pointer transition-all flex items-start gap-3.5 ${
                  isSelected
                    ? 'bg-gradient-to-r from-[#0E4838] to-[#041D16] border-[#3AD89A] shadow-[0_0_15px_rgba(58,216,154,0.3)]'
                    : 'bg-[#031811] border-[#0F3D30] hover:border-[#D9B978]/50'
                }`}
              >
                <div
                  className={`w-7 h-7 rounded-xl flex items-center justify-center mt-0.5 shrink-0 ${
                    isSelected ? 'bg-[#3AD89A]/20 text-[#3AD89A]' : 'bg-[#06241B] text-[#8E9F97]'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-xs font-bold text-warm-ivory tracking-wide">{d.title}</h4>
                  <p className="text-[11px] text-[#8E9F97] mt-0.5">{d.desc}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Action Controls */}
        <div className="flex items-center justify-end gap-3 pt-3 border-t border-[#0F3D30] relative z-10">
          <button onClick={onClose} className="px-4 py-2 rounded-xl text-xs font-medium text-[#8E9F97] hover:text-warm-ivory transition-colors cursor-pointer">
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="px-6 py-2.5 rounded-2xl bg-gradient-to-r from-[#F5D782] via-[#D9B978] to-[#C4A35F] text-[#020B08] font-bold text-xs shadow-[0_8px_25px_rgba(217,185,120,0.45)] hover:shadow-[0_12px_35px_rgba(217,185,120,0.65)] hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer border border-[#FFFDF7]/40"
          >
            Confirm Decision
          </button>
        </div>
      </div>
    </div>
  );
}
