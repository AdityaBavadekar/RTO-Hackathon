import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Shield, MapPin, FileText, LogOut, Truck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Sidebar: React.FC = () => {
  const { signOut } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await signOut();
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <div className="flex items-center gap-3">
          <Shield className="h-8 w-8 text-red-600" />
          <h1 className="text-xl font-bold">RTO Dashboard</h1>
        </div>
      </div>
      <nav className="mt-6">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center gap-3 px-6 py-3 hover:bg-gray-100 ${
              isActive ? 'bg-gray-100 text-red-600' : ''
            }`
          }
        >
          <FileText className="h-5 w-5" />
          <span>Challans</span>
        </NavLink>
        <NavLink
          to="/map"
          className={({ isActive }) =>
            `flex items-center gap-3 px-6 py-3 hover:bg-gray-100 ${
              isActive ? 'bg-gray-100 text-red-600' : ''
            }`
          }
        >
          <MapPin className="h-5 w-5" />
          <span>Map View</span>
        </NavLink>
        <NavLink
          to="/vehicles"
          className={({ isActive }) =>
            `flex items-center gap-3 px-6 py-3 hover:bg-gray-100 ${
              isActive ? 'bg-gray-100 text-red-600' : ''
            }`
          }
        >
          <Truck className="h-5 w-5" />
          <span>Vehicles</span>
        </NavLink>
      </nav>
      <div className="absolute bottom-0 w-64 p-6">
        <button 
          onClick={handleLogout}
          className="flex w-full items-center gap-3 text-gray-600 hover:text-red-600"
        >
          <LogOut className="h-5 w-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;