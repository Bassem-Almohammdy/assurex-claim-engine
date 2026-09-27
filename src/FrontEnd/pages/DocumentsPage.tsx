import { FileText, Plus } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import DocumentCard from '@/components/ui/DocumentCard';
import EmptyState from '@/components/ui/EmptyState';
import { mockDocuments } from '@/data/mockData';

export default function DocumentsPage() {
  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Documents"
        subtitle="All uploaded documents across claims"
        action={
          <button className="inline-flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors">
            <Plus className="w-4 h-4" />
            Upload Document
          </button>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {mockDocuments.map((doc) => (
          <DocumentCard key={doc.id} document={doc} />
        ))}
      </div>

      <div className="mt-6">
        <EmptyState
          icon={<FileText className="w-7 h-7 text-slate-400" />}
          title="More documents will appear here"
          description="Documents uploaded through claims will be listed in this section."
        />
      </div>
    </div>
  );
}
