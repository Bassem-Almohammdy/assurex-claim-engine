import { FileWarning, XCircle } from 'lucide-react';

interface MissingDocumentsProps {
  documents: string[];
}

export default function MissingDocuments({ documents }: MissingDocumentsProps) {
  if (documents.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 shadow-card p-5">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-50 flex items-center justify-center">
            <FileWarning className="w-5 h-5 text-emerald-600" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-sm">Missing Documents</h3>
            <p className="text-xs text-slate-400">All required documents provided</p>
          </div>
        </div>
        <div className="flex items-center gap-2 p-3 bg-emerald-50 rounded-lg">
          <XCircle className="w-4 h-4 text-emerald-600" />
          <span className="text-sm text-emerald-700 font-medium">No missing documents detected.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
      <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-50 flex items-center justify-center">
            <FileWarning className="w-5 h-5 text-amber-600" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-800 text-sm">Missing Documents</h3>
            <p className="text-xs text-slate-400">{documents.length} document(s) required</p>
          </div>
        </div>
      </div>
      <div className="p-4 space-y-2">
        {documents.map((doc, i) => (
          <div key={i} className="flex items-center gap-3 p-3 bg-amber-50/50 border border-amber-100 rounded-lg">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-amber-100 flex items-center justify-center">
              <XCircle className="w-4 h-4 text-amber-600" />
            </div>
            <span className="text-sm font-medium text-slate-700">{doc}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
