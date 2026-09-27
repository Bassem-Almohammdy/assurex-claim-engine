import { TrendingUp, BarChart3, PieChart, Activity } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import StatCard from '@/components/ui/StatCard';
import { dashboardStats, claimsAnalytics, mockClaims } from '@/data/mockData';

export default function AnalyticsPage() {
  const maxTotal = Math.max(...claimsAnalytics.map((a) => a.valid + a.invalid + a.review));
  const totalValid = claimsAnalytics.reduce((sum, a) => sum + a.valid, 0);
  const totalInvalid = claimsAnalytics.reduce((sum, a) => sum + a.invalid, 0);
  const totalReview = claimsAnalytics.reduce((sum, a) => sum + a.review, 0);
  const grandTotal = totalValid + totalInvalid + totalReview;
  const validPct = Math.round((totalValid / grandTotal) * 100);
  const invalidPct = Math.round((totalInvalid / grandTotal) * 100);
  const reviewPct = 100 - validPct - invalidPct;

  const categoryCounts = mockClaims.reduce((acc, c) => {
    acc[c.productCategory] = (acc[c.productCategory] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="animate-fade-in">
      <PageHeader title="Analytics" subtitle="Insights and trends across warranty claims" />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Processed" value={grandTotal} icon={Activity} color="brand" trend={{ value: '+15%', direction: 'up' }} />
        <StatCard label="Valid Rate" value={`${validPct}%`} icon={TrendingUp} color="green" trend={{ value: '+4%', direction: 'up' }} />
        <StatCard label="Invalid Rate" value={`${invalidPct}%`} icon={BarChart3} color="red" trend={{ value: '-2%', direction: 'down' }} />
        <StatCard label="Review Rate" value={`${reviewPct}%`} icon={PieChart} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl border border-slate-200 shadow-card p-5">
          <h3 className="font-semibold text-slate-800 text-sm mb-4">Monthly Claims Breakdown</h3>
          <div className="flex items-end justify-between gap-2 h-56">
            {claimsAnalytics.map((data) => {
              const total = data.valid + data.invalid + data.review;
              const heightPct = (total / maxTotal) * 100;
              return (
                <div key={data.month} className="flex-1 flex flex-col items-center gap-2">
                  <div className="w-full flex flex-col justify-end h-full gap-0.5">
                    <div className="w-full bg-amber-400 rounded-t transition-all duration-700" style={{ height: `${(data.review / total) * heightPct}%` }} />
                    <div className="w-full bg-red-400 transition-all duration-700" style={{ height: `${(data.invalid / total) * heightPct}%` }} />
                    <div className="w-full bg-emerald-500 rounded-b transition-all duration-700" style={{ height: `${(data.valid / total) * heightPct}%` }} />
                  </div>
                  <span className="text-xs text-slate-400 font-medium">{data.month}</span>
                </div>
              );
            })}
          </div>
          <div className="flex items-center justify-center gap-4 mt-4 pt-3 border-t border-slate-100">
            <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-emerald-500" /><span className="text-xs text-slate-500">Valid</span></div>
            <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-red-400" /><span className="text-xs text-slate-500">Invalid</span></div>
            <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-amber-400" /><span className="text-xs text-slate-500">Review</span></div>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-card p-5">
          <h3 className="font-semibold text-slate-800 text-sm mb-4">Claims by Product Category</h3>
          <div className="space-y-3">
            {Object.entries(categoryCounts).map(([category, count]) => {
              const pct = (count / mockClaims.length) * 100;
              return (
                <div key={category}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-600">{category}</span>
                    <span className="text-xs font-semibold text-slate-700">{count}</span>
                  </div>
                  <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                    <div className="h-full bg-brand-500 rounded-full transition-all duration-700" style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-card p-5">
        <h3 className="font-semibold text-slate-800 text-sm mb-4">Summary Statistics</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400">Active Warranties</p>
            <p className="text-xl font-bold text-slate-800 mt-1">{dashboardStats.activeWarranties}</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400">Expiring Soon</p>
            <p className="text-xl font-bold text-amber-600 mt-1">{dashboardStats.expiringWarranties}</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400">Expired</p>
            <p className="text-xl font-bold text-red-600 mt-1">{dashboardStats.expiredWarranties}</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400">Pending Review</p>
            <p className="text-xl font-bold text-slate-800 mt-1">{dashboardStats.pendingClaims}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
