import { Package, Plus } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';
import { mockProducts } from '@/data/mockData';

export default function ProductsPage() {
  return (
    <div className="animate-fade-in">
      <PageHeader
        title="Products"
        subtitle="Manage products in the warranty system"
        action={
          <button className="inline-flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg shadow-sm transition-colors">
            <Plus className="w-4 h-4" />
            Add Product
          </button>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockProducts.map((product) => (
          <div key={product.id} className="bg-white rounded-xl border border-slate-200 shadow-card hover:shadow-card-hover transition-all p-5">
            <div className="flex items-start justify-between mb-3">
              <div className="w-11 h-11 rounded-lg bg-brand-50 flex items-center justify-center">
                <Package className="w-5 h-5 text-brand-600" />
              </div>
              <span className="text-xs text-slate-400 font-mono">{product.id}</span>
            </div>
            <h3 className="font-semibold text-slate-800">{product.name}</h3>
            <p className="text-xs text-slate-400 mt-0.5">{product.category}</p>
            <div className="mt-4 space-y-1.5">
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Brand</span>
                <span className="font-medium text-slate-600">{product.brand}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Model</span>
                <span className="font-medium text-slate-600">{product.modelNumber}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Serial</span>
                <span className="font-medium text-slate-600 font-mono">{product.serialNumber}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Price</span>
                <span className="font-medium text-slate-600">${product.purchasePrice.toLocaleString()}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-400">Warranty</span>
                <span className="font-medium text-slate-600">{product.warrantyDurationMonths} months</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
