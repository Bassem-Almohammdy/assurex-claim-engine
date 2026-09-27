import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from '@/components/layout/Layout';
import DashboardPage from '@/pages/DashboardPage';
import NewClaimPage from '@/pages/NewClaimPage';
import ClaimsPage from '@/pages/ClaimsPage';
import ClaimDetailsPage from '@/pages/ClaimDetailsPage';
import ProductsPage from '@/pages/ProductsPage';
import WarrantiesPage from '@/pages/WarrantiesPage';
import DocumentsPage from '@/pages/DocumentsPage';
import AnalyticsPage from '@/pages/AnalyticsPage';
import SettingsPage from '@/pages/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/claims" element={<ClaimsPage />} />
          <Route path="/claims/new" element={<NewClaimPage />} />
          <Route path="/claims/:id" element={<ClaimDetailsPage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/warranties" element={<WarrantiesPage />} />
          <Route path="/documents" element={<DocumentsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="/" element={<DashboardPage />} />
          <Route path="*" element={<DashboardPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
