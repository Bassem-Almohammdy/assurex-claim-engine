import { CheckCircle2, XCircle, AlertCircle, Sparkles } from 'lucide-react';
import type { FinalDecision } from '@/types';

interface FinalDecisionCardProps {
  decision: FinalDecision;
}

const decisionConfig = {
  'Likely Valid': {
    icon: CheckCircle2,
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
    gradient: 'from-emerald-500 to-emerald-600',
    description: 'The claim meets all warranty criteria and is recommended for approval.',
  },
  'Likely Invalid': {
    icon: XCircle,
    color: 'text-red-600',
    bg: 'bg-red-50',
    border: 'border-red-200',
    gradient: 'from-red-500 to-red-600',
    description: 'The claim does not meet warranty requirements and is recommended for rejection.',
  },
  'Manual Review Required': {
    icon: AlertCircle,
    color: 'text-amber-600',
    bg: 'bg-amber-50',
    border: 'border-amber-200',
    gradient: 'from-amber-500 to-amber-600',
    description: 'The claim requires manual review by a warranty analyst before a decision can be made.',
  },
};

export default function FinalDecisionCard({ decision }: FinalDecisionCardProps) {
  const config = decisionConfig[decision];
  const Icon = config.icon;

  return (
    <div className={`rounded-xl border-2 ${config.border} shadow-card overflow-hidden`}>
      <div className={`px-5 py-4 ${config.bg}`}>
        <div className="flex items-center gap-3">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${config.gradient} flex items-center justify-center shadow-sm`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-slate-400" />
              <p className="text-xs text-slate-500 font-medium">Final Decision</p>
            </div>
            <p className={`text-lg font-bold ${config.color}`}>{decision}</p>
          </div>
        </div>
      </div>
      <div className="p-5 bg-white">
        <p className="text-sm text-slate-600">{config.description}</p>
        <div className="mt-4 pt-3 border-t border-slate-100">
          <p className="text-xs text-slate-400 italic">
            Mock decision — will be replaced with real decision logic in Phase 2
          </p>
        </div>
      </div>
    </div>
  );
}
