import { CheckCircle2, AlertCircle, XCircle, ShieldCheck } from 'lucide-react';
import type { WarrantyRule } from '@/types';

interface WarrantyRuleListProps {
  rules: WarrantyRule[];
}

const statusConfig = {
  Passed: { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' },
  Warning: { icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-200' },
  Failed: { icon: XCircle, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-200' },
};

export default function WarrantyRuleList({ rules }: WarrantyRuleListProps) {
  const passedCount = rules.filter((r) => r.status === 'Passed').length;
  const warningCount = rules.filter((r) => r.status === 'Warning').length;
  const failedCount = rules.filter((r) => r.status === 'Failed').length;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-brand-50 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5 text-brand-600" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-800 text-sm">Warranty Rules</h3>
              <p className="text-xs text-slate-400">Automated rule engine checks</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-medium">{passedCount} Passed</span>
            {warningCount > 0 && <span className="px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 font-medium">{warningCount} Warning</span>}
            {failedCount > 0 && <span className="px-2 py-0.5 rounded-full bg-red-50 text-red-700 font-medium">{failedCount} Failed</span>}
          </div>
        </div>
      </div>

      <div className="divide-y divide-slate-100">
        {rules.map((rule) => {
          const config = statusConfig[rule.status];
          const Icon = config.icon;
          return (
            <div key={rule.id} className="flex items-start gap-3 px-5 py-3.5 hover:bg-slate-50/50 transition-colors">
              <div className={`flex-shrink-0 w-7 h-7 rounded-lg ${config.bg} flex items-center justify-center mt-0.5`}>
                <Icon className={`w-4 h-4 ${config.color}`} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-slate-700">{rule.name}</p>
                  <span className={`text-xs font-semibold ${config.color}`}>{rule.status}</span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">{rule.message}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="px-5 py-3 border-t border-slate-100 bg-slate-50/30">
        <p className="text-xs text-slate-400 italic">Mock data — will be replaced with real rule engine results in Phase 2</p>
      </div>
    </div>
  );
}
