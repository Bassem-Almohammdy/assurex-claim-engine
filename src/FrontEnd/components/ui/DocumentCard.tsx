import { FileText, Image as ImageIcon, X, CheckCircle2, AlertCircle, Loader } from 'lucide-react';
import type { DocumentItem } from '@/types';

interface DocumentCardProps {
  document: DocumentItem;
  onRemove?: (id: string) => void;
}

export default function DocumentCard({ document, onRemove }: DocumentCardProps) {
  return (
    <div className="flex items-center gap-3 p-3 bg-white border border-slate-200 rounded-lg hover:shadow-card transition-all">
      <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-slate-50 flex items-center justify-center">
        {document.fileType === 'image' ? (
          <ImageIcon className="w-5 h-5 text-slate-500" />
        ) : (
          <FileText className="w-5 h-5 text-slate-500" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-slate-700 truncate">{document.name}</p>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>{document.type}</span>
          <span>·</span>
          <span>{document.fileType.toUpperCase()}</span>
          <span>·</span>
          <span>{document.fileSize}</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        {document.uploadStatus === 'Uploaded' && (
          <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600">
            <CheckCircle2 className="w-4 h-4" />
          </span>
        )}
        {document.uploadStatus === 'Pending' && (
          <Loader className="w-4 h-4 text-amber-500 animate-spin" />
        )}
        {document.uploadStatus === 'Failed' && (
          <AlertCircle className="w-4 h-4 text-red-500" />
        )}
        {onRemove && (
          <button
            onClick={() => onRemove(document.id)}
            className="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-red-500 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
}
