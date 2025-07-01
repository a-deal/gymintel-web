/**
 * Metro Page - Metropolitan area exploration and analysis
 * Uses Tailwind UI list and detail patterns
 */

import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@apollo/client';
import { LIST_METROPOLITAN_AREAS, GET_METROPOLITAN_AREA, GET_GYMS_BY_METRO } from '../graphql/queries';
import {
  BuildingOfficeIcon,
  MapPinIcon,
  UsersIcon,
  ChartBarIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import { GymCard } from '../components/GymCard';
import clsx from 'clsx';

export const MetroPage: React.FC = () => {
  const { code } = useParams<{ code: string }>();
  const [selectedMetro, setSelectedMetro] = useState<string>(code || '');
  const [showGyms, setShowGyms] = useState(false);

  const { data: metroListData, loading: metroListLoading } = useQuery(LIST_METROPOLITAN_AREAS);

  const { data: metroData, loading: metroLoading } = useQuery(
    GET_METROPOLITAN_AREA,
    {
      variables: { code: selectedMetro },
      skip: !selectedMetro,
    }
  );

  const { data: gymsData, loading: gymsLoading } = useQuery(
    GET_GYMS_BY_METRO,
    {
      variables: { metroCode: selectedMetro, limit: 50 },
      skip: !selectedMetro || !showGyms,
    }
  );

  const metroAreas = metroListData?.listMetropolitanAreas || [];
  const currentMetro = metroData?.metropolitanArea;
  const gyms = gymsData?.gymsByMetro || [];

  const getDensityColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'very_high': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatPopulation = (population: number) => {
    if (population >= 1000000) {
      return `${(population / 1000000).toFixed(1)}M`;
    }
    if (population >= 1000) {
      return `${(population / 1000).toFixed(0)}K`;
    }
    return population.toString();
  };

  return (
    <div className="h-full flex">
      {/* Sidebar - Metro List */}
      <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 flex items-center">
            <BuildingOfficeIcon className="h-5 w-5 mr-2 text-gym-blue-600" />
            Metropolitan Areas
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Explore gym markets across major cities
          </p>
        </div>

        {metroListLoading ? (
          <div className="p-6">
            <div className="animate-pulse space-y-4">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        ) : (
          <div className="p-4 space-y-2">
            {metroAreas.map((metro) => (
              <button
                key={metro.id}
                onClick={() => {
                  setSelectedMetro(metro.code);
                  setShowGyms(false);
                }}
                className={clsx(
                  'w-full text-left p-3 rounded-lg transition-colors duration-200',
                  selectedMetro === metro.code
                    ? 'bg-gym-blue-50 border border-gym-blue-200'
                    : 'hover:bg-gray-50 border border-transparent'
                )}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate">
                      {metro.name}
                    </h3>
                    <p className="text-sm text-gray-600 truncate">
                      {metro.state} • {metro.zipCodes.length} ZIP codes
                    </p>
                    {metro.population && (
                      <p className="text-xs text-gray-500">
                        Population: {formatPopulation(metro.population)}
                      </p>
                    )}
                  </div>
                  <div className="ml-2">
                    <span className={clsx(
                      'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                      getDensityColor(metro.densityCategory)
                    )}>
                      {metro.densityCategory.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {!selectedMetro ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Select a metropolitan area
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Choose from the list to explore gym market data and statistics
              </p>
            </div>
          </div>
        ) : currentMetro ? (
          <div className="p-8">
            {/* Header */}
            <div className="mb-8">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">
                    {currentMetro.name}
                  </h1>
                  <p className="text-lg text-gray-600 mt-1">
                    {currentMetro.description}
                  </p>
                </div>
                <span className={clsx(
                  'inline-flex items-center px-3 py-2 rounded-full text-sm font-medium',
                  getDensityColor(currentMetro.densityCategory)
                )}>
                  {currentMetro.densityCategory.replace('_', ' ')} density
                </span>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <MapPinIcon className="h-8 w-8 text-gym-blue-600" />
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">
                      {currentMetro.zipCodes.length}
                    </p>
                    <p className="text-sm text-gray-600">ZIP Codes</p>
                  </div>
                </div>
              </div>

              {currentMetro.population && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <div className="flex items-center">
                    <UsersIcon className="h-8 w-8 text-green-600" />
                    <div className="ml-4">
                      <p className="text-2xl font-bold text-gray-900">
                        {formatPopulation(currentMetro.population)}
                      </p>
                      <p className="text-sm text-gray-600">Population</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <ChartBarIcon className="h-8 w-8 text-purple-600" />
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">
                      {currentMetro.statistics.totalGyms}
                    </p>
                    <p className="text-sm text-gray-600">Total Gyms</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center">
                  <BuildingOfficeIcon className="h-8 w-8 text-orange-600" />
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">
                      {Math.round(currentMetro.statistics.averageConfidence * 100)}%
                    </p>
                    <p className="text-sm text-gray-600">Avg Confidence</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Market Characteristics */}
            {currentMetro.marketCharacteristics.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Market Characteristics
                </h3>
                <div className="flex flex-wrap gap-2">
                  {currentMetro.marketCharacteristics.map((characteristic, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700"
                    >
                      {characteristic}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* ZIP Codes */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                ZIP Codes ({currentMetro.zipCodes.length})
              </h3>
              <div className="grid grid-cols-6 md:grid-cols-10 gap-2">
                {currentMetro.zipCodes.map((zip, index) => (
                  <span
                    key={index}
                    className="text-center py-2 px-3 text-sm font-mono bg-gray-50 rounded border border-gray-200"
                  >
                    {zip}
                  </span>
                ))}
              </div>
            </div>

            {/* Statistics Detail */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Detailed Statistics
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm font-medium text-gray-700">Merge Rate</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Math.round(currentMetro.statistics.mergeRate * 100)}%
                  </p>
                  <p className="text-sm text-gray-500">
                    {currentMetro.statistics.mergedGyms} of {currentMetro.statistics.totalGyms} gyms
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Deduplication Rate</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {Math.round(currentMetro.statistics.deduplicationRate * 100)}%
                  </p>
                  <p className="text-sm text-gray-500">Cross-source matching</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Data Quality</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {currentMetro.statistics.averageConfidence >= 0.8 ? 'Excellent' :
                     currentMetro.statistics.averageConfidence >= 0.6 ? 'Good' :
                     currentMetro.statistics.averageConfidence >= 0.4 ? 'Fair' : 'Poor'}
                  </p>
                  <p className="text-sm text-gray-500">
                    {Math.round(currentMetro.statistics.averageConfidence * 100)}% average confidence
                  </p>
                </div>
              </div>
            </div>

            {/* Explore Gyms Button */}
            <div className="flex justify-center">
              <button
                onClick={() => setShowGyms(!showGyms)}
                disabled={gymsLoading}
                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-gym-blue-600 hover:bg-gym-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gym-blue-500 disabled:opacity-50"
              >
                {gymsLoading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                ) : (
                  <MapPinIcon className="w-5 h-5 mr-2" />
                )}
                {showGyms ? 'Hide Gyms' : 'Explore Gyms in this Area'}
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </button>
            </div>

            {/* Gyms List */}
            {showGyms && (
              <div className="mt-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Gyms in {currentMetro.name} ({gyms.length})
                </h3>
                {gyms.length > 0 ? (
                  <div className="space-y-4">
                    {gyms.map((gym) => (
                      <GymCard key={gym.id} gym={gym} />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <MapPinIcon className="mx-auto h-12 w-12 text-gray-400" />
                    <h3 className="mt-2 text-sm font-medium text-gray-900">
                      No gyms found
                    </h3>
                    <p className="mt-1 text-sm text-gray-500">
                      This metropolitan area doesn't have gym data yet.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : metroLoading ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-gym-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Loading metropolitan area data...</p>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};
