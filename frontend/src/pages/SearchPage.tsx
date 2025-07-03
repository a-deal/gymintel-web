/**
 * Search Page - Main gym search interface with filters and results
 */

import { useState, useEffect } from 'react';
import { Gym } from '../types/gym';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@apollo/client';
import { SEARCH_GYMS } from '../graphql/queries';
import { GymCard } from '../components/GymCard';
import { SearchFilters } from '../components/SearchFilters';
import { MapView } from '../components/MapView';
import { SearchInputMUISimple } from '../components/SearchInputMUISimple';
import { SearchFilters as SearchFiltersType } from '../types/gym';
import {
  MagnifyingGlassIcon,
  MapIcon,
  ListBulletIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';

export const SearchPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [location, setLocation] = useState(searchParams.get('location') || '');
  const [radius, setRadius] = useState(Number(searchParams.get('radius')) || 10);
  const [filters, setFilters] = useState<SearchFiltersType>({});
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list');
  const [showFilters, setShowFilters] = useState(false);

  const { data, loading, error, refetch } = useQuery(SEARCH_GYMS, {
    variables: {
      location,
      radius,
      limit: 50,
      filters: Object.keys(filters).length > 0 ? filters : null,
    },
    skip: !location,
  });

  useEffect(() => {
    if (location) {
      setSearchParams({ location, radius: radius.toString() });
    }
  }, [location, radius, setSearchParams]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (location.trim()) {
      refetch();
    }
  };

  const searchResult = data?.searchGyms;
  const gyms = searchResult?.gyms || [];

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Gym Search</h1>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setViewMode('list')}
              className={`p-2 rounded-md ${
                viewMode === 'list'
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <ListBulletIcon className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('map')}
              className={`p-2 rounded-md ${
                viewMode === 'map'
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <MapIcon className="w-5 h-5" />
            </button>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`p-2 rounded-md ${
                showFilters
                  ? 'bg-blue-100 text-blue-600'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <AdjustmentsHorizontalIcon className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mt-4 flex gap-4">
          <div className="flex-1">
            <SearchInputMUISimple
              value={location}
              onChange={setLocation}
              onSubmit={() => {
                if (location.trim()) {
                  refetch();
                }
              }}
              placeholder="Enter city name"
              loading={loading}
            />
          </div>
          <div className="w-32">
            <select
              value={radius}
              onChange={(e) => setRadius(Number(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value={5}>5 miles</option>
              <option value={10}>10 miles</option>
              <option value={15}>15 miles</option>
              <option value={25}>25 miles</option>
              <option value={50}>50 miles</option>
            </select>
          </div>
          <button
            type="submit"
            disabled={loading || !location.trim()}
            className="px-6 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <MagnifyingGlassIcon className="w-5 h-5" />
            )}
          </button>
        </form>

        {/* Search Stats */}
        {searchResult && (
          <div className="mt-4 text-sm text-gray-600">
            Found {searchResult.totalResults} gyms in {searchResult.location || location} ({radius} mile radius) •
            {searchResult.mergedCount} merged records •
            {Math.round(searchResult.avgConfidence * 100)}% avg confidence •
            {searchResult.executionTimeSeconds.toFixed(1)}s
          </div>
        )}
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Filters Sidebar */}
        {showFilters && (
          <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
            <SearchFilters
              filters={filters}
              onFiltersChange={setFilters}
            />
          </div>
        )}

        {/* Main Content */}
        <div className="flex-1 overflow-hidden">
          {error && (
            <div className="p-6">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800">Error loading gyms: {error.message}</p>
              </div>
            </div>
          )}

          {!location && !loading && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <MagnifyingGlassIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Enter a city or ZIP code to search for gyms
                </h3>
                <p className="text-gray-600">
                  Use intelligent filtering and confidence scoring to find the best gym matches.
                </p>
              </div>
            </div>
          )}

          {viewMode === 'list' && gyms.length > 0 && (
            <div className="p-6 space-y-4 overflow-y-auto h-full">
              {gyms.map((gym: Gym) => (
                <GymCard key={gym.id} gym={gym} />
              ))}
            </div>
          )}

          {viewMode === 'map' && gyms.length > 0 && (
            <MapView
              gyms={gyms}
              center={searchResult?.coordinates}
              radius={radius}
            />
          )}

          {loading && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-gray-600">Searching for gyms...</p>
              </div>
            </div>
          )}

          {!loading && location && gyms.length === 0 && !error && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <MagnifyingGlassIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No gyms found
                </h3>
                <p className="text-gray-600">
                  Try expanding your search radius or adjusting your filters.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
