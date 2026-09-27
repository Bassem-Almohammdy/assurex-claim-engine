import { User, Bell, Shield, Globe, Palette } from 'lucide-react';
import PageHeader from '@/components/ui/PageHeader';

export default function SettingsPage() {
  const sections = [
    { icon: User, title: 'Profile Settings', description: 'Manage your personal information and preferences' },
    { icon: Bell, title: 'Notifications', description: 'Configure email and in-app notification preferences' },
    { icon: Shield, title: 'Security', description: 'Password, two-factor authentication, and access control' },
    { icon: Globe, title: 'API Configuration', description: 'Connect external APIs for AI models and OCR services' },
    { icon: Palette, title: 'Appearance', description: 'Customize the look and feel of the dashboard' },
  ];

  return (
    <div className="animate-fade-in">
      <PageHeader title="Settings" subtitle="Manage your account and system configuration" />

      <div className="max-w-3xl space-y-4">
        {sections.map((section, i) => {
          const Icon = section.icon;
          return (
            <div key={i} className="bg-white rounded-xl border border-slate-200 shadow-card hover:shadow-card-hover transition-all p-5 flex items-center gap-4 cursor-pointer group">
              <div className="flex-shrink-0 w-11 h-11 rounded-lg bg-slate-50 group-hover:bg-brand-50 flex items-center justify-center transition-colors">
                <Icon className="w-5 h-5 text-slate-500 group-hover:text-brand-600 transition-colors" />
              </div>
              <div className="flex-1">
                <h3 className="font-medium text-slate-800 text-sm">{section.title}</h3>
                <p className="text-xs text-slate-400 mt-0.5">{section.description}</p>
              </div>
              <button className="px-3 py-1.5 text-xs font-medium text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-lg transition-colors">
                Configure
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
