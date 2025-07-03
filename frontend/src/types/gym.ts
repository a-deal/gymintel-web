/**
 * TypeScript type definitions for GymIntel application
 */

export interface Coordinates {
  latitude: number;
  longitude: number;
}

export interface DataSource {
  name: string;
  confidence: number;
  lastUpdated: string;
}

export interface Review {
  rating: number;
  reviewCount: number;
  sentimentScore?: number;
  source: string;
  lastUpdated: string;
}

export interface Gym {
  id: string;
  name: string;
  address: string;
  coordinates: Coordinates;
  phone?: string;
  website?: string;
  instagram?: string;
  confidence: number;
  matchConfidence: number;
  rating?: number;
  reviewCount?: number;
  sources: DataSource[];
  reviews: Review[];
  sourceCity?: string;
  metropolitanAreaCode?: string;
  createdAt: string;
  updatedAt: string;
}

export interface SearchResult {
  location: string;
  coordinates: Coordinates;
  radiusMiles: number;
  timestamp: string;
  gyms: Gym[];
  totalResults: number;
  yelpResults: number;
  googleResults: number;
  mergedCount: number;
  avgConfidence: number;
  executionTimeSeconds: number;
  useGoogle: boolean;
}

export interface MetroStatistics {
  totalGyms: number;
  mergedGyms: number;
  mergeRate: number;
  averageConfidence: number;
  sourceDistribution: string; // JSON string
  gymsPerCity: string; // JSON string
  deduplicationRate: number;
}

export interface MetropolitanArea {
  id: string;
  name: string;
  code: string;
  description: string;
  state: string;
  population?: number;
  densityCategory: string;
  marketCharacteristics: string[];
  cities: string[];
  statistics: MetroStatistics;
}

export interface GymAnalytics {
  location: string;
  totalGyms: number;
  confidenceDistribution: string; // JSON string
  sourceBreakdown: string; // JSON string
  ratingAnalysis: string; // JSON string
  densityScore: number;
  marketSaturation: string;
}

export interface MarketGap {
  areaDescription: string;
  coordinates: Coordinates;
  gapScore: number;
  populationDensity: number;
  nearestGymDistance: number;
  reasoning: string;
}

export interface SearchFilters {
  minRating?: number;
  maxDistance?: number;
  minConfidence?: number;
  sources?: string[];
  hasWebsite?: boolean;
  hasInstagram?: boolean;
}

export interface SearchProgress {
  searchId: string;
  status: string;
  progressPercentage: number;
  currentStep: string;
  estimatedCompletion?: string;
}

export interface ImportResult {
  success: boolean;
  gymsImported: number;
  gymsUpdated: number;
  errors: string[];
  importDurationSeconds: number;
}

export interface SavedSearch {
  id: string;
  userId: string;
  location: string;
  radius: number;
  name?: string;
  createdAt: string;
  lastRun?: string;
}
