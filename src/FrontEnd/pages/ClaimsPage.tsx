import { useState } from 'react';
import { Link } from 'react-router-dom';
import { FilePlus, Search, Filter } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import ClaimTable from '@/components/ui/ClaimTable';
import EmptyState from '@/components/ui/EmptyState';
import StatusBadge from '@/components/ui/StatusBadge';
import { mockClaims } from '@/data/mockData';
import type { ClaimStatus } from '@/types';

const statusFilters: (ClaimStatus | 'All')[] = ['All', 'Valid', 'Invalid', 'Manual Review', 'Pending'];

export default function ClaimsPage() {
  const [filter, setFilter] = useState<ClaimStatus | 'All'>('All');
  const [search, setSearch] = useState('');

  const filtered = mockClaims.filter((c) => {
    const matchesStatus = filter === 'All' || c.status === filter;
    const matchesSearch = !search ||
      c.id.toLowerCase().includes(search.toLowerCase()) ||
      c.product.toLowerCase().includes(search.toLowerCase()) ||
      c.customer.toLowerCase().includes(search.toLowerCase());
    return matchesStatus && matchesSearch;
  });

  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Claims"
        subtitle="Manage and review all warranty claims"
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

      <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div className="flex items-center gap-2 flex-wrap">
            <Filter className="w-4 h-4 text-slate-400" />
            {statusFilters.map((s) => (
              <button
                key={s}
                onClick={() => setFilter(s)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  filter === s
                    ? 'bg-brand-600 text-white'
                    : 'bg-slate-50 text-slate-600 hover:bg-slate-100'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
          <div className="relative sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search claims..."
              className="w-full pl-10 pr-4 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-400"
            />
          </div>
        </div>

        <div className="px-5 py-3 border-b border-slate-100 flex items-center gap-4 text-xs text-slate-400">
          <span>{filtered.length} claim(s) found</span>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1"><StatusBadge status="Valid" size="sm" /></span>
            <span className="flex items-center gap-1"><StatusBadge status="Invalid" size="sm" /></span>
            <span className="flex items-center gap-1"><StatusBadge status="Manual Review" size="sm" /></span>
            <span className="flex items-center gap-1"><StatusBadge status="Pending" size="sm" /></span>
          </div>
        </div>

        {filtered.length === 0 ? (
          <EmptyState
            title="No claims found"
            description="Try adjusting your filters or search query."
            action={
              <Link to="/claims/new" className="inline-flex items-center gap-2 px-4 py-2 bg-brand-600 text-white text-sm rounded-lg hover:bg-brand-700">
                <FilePlus className="w-4 h-4" /> New Claim
              </Link>
            }
          />
        ) : (
          <ClaimTable claims={filtered} />
        )}
      </div>
    </div>
  );
}
