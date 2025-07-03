/**
 * GraphQL Mutations for GymIntel Application
 */

import { gql } from '@apollo/client';

// Import gym data mutation
export const IMPORT_GYM_DATA = gql`
  mutation ImportGymData($location: String!, $data: [GymDataInput!]!) {
    importGymData(location: $location, data: $data) {
      success
      gymsImported
      gymsUpdated
      errors
      importDurationSeconds
    }
  }
`;

// Save search preferences
export const SAVE_SEARCH = gql`
  mutation SaveSearch(
    $userId: String!
    $location: String!
    $radius: Float!
    $name: String
  ) {
    saveSearch(
      userId: $userId
      location: $location
      radius: $radius
      name: $name
    ) {
      id
      userId
      location
      radius
      name
      createdAt
      lastRun
    }
  }
`;

// Trigger CLI import
export const TRIGGER_CLI_IMPORT = gql`
  mutation TriggerCliImport($location: String!, $radius: Float = 10.0) {
    triggerCliImport(location: $location, radius: $radius)
  }
`;

// Trigger gym search
export const TRIGGER_GYM_SEARCH = gql`
  mutation TriggerGymSearch($location: String!, $radius: Float = 10.0) {
    triggerGymSearch(location: $location, radius: $radius)
  }
`;
