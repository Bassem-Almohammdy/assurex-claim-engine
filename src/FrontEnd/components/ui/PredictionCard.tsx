import { BrainCircuit, ScanFace } from 'lucide-react';
import type { PredictionResult } from '@/types';
import StatusBadge from './StatusBadge';

interface PredictionCardProps {
  prediction: PredictionResult;
}

export default function PredictionCard({ prediction }: PredictionCardProps) {
  const isPython = prediction.model === 'Python Classification Model';
  const Icon = isPython ? BrainCircuit : ScanFace;

  const bars = [
    { label: 'Valid', value: prediction.validConfidence, color: 'bg-emerald-500' },
    { label: 'Invalid', value: prediction.invalidConfidence, color: 'bg-red-500' },
    { label: 'Manual Review', value: prediction.manualReviewConfidence, color: 'bg-amber-500' },
  ];

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${isPython ? 'bg-brand-50' : 'bg-teal-50'}`}>
              <Icon className={`w-5 h-5 ${isPython ? 'text-brand-600' : 'text-teal-600'}`} />
            </div>
            <div>
              <h3 className="font-semibold text-slate-800 text-sm">{prediction.model}</h3>
              <p className="text-xs text-slate-400">AI Classification Result</p>
            </div>
          </div>
          <StatusBadge status={prediction.prediction} size="sm" />
        </div>
      </div>

      <div className="p-5">
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-xs font-medium text-slate-500">Prediction</span>
            <span className="text-sm font-bold text-slate-800">{prediction.prediction}</span>
          </div>
        </div>

        <div className="space-y-3">
          {bars.map((bar) => (
            <div key={bar.label}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-slate-500">{bar.label}</span>
                <span className="text-xs font-semibold text-slate-700">{bar.value}%</span>
              </div>
              <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${bar.color} rounded-full transition-all duration-700 ease-out`}
                  style={{ width: `${bar.value}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <div className="mt-4 pt-3 border-t border-slate-100">
          <p className="text-xs text-slate-400 italic">Mock data — will be replaced with real model output in Phase 2</p>
        </div>
      </div>
    </div>
  );
}
