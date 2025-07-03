/**
 * GraphQL Subscriptions for GymIntel Application
 */

import { gql } from '@apollo/client';
import { GYM_FRAGMENT } from './queries';

// Subscribe to gym updates for a specific area
export const GYM_UPDATES_SUBSCRIPTION = gql`
  ${GYM_FRAGMENT}
  subscription GymUpdates($location: String!) {
    gymUpdates(location: $location) {
      ...GymFragment
    }
  }
`;

// Subscribe to search progress updates
export const SEARCH_PROGRESS_SUBSCRIPTION = gql`
  subscription SearchProgress($searchId: String!) {
    searchProgress(searchId: $searchId) {
      searchId
      status
      progressPercentage
      currentStep
      estimatedCompletion
      message
      locationInfo
    }
  }
`;
