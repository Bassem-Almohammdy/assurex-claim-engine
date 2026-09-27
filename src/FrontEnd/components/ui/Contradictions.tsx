import { AlertTriangle } from 'lucide-react';
import type { ContradictionItem } from '@/types';

interface ContradictionsProps {
  contradictions: ContradictionItem[];
}

const severityConfig = {
  High: { color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' },
  Medium: { color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200' },
  Low: { color: 'text-slate-600', bg: 'bg-slate-50', border: 'border-slate-200' },
};

export default function Contradictions({ contradictions }: ContradictionsProps) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-red-50 flex items-center justify-center">
            <AlertTriangle className="w-5 h-5 text-red-600" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-sm">Detected Contradictions</h3>
            <p className="text-xs text-slate-400">
              {contradictions.length === 0 ? 'No contradictions detected' : `${contradictions.length} contradiction(s) found`}
            </p>
          </div>
        </div>
      </div>

      {contradictions.length === 0 ? (
        <div className="p-5">
          <div className="flex items-center gap-2 p-3 bg-emerald-50 rounded-lg">
            <span className="text-sm text-emerald-700 font-medium">No contradictions detected in the submitted claim data.</span>
          </div>
        </div>
      ) : (
        <div className="p-4 space-y-2">
          {contradictions.map((c) => {
            const config = severityConfig[c.severity];
            return (
              <div key={c.id} className={`flex items-start gap-3 p-3 ${config.bg} border ${config.border} rounded-lg`}>
                <AlertTriangle className={`w-4 h-4 ${config.color} mt-0.5 flex-shrink-0`} />
                <div className="flex-1">
                  <p className="text-sm text-slate-700">{c.description}</p>
                  <span className={`text-xs font-medium ${config.color} mt-1 inline-block`}>Severity: {c.severity}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="px-5 py-3 border-t border-slate-100 bg-slate-50/30">
        <p className="text-xs text-slate-400 italic">Mock data — will be replaced with real contradiction detection in Phase 2</p>
      </div>
    </div>
  );
}
