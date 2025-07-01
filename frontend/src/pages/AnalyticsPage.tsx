/**
 * Analytics Page - Gym market analytics and insights
 * Uses Tailwind UI dashboard patterns with Recharts
 */

import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import { GET_GYM_ANALYTICS, MARKET_GAP_ANALYSIS } from '../graphql/queries';
import {
  ChartBarIcon,
  MapPinIcon,
  TrendingUpIcon,
  ExclamationTriangleIcon,
  MagnifyingGlassIcon
} from '@heroicons/react/24/outline';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';

export const AnalyticsPage: React.FC = () => {
  const [zipcode, setZipcode] = useState('');
  const [activeZipcode, setActiveZipcode] = useState('');

  const { data: analyticsData, loading: analyticsLoading, error: analyticsError } = useQuery(
    GET_GYM_ANALYTICS,
    {
      variables: { zipcode: activeZipcode },
      skip: !activeZipcode,
    }
  );

  const { data: gapData, loading: gapLoading } = useQuery(
    MARKET_GAP_ANALYSIS,
    {
      variables: { zipcode: activeZipcode, radius: 10 },
      skip: !activeZipcode,
    }
  );

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (zipcode.trim()) {
      setActiveZipcode(zipcode.trim());
    }
  };

  const analytics = analyticsData?.gymAnalytics;
  const marketGaps = gapData?.marketGapAnalysis || [];

  // Parse JSON data for charts
  const confidenceData = analytics?.confidenceDistribution
    ? Object.entries(JSON.parse(analytics.confidenceDistribution)).map(([range, count]) => ({
        range,
        count: count as number,
      }))
    : [];

  const sourceData = analytics?.sourceBreakdown
    ? Object.entries(JSON.parse(analytics.sourceBreakdown)).map(([source, count]) => ({
        source,
        count: count as number,
      }))
    : [];

  const ratingAnalysis = analytics?.ratingAnalysis
    ? JSON.parse(analytics.ratingAnalysis)
    : null;

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  return (
    <div className="h-full overflow-y-auto">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-6">
        <div className="max-w-7xl mx-auto">
          <div className="md:flex md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <h1 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">
                <ChartBarIcon className="h-8 w-8 inline mr-2 text-gym-blue-600" />
                Gym Market Analytics
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Comprehensive analysis of gym markets with intelligence insights
              </p>
            </div>
          </div>

          {/* Search Form */}
          <form onSubmit={handleSearch} className="mt-6 flex gap-4">
            <div className="flex-1 max-w-lg">
              <input
                type="text"
                placeholder="Enter ZIP code for analytics"
                value={zipcode}
                onChange={(e) => setZipcode(e.target.value)}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-gym-blue-500 focus:ring-gym-blue-500 sm:text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={analyticsLoading || !zipcode.trim()}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-gym-blue-600 hover:bg-gym-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gym-blue-500 disabled:opacity-50"
            >
              {analyticsLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
              ) : (
                <MagnifyingGlassIcon className="w-4 h-4 mr-2" />
              )}
              Analyze
            </button>
          </form>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Empty State */}
        {!activeZipcode && (
          <div className="text-center py-12">
            <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No analytics yet</h3>
            <p className="mt-1 text-sm text-gray-500">
              Enter a ZIP code to get detailed gym market analytics
            </p>
          </div>
        )}

        {/* Error State */}
        {analyticsError && (
          <div className="rounded-md bg-red-50 p-4 mb-6">
            <div className="flex">
              <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Error loading analytics
                </h3>
                <p className="mt-2 text-sm text-red-700">
                  {analyticsError.message}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Analytics Dashboard */}
        {analytics && (
          <div className="space-y-8">
            {/* Overview Cards */}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <MapPinIcon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Total Gyms
                        </dt>
                        <dd className="text-lg font-medium text-gray-900">
                          {analytics.totalGyms}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <TrendingUpIcon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Density Score
                        </dt>
                        <dd className="text-lg font-medium text-gray-900">
                          {analytics.densityScore.toFixed(1)}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <ChartBarIcon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          Market Saturation
                        </dt>
                        <dd className="text-lg font-medium text-gray-900 capitalize">
                          {analytics.marketSaturation}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <MapPinIcon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          ZIP Code
                        </dt>
                        <dd className="text-lg font-medium text-gray-900">
                          {analytics.zipcode}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Confidence Distribution */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Confidence Distribution
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={confidenceData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="range" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="count" fill="#3b82f6" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Source Breakdown */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Data Source Breakdown
                </h3>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={sourceData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ source, percent }) => `${source} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="count"
                      >
                        {sourceData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Rating Analysis */}
            {ratingAnalysis && (
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Rating Analysis
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {ratingAnalysis.count}
                    </div>
                    <div className="text-sm text-gray-500">Rated Gyms</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {ratingAnalysis.average.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">Average Rating</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {ratingAnalysis.min.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">Lowest Rating</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {ratingAnalysis.max.toFixed(1)}
                    </div>
                    <div className="text-sm text-gray-500">Highest Rating</div>
                  </div>
                </div>
              </div>
            )}

            {/* Market Gaps */}
            {marketGaps.length > 0 && (
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Market Opportunity Analysis
                </h3>
                <div className="space-y-4">
                  {marketGaps.map((gap, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="text-sm font-medium text-gray-900">
                            {gap.areaDescription}
                          </h4>
                          <p className="text-sm text-gray-600 mt-1">
                            {gap.reasoning}
                          </p>
                          <div className="flex items-center mt-2 space-x-4 text-xs text-gray-500">
                            <span>Gap Score: {Math.round(gap.gapScore * 100)}%</span>
                            <span>Population Density: {gap.populationDensity}/sq mi</span>
                            <span>Nearest Gym: {gap.nearestGymDistance} miles</span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className={`text-right text-sm font-medium ${
                            gap.gapScore >= 0.7 ? 'text-green-600' :
                            gap.gapScore >= 0.5 ? 'text-yellow-600' : 'text-red-600'
                          }`}>
                            {gap.gapScore >= 0.7 ? 'High Opportunity' :
                             gap.gapScore >= 0.5 ? 'Medium Opportunity' : 'Low Opportunity'}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
