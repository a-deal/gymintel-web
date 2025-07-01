/**
 * MapView Component - Interactive map with gym locations
 * Uses Mapbox GL JS with Tailwind UI patterns
 */

import React, { useRef, useEffect, useState } from 'react';
import Map, { Marker, NavigationControl, ScaleControl, GeolocateControl } from 'react-map-gl';
import { Gym, Coordinates } from '../types/gym';
import {
  MapPinIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import clsx from 'clsx';

// Mapbox access token - should be in environment variables
const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_ACCESS_TOKEN || 'your-mapbox-token';

interface MapViewProps {
  gyms: Gym[];
  center?: Coordinates;
  radius?: number;
  onGymClick?: (gym: Gym) => void;
}

export const MapView: React.FC<MapViewProps> = ({
  gyms,
  center,
  radius,
  onGymClick
}) => {
  const mapRef = useRef<any>(null);
  const [selectedGym, setSelectedGym] = useState<Gym | null>(null);
  const [viewState, setViewState] = useState({
    longitude: center?.longitude || -122.4194,
    latitude: center?.latitude || 37.7749,
    zoom: 11,
  });

  // Update map center when center prop changes
  useEffect(() => {
    if (center && mapRef.current) {
      setViewState(prev => ({
        ...prev,
        longitude: center.longitude,
        latitude: center.latitude,
        zoom: radius ? Math.max(8, 14 - Math.log2(radius)) : 11,
      }));
    }
  }, [center, radius]);

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'bg-green-500 border-green-600';
    if (confidence >= 0.6) return 'bg-yellow-500 border-yellow-600';
    if (confidence >= 0.4) return 'bg-orange-500 border-orange-600';
    return 'bg-red-500 border-red-600';
  };

  const handleGymClick = (gym: Gym) => {
    setSelectedGym(gym);
    onGymClick?.(gym);
  };

  // Fallback component when no Mapbox token
  if (!MAPBOX_TOKEN || MAPBOX_TOKEN === 'your-mapbox-token') {
    return (
      <div className="h-full flex items-center justify-center bg-gray-100">
        <div className="text-center p-8">
          <MapPinIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Map View Unavailable
          </h3>
          <p className="text-gray-600 mb-4">
            Mapbox access token required for interactive maps.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
            <div className="flex">
              <InformationCircleIcon className="h-5 w-5 text-blue-400 mt-0.5 mr-3" />
              <div className="text-sm">
                <p className="text-blue-800 font-medium mb-1">To enable maps:</p>
                <p className="text-blue-700">
                  Add your Mapbox token to <code className="bg-blue-100 px-1 rounded">VITE_MAPBOX_ACCESS_TOKEN</code> in your environment variables.
                </p>
              </div>
            </div>
          </div>

          {/* Gym List Fallback */}
          <div className="mt-6 max-w-md mx-auto">
            <h4 className="text-sm font-medium text-gray-900 mb-3">
              Gyms in this area ({gyms.length}):
            </h4>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {gyms.map((gym) => (
                <div
                  key={gym.id}
                  className="text-left bg-white border border-gray-200 rounded-lg p-3 hover:bg-gray-50 cursor-pointer"
                  onClick={() => handleGymClick(gym)}
                >
                  <div className="font-medium text-gray-900 text-sm">{gym.name}</div>
                  <div className="text-xs text-gray-500 mt-1">{gym.address}</div>
                  <div className="flex items-center mt-1">
                    <span className={clsx(
                      'inline-block w-2 h-2 rounded-full mr-2',
                      getConfidenceColor(gym.confidence).split(' ')[0]
                    )} />
                    <span className="text-xs text-gray-600">
                      {Math.round(gym.confidence * 100)}% confidence
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full relative">
      <Map
        ref={mapRef}
        {...viewState}
        onMove={evt => setViewState(evt.viewState)}
        style={{ width: '100%', height: '100%' }}
        mapStyle="mapbox://styles/mapbox/light-v11"
        mapboxAccessToken={MAPBOX_TOKEN}
      >
        {/* Controls */}
        <NavigationControl position="top-right" />
        <ScaleControl position="bottom-left" />
        <GeolocateControl position="top-right" />

        {/* Gym Markers */}
        {gyms.map((gym) => (
          <Marker
            key={gym.id}
            longitude={gym.coordinates.longitude}
            latitude={gym.coordinates.latitude}
            anchor="bottom"
          >
            <button
              onClick={() => handleGymClick(gym)}
              className={clsx(
                'w-6 h-6 rounded-full border-2 shadow-lg hover:scale-110 transition-all duration-200',
                getConfidenceColor(gym.confidence),
                selectedGym?.id === gym.id && 'ring-2 ring-white ring-offset-2 ring-offset-blue-500'
              )}
              title={`${gym.name} - ${Math.round(gym.confidence * 100)}% confidence`}
            />
          </Marker>
        ))}

        {/* Search Radius Circle (if center and radius provided) */}
        {center && radius && (
          <div className="absolute inset-0 pointer-events-none">
            {/* This would require a proper circle overlay implementation */}
          </div>
        )}
      </Map>

      {/* Selected Gym Popup */}
      {selectedGym && (
        <div className="absolute top-4 left-4 right-4 md:left-4 md:right-auto md:w-80 bg-white rounded-lg shadow-lg border border-gray-200 p-4 animate-slide-up">
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-gray-900 truncate">
                {selectedGym.name}
              </h3>
              <p className="text-sm text-gray-600 mt-1">
                {selectedGym.address}
              </p>

              {selectedGym.rating && (
                <div className="flex items-center mt-2">
                  <div className="flex items-center">
                    <span className="text-yellow-400 text-sm">★</span>
                    <span className="ml-1 text-sm font-medium text-gray-900">
                      {selectedGym.rating.toFixed(1)}
                    </span>
                  </div>
                  {selectedGym.reviewCount && (
                    <span className="ml-2 text-sm text-gray-500">
                      ({selectedGym.reviewCount} reviews)
                    </span>
                  )}
                </div>
              )}

              <div className="flex items-center mt-2">
                <span className={clsx(
                  'inline-block w-2 h-2 rounded-full mr-2',
                  getConfidenceColor(selectedGym.confidence).split(' ')[0]
                )} />
                <span className="text-sm text-gray-600">
                  {Math.round(selectedGym.confidence * 100)}% confidence
                </span>
              </div>
            </div>

            <button
              onClick={() => setSelectedGym(null)}
              className="ml-2 text-gray-400 hover:text-gray-600 p-1"
            >
              <XMarkIcon className="h-5 w-5" />
            </button>
          </div>

          {(selectedGym.phone || selectedGym.website) && (
            <div className="mt-4 pt-3 border-t border-gray-200 space-y-2">
              {selectedGym.phone && (
                <a
                  href={`tel:${selectedGym.phone}`}
                  className="block text-sm text-gym-blue-600 hover:text-gym-blue-500"
                >
                  📞 {selectedGym.phone}
                </a>
              )}
              {selectedGym.website && (
                <a
                  href={selectedGym.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block text-sm text-gym-blue-600 hover:text-gym-blue-500"
                >
                  🌐 Visit Website
                </a>
              )}
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      <div className="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg border border-gray-200 p-3">
        <h4 className="text-xs font-medium text-gray-900 mb-2">Confidence Level</h4>
        <div className="space-y-1">
          {[
            { color: 'bg-green-500', label: 'Excellent (80%+)' },
            { color: 'bg-yellow-500', label: 'Good (60-79%)' },
            { color: 'bg-orange-500', label: 'Fair (40-59%)' },
            { color: 'bg-red-500', label: 'Low (<40%)' },
          ].map((item, index) => (
            <div key={index} className="flex items-center text-xs">
              <span className={clsx('inline-block w-2 h-2 rounded-full mr-2', item.color)} />
              <span className="text-gray-700">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
