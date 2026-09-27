import { Link } from 'react-router-dom';
import { Eye } from 'lucide-react';
import type { Claim } from '@/types';
import StatusBadge from './StatusBadge';

interface ClaimTableProps {
  claims: Claim[];
  showAction?: boolean;
}

export default function ClaimTable({ claims, showAction = true }: ClaimTableProps) {
  return (
    <div className="overflow-x-auto scrollbar-thin">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-left">
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Claim ID</th>
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Product</th>
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Customer</th>
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Status</th>
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Warranty</th>
            <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider">Submitted Date</th>
            {showAction && <th className="px-4 py-3 font-medium text-slate-500 text-xs uppercase tracking-wider text-right">Action</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {claims.map((claim) => (
            <tr key={claim.id} className="hover:bg-slate-50 transition-colors">
              <td className="px-4 py-3">
                <Link to={`/claims/${claim.id}`} className="font-medium text-brand-600 hover:text-brand-700">
                  {claim.id}
                </Link>
              </td>
              <td className="px-4 py-3">
                <div className="font-medium text-slate-700">{claim.product}</div>
                <div className="text-xs text-slate-400">{claim.productCategory}</div>
              </td>
              <td className="px-4 py-3 text-slate-600">{claim.customer}</td>
              <td className="px-4 py-3"><StatusBadge status={claim.status} size="sm" /></td>
              <td className="px-4 py-3"><StatusBadge status={claim.warrantyStatus} size="sm" /></td>
              <td className="px-4 py-3 text-slate-500 text-xs">{claim.submittedDate}</td>
              {showAction && (
                <td className="px-4 py-3 text-right">
                  <Link
                    to={`/claims/${claim.id}`}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-50 hover:bg-brand-50 text-slate-600 hover:text-brand-600 text-xs font-medium transition-colors"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    View
                  </Link>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
