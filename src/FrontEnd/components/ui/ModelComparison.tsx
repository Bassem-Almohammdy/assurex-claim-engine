import { CheckCircle2, XCircle, GitCompare } from 'lucide-react';
import type { ModelComparison } from '@/types';

interface ModelComparisonProps {
  comparison: ModelComparison;
}

export default function ModelComparison({ comparison }: ModelComparisonProps) {
  const consistencyColor =
    comparison.modelConsistency === 'Strong Match' ? 'text-emerald-600 bg-emerald-50' :
    comparison.modelConsistency === 'Moderate Match' ? 'text-amber-600 bg-amber-50' :
    'text-red-600 bg-red-50';

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-violet-50 flex items-center justify-center">
            <GitCompare className="w-5 h-5 text-violet-600" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-sm">Model Comparison</h3>
            <p className="text-xs text-slate-400">Cross-model consistency analysis</p>
          </div>
        </div>
      </div>

      <div className="p-5">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="text-center p-3 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">Python Prediction</p>
            <p className="text-sm font-bold text-slate-800">{comparison.pythonPrediction}</p>
          </div>
          <div className="text-center p-3 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">Teachable Machine</p>
            <p className="text-sm font-bold text-slate-800">{comparison.tmPrediction}</p>
          </div>
        </div>

        <div className="space-y-2.5">
          <ComparisonRow
            label="Prediction Match"
            value={comparison.predictionMatch ? 'Yes' : 'No'}
            positive={comparison.predictionMatch}
          />
          <ComparisonRow
            label="Confidence Difference"
            value={`${comparison.confidenceDifference}%`}
            positive={comparison.confidenceDifference <= 5}
          />
          <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-lg">
            <span className="text-sm text-slate-500">Model Consistency</span>
            <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium ${consistencyColor}`}>
              {comparison.modelConsistency}
            </span>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-100">
          <p className="text-xs text-slate-400 italic">Mock data — will be replaced with real comparison logic in Phase 2</p>
        </div>
      </div>
    </div>
  );
}

function ComparisonRow({ label, value, positive }: { label: string; value: string; positive: boolean }) {
  return (
    <div className="flex items-center justify-between py-2 px-3 bg-slate-50 rounded-lg">
      <span className="text-sm text-slate-500">{label}</span>
      <span className={`inline-flex items-center gap-1.5 text-sm font-medium ${positive ? 'text-emerald-600' : 'text-amber-600'}`}>
        {positive ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
        {value}
      </span>
    </div>
  );
}
