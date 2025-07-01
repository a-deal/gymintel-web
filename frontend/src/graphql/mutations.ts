/**
 * GraphQL Mutations for GymIntel Application
 */

import { gql } from '@apollo/client';

// Import gym data mutation
export const IMPORT_GYM_DATA = gql`
  mutation ImportGymData($zipcode: String!, $data: [GymDataInput!]!) {
    importGymData(zipcode: $zipcode, data: $data) {
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
    $zipcode: String!
    $radius: Float!
    $name: String
  ) {
    saveSearch(
      userId: $userId
      zipcode: $zipcode
      radius: $radius
      name: $name
    ) {
      id
      userId
      zipcode
      radius
      name
      createdAt
      lastRun
    }
  }
`;

// Trigger CLI import
export const TRIGGER_CLI_IMPORT = gql`
  mutation TriggerCliImport($zipcode: String!, $radius: Float = 10.0) {
    triggerCliImport(zipcode: $zipcode, radius: $radius)
  }
`;