import React from 'react';
import { Outlet } from 'react-router-dom';
import { Shield, MapPin, FileText, LogOut } from 'lucide-react';
import Sidebar from './Sidebar';

const Layout: React.FC = () => {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;