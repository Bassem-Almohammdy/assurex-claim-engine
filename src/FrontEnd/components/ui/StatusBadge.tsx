import type { ClaimStatus, WarrantyStatus, RuleStatus, FinalDecision } from '@/types';
import { CheckCircle2, XCircle, AlertCircle, Clock, ShieldCheck, ShieldAlert, ShieldX } from 'lucide-react';

type BadgeType = ClaimStatus | WarrantyStatus | RuleStatus | FinalDecision;

interface StatusBadgeProps {
  status: BadgeType;
  size?: 'sm' | 'md';
}

const config: Record<string, { bg: string; text: string; icon: typeof CheckCircle2 }> = {
  'Valid': { bg: 'bg-emerald-50', text: 'text-emerald-700', icon: CheckCircle2 },
  'Invalid': { bg: 'bg-red-50', text: 'text-red-700', icon: XCircle },
  'Manual Review': { bg: 'bg-amber-50', text: 'text-amber-700', icon: AlertCircle },
  'Pending': { bg: 'bg-slate-100', text: 'text-slate-600', icon: Clock },
  'Active': { bg: 'bg-emerald-50', text: 'text-emerald-700', icon: ShieldCheck },
  'Expiring': { bg: 'bg-amber-50', text: 'text-amber-700', icon: ShieldAlert },
  'Expired': { bg: 'bg-red-50', text: 'text-red-700', icon: ShieldX },
  'Passed': { bg: 'bg-emerald-50', text: 'text-emerald-700', icon: CheckCircle2 },
  'Warning': { bg: 'bg-amber-50', text: 'text-amber-700', icon: AlertCircle },
  'Failed': { bg: 'bg-red-50', text: 'text-red-700', icon: XCircle },
  'Likely Valid': { bg: 'bg-emerald-50', text: 'text-emerald-700', icon: CheckCircle2 },
  'Likely Invalid': { bg: 'bg-red-50', text: 'text-red-700', icon: XCircle },
  'Manual Review Required': { bg: 'bg-amber-50', text: 'text-amber-700', icon: AlertCircle },
};

export default function StatusBadge({ status, size = 'md' }: StatusBadgeProps) {
  const c = config[status] ?? config['Pending'];
  const Icon = c.icon;
  const sizeClass = size === 'sm' ? 'px-2 py-0.5 text-xs gap-1' : 'px-2.5 py-1 text-xs gap-1.5';
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full font-medium ${c.bg} ${c.text} ${sizeClass}`}>
      <Icon className={size === 'sm' ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
      {status}
    </span>
  );
}
