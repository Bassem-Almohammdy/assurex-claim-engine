import type { PredictionResult } from '@/types';

interface ConfidenceChartProps {
  prediction: PredictionResult;
}

export default function ConfidenceChart({ prediction }: ConfidenceChartProps) {
  const segments = [
    { label: 'Valid', value: prediction.validConfidence, color: 'bg-emerald-500' },
    { label: 'Invalid', value: prediction.invalidConfidence, color: 'bg-red-500' },
    { label: 'Manual Review', value: prediction.manualReviewConfidence, color: 'bg-amber-500' },
  ];

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card p-5">
      <h4 className="text-sm font-semibold text-slate-700 mb-4">Confidence Distribution</h4>
      <div className="flex h-3 rounded-full overflow-hidden">
        {segments.map((seg) => (
          <div
            key={seg.label}
            className={`${seg.color} transition-all duration-700 ease-out`}
            style={{ width: `${seg.value}%` }}
            title={`${seg.label}: ${seg.value}%`}
          />
        ))}
      </div>
      <div className="flex items-center justify-between mt-3">
        {segments.map((seg) => (
          <div key={seg.label} className="flex items-center gap-1.5">
            <span className={`w-2.5 h-2.5 rounded-sm ${seg.color}`} />
            <span className="text-xs text-slate-500">{seg.label}</span>
            <span className="text-xs font-semibold text-slate-700">{seg.value}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}
