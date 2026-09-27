import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Package, FileText, Upload } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import DocumentUpload from '@/components/ui/DocumentUpload';

const categories = ['Smartphone', 'Laptop', 'Audio', 'Television', 'Home Appliance', 'Gaming Console', 'Camera', 'Wearable'];
const damageTypes = ['Display malfunction', 'Audio malfunction', 'Hardware malfunction', 'Physical damage', 'Software issue', 'Battery issue', 'Connectivity issue', 'Other'];

export default function NewClaimPage() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      navigate('/claims');
    }, 1200);
  };

  const inputClass = 'w-full px-3.5 py-2.5 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-400 transition-colors';
  const labelClass = 'block text-sm font-medium text-slate-700 mb-1.5';

  return (
    <div className="animate-fade-in max-w-4xl">
      <PageHeader title="New Claim" subtitle="Submit a new warranty claim for validation" />

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Product Information */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-brand-50 flex items-center justify-center">
                <Package className="w-4.5 h-4.5 text-brand-600" />
              </div>
              <div>
                <h2 className="font-semibold text-slate-800 text-sm">Product Information</h2>
                <p className="text-xs text-slate-400">Details about the product under warranty</p>
              </div>
            </div>
          </div>
          <div className="p-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>Product Category</label>
              <select className={inputClass} required>
                <option value="">Select category</option>
                {categories.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className={labelClass}>Product Name</label>
              <input type="text" placeholder="e.g. Galaxy S24 Ultra" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Brand</label>
              <input type="text" placeholder="e.g. Samsung" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Model Number</label>
              <input type="text" placeholder="e.g. SM-S928B" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Serial Number</label>
              <input type="text" placeholder="e.g. SN-S24U-8847201" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Purchase Date</label>
              <input type="date" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Purchase Price</label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">$</span>
                <input type="number" placeholder="1299" className={`${inputClass} pl-7`} required />
              </div>
            </div>
            <div>
              <label className={labelClass}>Warranty Duration (months)</label>
              <select className={inputClass} required>
                <option value="">Select duration</option>
                <option value="6">6 months</option>
                <option value="12">12 months</option>
                <option value="24">24 months</option>
                <option value="36">36 months</option>
              </select>
            </div>
          </div>
        </div>

        {/* Claim Information */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-teal-50 flex items-center justify-center">
                <FileText className="w-4.5 h-4.5 text-teal-600" />
              </div>
              <div>
                <h2 className="font-semibold text-slate-800 text-sm">Claim Information</h2>
                <p className="text-xs text-slate-400">Details about the fault and claim</p>
              </div>
            </div>
          </div>
          <div className="p-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>Fault Occurrence Date</label>
              <input type="date" className={inputClass} required />
            </div>
            <div>
              <label className={labelClass}>Damage Type</label>
              <select className={inputClass} required>
                <option value="">Select damage type</option>
                {damageTypes.map((d) => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
            <div className="sm:col-span-2">
              <label className={labelClass}>Fault Description</label>
              <textarea
                rows={3}
                placeholder="Describe the fault in detail..."
                className={`${inputClass} resize-none`}
                required
              />
            </div>
            <div>
              <label className={labelClass}>Previous Repairs</label>
              <input type="text" placeholder="e.g. None" className={inputClass} />
            </div>
            <div>
              <label className={labelClass}>Service Center</label>
              <input type="text" placeholder="e.g. Authorized Service Center" className={inputClass} />
            </div>
            <div>
              <label className={labelClass}>Claim Submission Date</label>
              <input type="date" className={inputClass} required />
            </div>
          </div>
        </div>

        {/* Supporting Documents */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-card overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-violet-50 flex items-center justify-center">
                <Upload className="w-4.5 h-4.5 text-violet-600" />
              </div>
              <div>
                <h2 className="font-semibold text-slate-800 text-sm">Supporting Documents</h2>
                <p className="text-xs text-slate-400">Upload relevant documents for claim validation</p>
              </div>
            </div>
          </div>
          <div className="p-5 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <DocumentUpload label="Purchase Receipt" type="Purchase Receipt" />
            <DocumentUpload label="Warranty Card" type="Warranty Card" />
            <DocumentUpload label="Product Image" type="Product Image" />
            <DocumentUpload label="Serial Number Evidence" type="Serial Number Evidence" />
            <DocumentUpload label="Fault Evidence" type="Fault Evidence" />
            <DocumentUpload label="Repair Report" type="Repair Report" />
          </div>
        </div>

        {/* Submit */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => navigate('/claims')}
            className="px-5 py-2.5 text-sm font-medium text-slate-600 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="inline-flex items-center gap-2 px-5 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors disabled:opacity-60"
          >
            {submitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                Submit Claim
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
