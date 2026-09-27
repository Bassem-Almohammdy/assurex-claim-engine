import { useRef, useState } from 'react';
import { UploadCloud, FileText, Image as ImageIcon, X, CheckCircle2, AlertCircle, Loader } from 'lucide-react';
import type { DocumentItem } from '@/types';

interface DocumentUploadProps {
  label: string;
  type: DocumentItem['type'];
  onUpload?: (file: File) => void;
}

interface UploadedFile {
  name: string;
  type: 'image' | 'pdf';
  size: string;
  status: 'Uploaded' | 'Pending' | 'Failed';
}

export default function DocumentUpload({ label, type, onUpload }: DocumentUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState<UploadedFile[]>([]);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const newFiles: UploadedFile[] = Array.from(fileList).map((file) => ({
      name: file.name,
      type: file.type.startsWith('image/') ? 'image' : 'pdf',
      size: file.size > 1024 * 1024 ? `${(file.size / (1024 * 1024)).toFixed(1)} MB` : `${(file.size / 1024).toFixed(0)} KB`,
      status: 'Uploaded' as const,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
    if (onUpload && fileList[0]) onUpload(fileList[0]);
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-2">{label}</label>
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
        className={`relative border-2 border-dashed rounded-xl p-5 text-center cursor-pointer transition-all ${
          isDragging
            ? 'border-brand-400 bg-brand-50'
            : 'border-slate-200 hover:border-brand-300 hover:bg-slate-50'
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*,.pdf"
          multiple
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <UploadCloud className={`w-7 h-7 mx-auto mb-2 ${isDragging ? 'text-brand-500' : 'text-slate-400'}`} />
        <p className="text-sm text-slate-600 font-medium">
          Drag &amp; drop or <span className="text-brand-600">browse</span>
        </p>
        <p className="text-xs text-slate-400 mt-1">Image or PDF · Max 10MB</p>
      </div>

      {files.length > 0 && (
        <div className="mt-3 space-y-2">
          {files.map((file, i) => (
            <div key={i} className="flex items-center gap-3 p-2.5 bg-white border border-slate-200 rounded-lg animate-fade-in">
              <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-slate-50 flex items-center justify-center">
                {file.type === 'image' ? (
                  <ImageIcon className="w-4 h-4 text-slate-500" />
                ) : (
                  <FileText className="w-4 h-4 text-slate-500" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-slate-700 truncate">{file.name}</p>
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <span>{file.type.toUpperCase()}</span>
                  <span>·</span>
                  <span>{file.size}</span>
                  <span>·</span>
                  <span className="text-slate-400">{type}</span>
                </div>
              </div>
              {file.status === 'Uploaded' && (
                <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-600">
                  <CheckCircle2 className="w-4 h-4" />
                </span>
              )}
              {file.status === 'Pending' && (
                <Loader className="w-4 h-4 text-amber-500 animate-spin" />
              )}
              {file.status === 'Failed' && (
                <AlertCircle className="w-4 h-4 text-red-500" />
              )}
              <button
                onClick={() => removeFile(i)}
                className="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-red-500 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
