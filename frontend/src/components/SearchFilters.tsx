/**
 * SearchFilters Component - Advanced filtering interface
 * Uses Tailwind UI form patterns with Headless UI components
 */

import React from 'react';
import { Switch } from '@headlessui/react';
import { SearchFilters as SearchFiltersType } from '../types/gym';
import { 
  AdjustmentsHorizontalIcon,
  StarIcon,
  ShieldCheckIcon,
  MapPinIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

interface SearchFiltersProps {
  filters: SearchFiltersType;
  onFiltersChange: (filters: SearchFiltersType) => void;
}

export const SearchFilters: React.FC<SearchFiltersProps> = ({ 
  filters, 
  onFiltersChange 
}) => {
  const updateFilter = (key: keyof SearchFiltersType, value: any) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    onFiltersChange({});
  };

  const activeFiltersCount = Object.values(filters).filter(
    value => value !== undefined && value !== null && value !== ''
  ).length;

  return (
    <div className="p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center">
          <AdjustmentsHorizontalIcon className="h-5 w-5 text-gray-400 mr-2" />
          <h3 className="text-lg font-medium text-gray-900">Filters</h3>
          {activeFiltersCount > 0 && (
            <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-gym-blue-100 text-gym-blue-800">
              {activeFiltersCount}
            </span>
          )}
        </div>
        
        {activeFiltersCount > 0 && (
          <button
            onClick={clearFilters}
            className="text-sm font-medium text-gym-blue-600 hover:text-gym-blue-500"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="space-y-6">
        {/* Rating Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <StarIcon className="h-4 w-4 inline mr-1" />
            Minimum Rating
          </label>
          <div className="space-y-2">
            {[4.5, 4.0, 3.5, 3.0, 2.5].map((rating) => (
              <label key={rating} className="flex items-center">
                <input
                  type="radio"
                  name="minRating"
                  value={rating}
                  checked={filters.minRating === rating}
                  onChange={(e) => updateFilter('minRating', parseFloat(e.target.value))}
                  className="h-4 w-4 text-gym-blue-600 border-gray-300 focus:ring-gym-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">
                  {rating}+ stars
                </span>
              </label>
            ))}
            <label className="flex items-center">
              <input
                type="radio"
                name="minRating"
                checked={!filters.minRating}
                onChange={() => updateFilter('minRating', undefined)}
                className="h-4 w-4 text-gym-blue-600 border-gray-300 focus:ring-gym-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Any rating</span>
            </label>
          </div>
        </div>

        {/* Confidence Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <ShieldCheckIcon className="h-4 w-4 inline mr-1" />
            Minimum Confidence
          </label>
          <div className="space-y-2">
            {[
              { value: 0.8, label: 'Excellent (80%+)', color: 'text-confidence-excellent' },
              { value: 0.6, label: 'High (60%+)', color: 'text-confidence-high' },
              { value: 0.4, label: 'Medium (40%+)', color: 'text-confidence-medium' },
              { value: 0.2, label: 'Low (20%+)', color: 'text-confidence-low' },
            ].map((conf) => (
              <label key={conf.value} className="flex items-center">
                <input
                  type="radio"
                  name="minConfidence"
                  value={conf.value}
                  checked={filters.minConfidence === conf.value}
                  onChange={(e) => updateFilter('minConfidence', parseFloat(e.target.value))}
                  className="h-4 w-4 text-gym-blue-600 border-gray-300 focus:ring-gym-blue-500"
                />
                <span className={clsx('ml-2 text-sm', conf.color)}>
                  {conf.label}
                </span>
              </label>
            ))}
            <label className="flex items-center">
              <input
                type="radio"
                name="minConfidence"
                checked={!filters.minConfidence}
                onChange={() => updateFilter('minConfidence', undefined)}
                className="h-4 w-4 text-gym-blue-600 border-gray-300 focus:ring-gym-blue-500"
              />
              <span className="ml-2 text-sm text-gray-700">Any confidence</span>
            </label>
          </div>
        </div>

        {/* Distance Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <MapPinIcon className="h-4 w-4 inline mr-1" />
            Maximum Distance
          </label>
          <div className="space-y-2">
            <input
              type="range"
              min="1"
              max="50"
              step="1"
              value={filters.maxDistance || 50}
              onChange={(e) => updateFilter('maxDistance', parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>1 mile</span>
              <span className="font-medium text-gym-blue-600">
                {filters.maxDistance || 50} miles
              </span>
              <span>50 miles</span>
            </div>
          </div>
        </div>

        {/* Data Sources */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Data Sources
          </label>
          <div className="space-y-2">
            {['Yelp', 'Google Places', 'Merged'].map((source) => (
              <label key={source} className="flex items-center">
                <input
                  type="checkbox"
                  checked={filters.sources?.includes(source) || false}
                  onChange={(e) => {
                    const currentSources = filters.sources || [];
                    if (e.target.checked) {
                      updateFilter('sources', [...currentSources, source]);
                    } else {
                      updateFilter('sources', currentSources.filter(s => s !== source));
                    }
                  }}
                  className="h-4 w-4 text-gym-blue-600 border-gray-300 rounded focus:ring-gym-blue-500"
                />
                <span className="ml-2 text-sm text-gray-700">{source}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Contact Info Toggles */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Has Website</span>
            <Switch
              checked={filters.hasWebsite || false}
              onChange={(checked) => updateFilter('hasWebsite', checked || undefined)}
              className={clsx(
                filters.hasWebsite ? 'bg-gym-blue-600' : 'bg-gray-200',
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-gym-blue-500 focus:ring-offset-2'
              )}
            >
              <span
                className={clsx(
                  filters.hasWebsite ? 'translate-x-6' : 'translate-x-1',
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform'
                )}
              />
            </Switch>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Has Instagram</span>
            <Switch
              checked={filters.hasInstagram || false}
              onChange={(checked) => updateFilter('hasInstagram', checked || undefined)}
              className={clsx(
                filters.hasInstagram ? 'bg-gym-blue-600' : 'bg-gray-200',
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-gym-blue-500 focus:ring-offset-2'
              )}
            >
              <span
                className={clsx(
                  filters.hasInstagram ? 'translate-x-6' : 'translate-x-1',
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform'
                )}
              />
            </Switch>
          </div>
        </div>
      </div>
    </div>
  );
};