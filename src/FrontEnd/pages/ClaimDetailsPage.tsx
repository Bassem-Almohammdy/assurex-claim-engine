import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Package, FileText, User, Calendar, DollarSign, Hash, Wrench, Building2 } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import StatusBadge from '@/components/ui/StatusBadge';
import ClaimSummaryCard from '@/components/ui/ClaimSummaryCard';
import DocumentCard from '@/components/ui/DocumentCard';
import PredictionCard from '@/components/ui/PredictionCard';
import ModelComparison from '@/components/ui/ModelComparison';
import WarrantyRuleList from '@/components/ui/WarrantyRuleList';
import MissingDocuments from '@/components/ui/MissingDocuments';
import Contradictions from '@/components/ui/Contradictions';
import DuplicateIndicator from '@/components/ui/DuplicateIndicator';
import FinalDecisionCard from '@/components/ui/FinalDecisionCard';
import { mockClaims } from '@/data/mockData';

export default function ClaimDetailsPage() {
  const { id } = useParams<{ id: string }>();
  const claim = mockClaims.find((c) => c.id === id);

  if (!claim) {
    return (
      <div className="animate-fade-in">
        <PageHeader title="Claim Not Found" />
        <div className="bg-white rounded-xl border border-slate-200 shadow-card p-8 text-center">
          <p className="text-slate-500">The claim you are looking for does not exist.</p>
          <Link to="/claims" className="inline-flex items-center gap-2 mt-4 text-brand-600 hover:text-brand-700 font-medium text-sm">
            <ArrowLeft className="w-4 h-4" /> Back to Claims
          </Link>
        </div>
      </div>
    );
  }

  const infoItems = [
    { icon: User, label: 'Customer', value: claim.customer },
    { icon: User, label: 'Email', value: claim.customerEmail },
    { icon: Calendar, label: 'Submission Date', value: claim.submittedDate },
    { icon: Calendar, label: 'Fault Occurrence', value: claim.faultOccurrenceDate },
  ];

  const productItems = [
    { icon: Package, label: 'Product', value: claim.product },
    { icon: Package, label: 'Category', value: claim.productCategory },
    { icon: Hash, label: 'Brand', value: claim.brand },
    { icon: Hash, label: 'Model Number', value: claim.modelNumber },
    { icon: Hash, label: 'Serial Number', value: claim.serialNumber },
    { icon: Calendar, label: 'Purchase Date', value: claim.purchaseDate },
    { icon: DollarSign, label: 'Purchase Price', value: `$${claim.purchasePrice.toLocaleString()}` },
    { icon: Wrench, label: 'Warranty Duration', value: `${claim.warrantyDurationMonths} months` },
    { icon: Wrench, label: 'Damage Type', value: claim.damageType },
    { icon: Wrench, label: 'Previous Repairs', value: claim.previousRepairs },
    { icon: Building2, label: 'Service Center', value: claim.serviceCenter },
  ];

  return (
    <div className="animate-fade-in">
      <PageHeader
        title={`Claim ${claim.id}`}
        subtitle="Detailed claim review and AI analysis"
        action={
          <Link
            to="/claims"
            className="inline-flex items-center gap-2 px-3.5 py-2 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </Link>
        }
      />

      {/* Claim Overview */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden mb-6">
        <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
          <h2 className="font-semibold text-slate-800 text-sm">Claim Overview</h2>
        </div>
        <div className="p-5">
          <div className="flex flex-wrap items-center gap-3 mb-5">
            <span className="text-lg font-bold text-slate-800">{claim.id}</span>
            <StatusBadge status={claim.status} />
            <StatusBadge status={claim.warrantyStatus} />
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {infoItems.map((item, i) => {
              const Icon = item.icon;
              return (
                <div key={i} className="flex items-center gap-3">
                  <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-slate-50 flex items-center justify-center">
                    <Icon className="w-4 h-4 text-slate-500" />
                  </div>
                  <div>
                    <p className="text-xs text-slate-400">{item.label}</p>
                    <p className="text-sm font-medium text-slate-700">{item.value}</p>
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-4 p-4 bg-slate-50 rounded-lg">
            <p className="text-xs text-slate-400 mb-1">Fault Description</p>
            <p className="text-sm text-slate-600">{claim.faultDescription}</p>
          </div>
        </div>
      </div>

      {/* Product Information */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden mb-6">
        <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-brand-50 flex items-center justify-center">
              <Package className="w-4.5 h-4.5 text-brand-600" />
            </div>
            <h2 className="font-semibold text-slate-800 text-sm">Product Information</h2>
          </div>
        </div>
        <div className="p-5 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {productItems.map((item, i) => {
            const Icon = item.icon;
            return (
              <div key={i}>
                <div className="flex items-center gap-1.5 mb-1">
                  <Icon className="w-3.5 h-3.5 text-slate-400" />
                  <p className="text-xs text-slate-400">{item.label}</p>
                </div>
                <p className="text-sm font-medium text-slate-700">{item.value}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Documents */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden mb-6">
        <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-teal-50 flex items-center justify-center">
              <FileText className="w-4.5 h-4.5 text-teal-600" />
            </div>
            <div>
              <h2 className="font-semibold text-slate-800 text-sm">Uploaded Documents</h2>
              <p className="text-xs text-slate-400">{claim.documents.length} document(s) attached</p>
            </div>
          </div>
        </div>
        <div className="p-5">
          {claim.documents.length === 0 ? (
            <p className="text-sm text-slate-400 text-center py-4">No documents uploaded for this claim.</p>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {claim.documents.map((doc) => (
                <DocumentCard key={doc.id} document={doc} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Claim Summary Card + AI Results */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <ClaimSummaryCard summary={claim.summary} />
        <div className="space-y-6">
          <PredictionCard prediction={claim.pythonPrediction} />
          <PredictionCard prediction={claim.tmPrediction} />
        </div>
      </div>

      {/* Model Comparison */}
      <div className="mb-6">
        <ModelComparison comparison={claim.comparison} />
      </div>

      {/* Warranty Rules + Missing Documents */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <WarrantyRuleList rules={claim.rules} />
        <div className="space-y-6">
          <MissingDocuments documents={claim.summary.missingDocuments} />
          <Contradictions contradictions={claim.contradictions} />
          <DuplicateIndicator status={claim.duplicateStatus} />
        </div>
      </div>

      {/* Final Decision */}
      <div className="max-w-2xl">
        <FinalDecisionCard decision={claim.finalDecision} />
      </div>
    </div>
  );
}
