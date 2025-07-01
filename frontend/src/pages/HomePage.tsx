/**
 * Home Page - Landing page with quick search and overview
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLazyQuery } from '@apollo/client';
import { SEARCH_GYMS } from '../graphql/queries';
import { MagnifyingGlassIcon, MapPinIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export const HomePage: React.FC = () => {
  const [zipcode, setZipcode] = useState('');
  const navigate = useNavigate();
  const [searchGyms, { loading }] = useLazyQuery(SEARCH_GYMS);

  const handleQuickSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!zipcode.trim()) return;

    // Navigate to search page with zipcode
    navigate(`/search?zipcode=${zipcode}`);
  };

  const features = [
    {
      title: 'Smart Gym Discovery',
      description: 'AI-powered gym search with confidence scoring and multi-source data aggregation',
      icon: MagnifyingGlassIcon,
      color: 'blue',
    },
    {
      title: 'Interactive Maps',
      description: 'Visualize gym locations with clustering, density overlays, and confidence indicators',
      icon: MapPinIcon,
      color: 'green',
    },
    {
      title: 'Business Intelligence',
      description: 'Market gap analysis, competitor mapping, and demographic insights for strategic planning',
      icon: ChartBarIcon,
      color: 'purple',
    },
  ];

  const stats = [
    { label: 'Metropolitan Areas', value: '15+' },
    { label: 'Data Sources', value: '2' },
    { label: 'Confidence Algorithms', value: '5' },
    { label: 'Real-time Updates', value: 'Yes' },
  ];

  return (
    <div className="min-h-full">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 font-heading">
              Intelligent Gym Discovery
            </h1>
            <p className="text-xl md:text-2xl mb-12 text-blue-100 max-w-3xl mx-auto">
              Advanced gym intelligence platform with AI-powered confidence scoring,
              multi-source data aggregation, and real-time business analytics.
            </p>

            {/* Quick Search */}
            <div className="max-w-md mx-auto">
              <form onSubmit={handleQuickSearch} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Enter ZIP code to start..."
                  value={zipcode}
                  onChange={(e) => setZipcode(e.target.value)}
                  className="flex-1 px-4 py-3 rounded-lg text-gray-900 placeholder-gray-500 border-0 focus:ring-2 focus:ring-blue-300 focus:outline-none"
                />
                <button
                  type="submit"
                  disabled={loading || !zipcode.trim()}
                  className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-blue-300 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  {loading ? (
                    <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <MagnifyingGlassIcon className="w-5 h-5" />
                  )}
                </button>
              </form>
              <p className="text-blue-200 text-sm mt-2">
                Search gyms with intelligent confidence scoring
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4 font-heading">
              Phase 3B: Core Features
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Transform from CLI tool to comprehensive web platform with advanced visualization and business intelligence.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              const colorClasses = {
                blue: 'bg-blue-100 text-blue-600',
                green: 'bg-green-100 text-green-600',
                purple: 'bg-purple-100 text-purple-600',
              };

              return (
                <div key={index} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
                  <div className={`w-12 h-12 rounded-lg ${colorClasses[feature.color as keyof typeof colorClasses]} flex items-center justify-center mb-4`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2 font-heading">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white py-16">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-4 font-heading">
            Ready to Explore Gym Intelligence?
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Start with a search, explore metropolitan areas, or dive into detailed analytics.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/search')}
              className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors duration-200"
            >
              Start Searching
            </button>
            <button
              onClick={() => navigate('/metro')}
              className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              Explore Metro Areas
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
