import { ShieldCheck, Plus } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import { mockWarranties } from '@/data/mockData';

export default function WarrantiesPage() {
  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Warranties"
        subtitle="Track active and expiring warranties"
        action={
          <button className="inline-flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors">
            <Plus className="w-4 h-4" />
            Add Warranty
          </button>
        }
      />

      <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
        <div className="overflow-x-auto scrollbar-thin">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left">
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Warranty ID</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Product</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Status</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Start Date</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">End Date</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Duration</th>
                <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Days Left</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {mockWarranties.map((w) => (
                <tr key={w.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <ShieldCheck className="w-4 h-4 text-slate-400" />
                      <span className="font-medium text-slate-700">{w.id}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{w.productName}</td>
                  <td className="px-4 py-3"><StatusBadge status={w.status} size="sm" /></td>
                  <td className="px-4 py-3 text-slate-500 text-xs">{w.startDate}</td>
                  <td className="px-4 py-3 text-slate-500 text-xs">{w.endDate}</td>
                  <td className="px-4 py-3 text-slate-600">{w.durationMonths} months</td>
                  <td className="px-4 py-3">
                    <span className={`text-sm font-medium ${w.daysRemaining > 0 ? 'text-slate-700' : 'text-red-600'}`}>
                      {w.daysRemaining > 0 ? `${w.daysRemaining} days` : 'Expired'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
