import { CopyCheck, CopyX } from 'lucide-react';

interface DuplicateIndicatorProps {
  status: string;
}

export default function DuplicateIndicator({ status }: DuplicateIndicatorProps) {
  const isClean = status.toLowerCase().includes('no possible duplicate') || status.toLowerCase().includes('no duplicate');

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${isClean ? 'bg-emerald-50' : 'bg-red-50'}`}>
            {isClean ? <CopyCheck className="w-5 h-5 text-emerald-600" /> : <CopyX className="w-5 h-5 text-red-600" />}
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-sm">Duplicate Claim Check</h3>
            <p className="text-xs text-slate-400">Cross-reference against existing claims</p>
          </div>
        </div>
      </div>

      <div className="p-5">
        <div className={`flex items-center gap-3 p-4 rounded-lg ${isClean ? 'bg-emerald-50' : 'bg-red-50'}`}>
          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isClean ? 'bg-emerald-100' : 'bg-red-100'}`}>
            {isClean ? <CopyCheck className="w-4 h-4 text-emerald-600" /> : <CopyX className="w-4 h-4 text-red-600" />}
          </div>
          <div>
            <p className="text-xs text-slate-400 mb-0.5">Status</p>
            <p className={`text-sm font-medium ${isClean ? 'text-emerald-700' : 'text-red-700'}`}>{status}</p>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-slate-100">
          <p className="text-xs text-slate-400 italic">Mock data — will be replaced with real duplicate detection in Phase 2</p>
        </div>
      </div>
    </div>
  );
}
