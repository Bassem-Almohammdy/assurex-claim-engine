import type { LucideIcon } from 'lucide-react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  color: 'brand' | 'green' | 'red' | 'amber' | 'teal' | 'purple';
  trend?: { value: string; direction: 'up' | 'down' };
  subtitle?: string;
}

const colorMap = {
  brand: { bg: 'bg-brand-50', icon: 'bg-brand-500', text: 'text-brand-700' },
  green: { bg: 'bg-emerald-50', icon: 'bg-emerald-500', text: 'text-emerald-700' },
  red: { bg: 'bg-red-50', icon: 'bg-red-500', text: 'text-red-700' },
  amber: { bg: 'bg-amber-50', icon: 'bg-amber-500', text: 'text-amber-700' },
  teal: { bg: 'bg-teal-50', icon: 'bg-teal-500', text: 'text-teal-700' },
  purple: { bg: 'bg-violet-50', icon: 'bg-violet-500', text: 'text-violet-700' },
};

export default function StatCard({ label, value, icon: Icon, color, trend, subtitle }: StatCardProps) {
  const colors = colorMap[color];
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card hover:shadow-card-hover transition-all duration-200 p-5 group">
      <div className="flex items-start justify-between mb-3">
        <div className={`w-11 h-11 rounded-lg ${colors.bg} flex items-center justify-center`}>
          <Icon className={`w-5 h-5 ${colors.text}`} />
        </div>
        {trend && (
          <div className={`flex items-center gap-1 text-xs font-medium ${trend.direction === 'up' ? 'text-emerald-600' : 'text-red-600'}`}>
            {trend.direction === 'up' ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
            {trend.value}
          </div>
        )}
      </div>
      <p className="text-2xl font-bold text-slate-800 tracking-tight">{value}</p>
      <p className="text-sm text-slate-500 mt-1">{label}</p>
      {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
    </div>
  );
}
