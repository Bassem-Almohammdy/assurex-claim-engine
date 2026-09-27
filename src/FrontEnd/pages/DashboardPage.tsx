import { Link } from 'react-router-dom';
import {
  ClipboardList,
  CheckCircle2,
  XCircle,
  AlertCircle,
  ShieldCheck,
  ShieldAlert,
  FilePlus,
  TrendingUp,
} from 'lucide-react';
import StatCard from '@/components/ui/StatCard';
import ClaimTable from '@/components/ui/ClaimTable';
import PageHeader from '@/components/ui/PageHeader';
import { mockClaims, dashboardStats, claimsAnalytics } from '@/data/mockData';

export default function DashboardPage() {
  const recentClaims = mockClaims.slice(0, 5);
  const maxTotal = Math.max(...claimsAnalytics.map((a) => a.valid + a.invalid + a.review));

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Dashboard"
        subtitle="Overview of warranty claims and system activity"
        action={
          <Link
            to="/claims/new"
            className="inline-flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors"
          >
            <FilePlus className="w-4 h-4" />
            New Claim
          </Link>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <StatCard label="Total Claims" value={dashboardStats.totalClaims} icon={ClipboardList} color="brand" trend={{ value: '+12%', direction: 'up' }} />
        <StatCard label="Valid Claims" value={dashboardStats.validClaims} icon={CheckCircle2} color="green" trend={{ value: '+8%', direction: 'up' }} />
        <StatCard label="Invalid Claims" value={dashboardStats.invalidClaims} icon={XCircle} color="red" trend={{ value: '-3%', direction: 'down' }} />
        <StatCard label="Manual Reviews" value={dashboardStats.manualReviews} icon={AlertCircle} color="amber" />
        <StatCard label="Active Warranties" value={dashboardStats.activeWarranties} icon={ShieldCheck} color="teal" />
        <StatCard label="Expiring Warranties" value={dashboardStats.expiringWarranties} icon={ShieldAlert} color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-card">
          <div className="px-5 py-4 border-b border-slate-100">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold text-slate-800">Recent Claims</h2>
              <Link to="/claims" className="text-sm text-brand-600 hover:text-brand-700 font-medium">
                View all →
              </Link>
            </div>
          </div>
          <ClaimTable claims={recentClaims} />
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-card">
          <div className="px-5 py-4 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-brand-600" />
              <h2 className="font-semibold text-slate-800">Claims Analytics</h2>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">Last 6 months</p>
          </div>
          <div className="p-5">
            <div className="flex items-end justify-between gap-2 h-48">
              {claimsAnalytics.map((data) => {
                const total = data.valid + data.invalid + data.review;
                const heightPct = (total / maxTotal) * 100;
                return (
                  <div key={data.month} className="flex-1 flex flex-col items-center gap-2">
                    <div className="w-full flex flex-col justify-end h-full gap-0.5">
                      <div
                        className="w-full bg-amber-400 rounded-t transition-all duration-700"
                        style={{ height: `${(data.review / total) * heightPct}%` }}
                        title={`Review: ${data.review}`}
                      />
                      <div
                        className="w-full bg-red-400 transition-all duration-700"
                        style={{ height: `${(data.invalid / total) * heightPct}%` }}
                        title={`Invalid: ${data.invalid}`}
                      />
                      <div
                        className="w-full bg-emerald-500 rounded-b transition-all duration-700"
                        style={{ height: `${(data.valid / total) * heightPct}%` }}
                        title={`Valid: ${data.valid}`}
                      />
                    </div>
                    <span className="text-xs text-slate-400 font-medium">{data.month}</span>
                  </div>
                );
              })}
            </div>
            <div className="flex items-center justify-center gap-4 mt-4 pt-3 border-t border-slate-100">
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
                <span className="text-xs text-slate-500">Valid</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-red-400" />
                <span className="text-xs text-slate-500">Invalid</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="w-2.5 h-2.5 rounded-sm bg-amber-400" />
                <span className="text-xs text-slate-500">Review</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
