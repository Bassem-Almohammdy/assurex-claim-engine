import {
  ShieldCheck,
  ShieldAlert,
  ShieldX,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  FileWarning,
  Wrench,
  Receipt,
  Hash,
} from 'lucide-react';
import type { ClaimSummary } from '@/types';
import StatusBadge from './StatusBadge';

interface ClaimSummaryCardProps {
  summary: ClaimSummary;
}

export default function ClaimSummaryCard({ summary }: ClaimSummaryCardProps) {
  const warrantyIcon =
    summary.warrantyStatus === 'Active' ? ShieldCheck :
    summary.warrantyStatus === 'Expiring' ? ShieldAlert : ShieldX;

  const WarrantyIcon = warrantyIcon;

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-slate-800">Claim Summary</h3>
            <p className="text-xs text-slate-400 mt-0.5">{summary.claimId}</p>
          </div>
          <span className="text-xs text-slate-400 font-mono bg-slate-100 px-2 py-1 rounded">TM Input</span>
        </div>
      </div>

      <div className="p-5 space-y-4">
        <div className="flex items-center gap-3 pb-3 border-b border-slate-100">
          <div className="w-10 h-10 rounded-lg bg-brand-50 flex items-center justify-center">
            <WarrantyIcon className="w-5 h-5 text-brand-600" />
          </div>
          <div className="flex-1">
            <p className="font-medium text-slate-800">{summary.product}</p>
            <p className="text-xs text-slate-400">{summary.productCategory}</p>
          </div>
          <StatusBadge status={summary.warrantyStatus} size="sm" />
        </div>

        <div className="grid grid-cols-2 gap-x-4 gap-y-3">
          <InfoItem label="Product Age" value={summary.productAge} />
          <InfoItem label="Warranty Period" value={summary.warrantyPeriod} />
          <InfoItem label="Fault Type" value={summary.faultType} />
          <InfoItem label="Repair History" value={summary.repairHistory} />
        </div>

        <div className="space-y-2 pt-3 border-t border-slate-100">
          <BooleanItem
            label="Receipt Available"
            value={summary.receiptAvailable}
            icon={Receipt}
          />
          <SerialNumberItem status={summary.serialNumberStatus} />
        </div>

        {summary.missingDocuments.length > 0 && (
          <div className="pt-3 border-t border-slate-100">
            <div className="flex items-center gap-2 mb-2">
              <FileWarning className="w-4 h-4 text-amber-500" />
              <p className="text-xs font-medium text-slate-600">Missing Documents</p>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {summary.missingDocuments.map((doc, i) => (
                <span key={i} className="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-amber-50 text-amber-700 text-xs font-medium">
                  <XCircle className="w-3 h-3" />
                  {doc}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs text-slate-400 mb-0.5">{label}</p>
      <p className="text-sm font-medium text-slate-700">{value}</p>
    </div>
  );
}

function BooleanItem({ label, value, icon: Icon }: { label: string; value: boolean; icon: typeof Receipt }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Icon className="w-4 h-4 text-slate-400" />
        <span className="text-sm text-slate-600">{label}</span>
      </div>
      {value ? (
        <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600">
          <CheckCircle2 className="w-4 h-4" /> Available
        </span>
      ) : (
        <span className="inline-flex items-center gap-1 text-xs font-medium text-red-600">
          <XCircle className="w-4 h-4" /> Missing
        </span>
      )}
    </div>
  );
}

function SerialNumberItem({ status }: { status: 'Verified' | 'Unverified' | 'Mismatch' }) {
  const Icon = Hash;
  const colorClass =
    status === 'Verified' ? 'text-emerald-600' :
    status === 'Mismatch' ? 'text-red-600' : 'text-amber-600';
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Icon className="w-4 h-4 text-slate-400" />
        <span className="text-sm text-slate-600">Serial Number</span>
      </div>
      <span className={`inline-flex items-center gap-1 text-xs font-medium ${colorClass}`}>
        {status === 'Verified' ? <CheckCircle2 className="w-4 h-4" /> :
         status === 'Mismatch' ? <XCircle className="w-4 h-4" /> : <AlertTriangle className="w-4 h-4" />}
        {status}
      </span>
    </div>
  );
}
