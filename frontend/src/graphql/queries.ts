/**
 * GraphQL Queries for GymIntel Application
 */

import { gql } from '@apollo/client';

// Fragment for Gym data
export const GYM_FRAGMENT = gql`
  fragment GymFragment on Gym {
    id
    name
    address
    coordinates {
      latitude
      longitude
    }
    phone
    website
    instagram
    confidence
    matchConfidence
    rating
    reviewCount
    sources {
      name
      confidence
      lastUpdated
    }
    reviews {
      rating
      reviewCount
      sentimentScore
      source
      lastUpdated
    }
    sourceZipcode
    metropolitanAreaCode
    createdAt
    updatedAt
  }
`;

// Search gyms query
export const SEARCH_GYMS = gql`
  ${GYM_FRAGMENT}
  query SearchGyms(
    $zipcode: String!
    $radius: Float = 10.0
    $limit: Int = 50
    $filters: SearchFilters
  ) {
    searchGyms(
      zipcode: $zipcode
      radius: $radius
      limit: $limit
      filters: $filters
    ) {
      zipcode
      coordinates {
        latitude
        longitude
      }
      radiusMiles
      timestamp
      gyms {
        ...GymFragment
      }
      totalResults
      yelpResults
      googleResults
      mergedCount
      avgConfidence
      executionTimeSeconds
      useGoogle
    }
  }
`;

// Get gym by ID
export const GET_GYM_BY_ID = gql`
  ${GYM_FRAGMENT}
  query GetGymById($gymId: ID!) {
    gymById(gymId: $gymId) {
      ...GymFragment
    }
  }
`;

// Get metropolitan area
export const GET_METROPOLITAN_AREA = gql`
  query GetMetropolitanArea($code: String!) {
    metropolitanArea(code: $code) {
      id
      name
      code
      description
      state
      population
      densityCategory
      marketCharacteristics
      zipCodes
      statistics {
        totalGyms
        mergedGyms
        mergeRate
        averageConfidence
        sourceDistribution
        gymsPerZip
        deduplicationRate
      }
    }
  }
`;

// List all metropolitan areas
export const LIST_METROPOLITAN_AREAS = gql`
  query ListMetropolitanAreas {
    listMetropolitanAreas {
      id
      name
      code
      description
      state
      population
      densityCategory
      marketCharacteristics
      zipCodes
      statistics {
        totalGyms
        mergedGyms
        mergeRate
        averageConfidence
        sourceDistribution
        gymsPerZip
        deduplicationRate
      }
    }
  }
`;

// Get gym analytics
export const GET_GYM_ANALYTICS = gql`
  query GetGymAnalytics($zipcode: String!) {
    gymAnalytics(zipcode: $zipcode) {
      zipcode
      totalGyms
      confidenceDistribution
      sourceBreakdown
      ratingAnalysis
      densityScore
      marketSaturation
    }
  }
`;

// Market gap analysis
export const MARKET_GAP_ANALYSIS = gql`
  query MarketGapAnalysis($zipcode: String!, $radius: Float = 10.0) {
    marketGapAnalysis(zipcode: $zipcode, radius: $radius) {
      areaDescription
      coordinates {
        latitude
        longitude
      }
      gapScore
      populationDensity
      nearestGymDistance
      reasoning
    }
  }
`;

// Get gyms by metro
export const GET_GYMS_BY_METRO = gql`
  ${GYM_FRAGMENT}
  query GetGymsByMetro($metroCode: String!, $limit: Int = 100, $offset: Int = 0) {
    gymsByMetro(metroCode: $metroCode, limit: $limit, offset: $offset) {
      ...GymFragment
    }
  }
`;
