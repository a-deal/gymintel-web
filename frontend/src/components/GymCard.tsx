/**
 * GymCard Component - Displays gym information in a card format
 * Uses Tailwind UI card patterns with confidence scoring
 */

import { Gym } from '../types/gym';
import {
  MapPinIcon,
  PhoneIcon,
  GlobeAltIcon,
  StarIcon,
  ShieldCheckIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';
import clsx from 'clsx';

interface GymCardProps {
  gym: Gym;
  onClick?: () => void;
}

export const GymCard = ({ gym, onClick }: GymCardProps) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-confidence-excellent bg-green-50 border-green-200';
    if (confidence >= 0.6) return 'text-confidence-high bg-green-50 border-green-200';
    if (confidence >= 0.4) return 'text-confidence-medium bg-yellow-50 border-yellow-200';
    return 'text-confidence-low bg-red-50 border-red-200';
  };

  const getConfidenceLabel = (confidence: number) => {
    if (confidence >= 0.8) return 'Excellent';
    if (confidence >= 0.6) return 'High';
    if (confidence >= 0.4) return 'Medium';
    return 'Low';
  };

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;

    for (let i = 0; i < 5; i++) {
      if (i < fullStars) {
        stars.push(
          <StarIconSolid key={i} className="h-4 w-4 text-yellow-400" />
        );
      } else if (i === fullStars && hasHalfStar) {
        stars.push(
          <div key={i} className="relative">
            <StarIcon className="h-4 w-4 text-gray-300" />
            <div className="absolute inset-0 overflow-hidden w-1/2">
              <StarIconSolid className="h-4 w-4 text-yellow-400" />
            </div>
          </div>
        );
      } else {
        stars.push(
          <StarIcon key={i} className="h-4 w-4 text-gray-300" />
        );
      }
    }
    return stars;
  };

  return (
    <div
      className={clsx(
        'bg-white rounded-lg shadow-gym border border-gray-200 p-6 hover:shadow-gym-lg transition-all duration-200',
        onClick && 'cursor-pointer hover:border-gym-blue-300'
      )}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {gym.name}
          </h3>
          <div className="flex items-center mt-1 text-sm text-gray-500">
            <MapPinIcon className="h-4 w-4 mr-1 flex-shrink-0" />
            <span className="truncate">{gym.address}</span>
          </div>
        </div>

        {/* Confidence Badge */}
        <div className={clsx(
          'ml-4 px-2 py-1 rounded-full text-xs font-medium border',
          getConfidenceColor(gym.confidence)
        )}>
          <div className="flex items-center">
            <ShieldCheckIcon className="h-3 w-3 mr-1" />
            {getConfidenceLabel(gym.confidence)} ({Math.round(gym.confidence * 100)}%)
          </div>
        </div>
      </div>

      {/* Rating */}
      {gym.rating && (
        <div className="flex items-center mb-4">
          <div className="flex items-center">
            {renderStars(gym.rating)}
          </div>
          <span className="ml-2 text-sm font-medium text-gray-900">
            {gym.rating.toFixed(1)}
          </span>
          {gym.reviewCount && (
            <span className="ml-1 text-sm text-gray-500">
              ({gym.reviewCount} reviews)
            </span>
          )}
        </div>
      )}

      {/* Contact Info */}
      <div className="space-y-2 mb-4">
        {gym.phone && (
          <div className="flex items-center text-sm text-gray-600">
            <PhoneIcon className="h-4 w-4 mr-2 text-gray-400" />
            <a
              href={`tel:${gym.phone}`}
              className="hover:text-gym-blue-600 transition-colors"
              onClick={(e) => e.stopPropagation()}
            >
              {gym.phone}
            </a>
          </div>
        )}

        {gym.website && (
          <div className="flex items-center text-sm text-gray-600">
            <GlobeAltIcon className="h-4 w-4 mr-2 text-gray-400" />
            <a
              href={gym.website}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-gym-blue-600 transition-colors truncate"
              onClick={(e) => e.stopPropagation()}
            >
              Visit Website
            </a>
          </div>
        )}
      </div>

      {/* Data Sources */}
      {gym.sources.length > 0 && (
        <div className="mb-4">
          <div className="text-xs font-medium text-gray-700 mb-2">Data Sources:</div>
          <div className="flex flex-wrap gap-1">
            {gym.sources.map((source, index) => (
              <span
                key={index}
                className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700"
              >
                {source.name}
                {source.confidence > 0 && (
                  <span className="ml-1 text-gray-500">
                    ({Math.round(source.confidence * 100)}%)
                  </span>
                )}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
        <div className="flex items-center text-xs text-gray-500">
          <CalendarIcon className="h-3 w-3 mr-1" />
          Updated {new Date(gym.updatedAt).toLocaleDateString()}
        </div>

        {gym.sourceZipcode && (
          <span className="text-xs text-gray-500">
            Source: {gym.sourceZipcode}
          </span>
        )}
      </div>
    </div>
  );
};
