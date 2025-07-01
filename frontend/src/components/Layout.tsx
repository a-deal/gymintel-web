/**
 * Layout Component - Main application layout with navigation
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  MapIcon, 
  ChartBarIcon, 
  MagnifyingGlassIcon,
  BuildingOfficeIcon
} from '@heroicons/react/24/outline';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navigation = [
    { name: 'Home', href: '/', icon: MapIcon },
    { name: 'Search', href: '/search', icon: MagnifyingGlassIcon },
    { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
    { name: 'Metro Areas', href: '/metro', icon: BuildingOfficeIcon },
  ];

  const isActive = (href: string) => {
    if (href === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="flex items-center px-6 py-4 border-b border-gray-200">
          <MapIcon className="h-8 w-8 text-blue-600" />
          <h1 className="ml-3 text-xl font-bold text-gray-900 font-heading">GymIntel</h1>
        </div>
        
        <nav className="mt-6">
          <div className="px-3">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                    isActive(item.href)
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon
                    className={`mr-3 h-5 w-5 flex-shrink-0 ${
                      isActive(item.href) ? 'text-blue-700' : 'text-gray-400 group-hover:text-gray-600'
                    }`}
                  />
                  {item.name}
                </Link>
              );
            })}
          </div>
        </nav>

        {/* Footer */}
        <div className="absolute bottom-0 w-64 p-4 border-t border-gray-200 bg-white">
          <div className="text-xs text-gray-500">
            <p>Version 1.0.0</p>
            <p>Phase 3B: Core Features</p>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};