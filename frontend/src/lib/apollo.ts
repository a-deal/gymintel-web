/**
 * Apollo Client Configuration
 * Handles GraphQL connections, caching, and subscriptions
 */

import { ApolloClient, InMemoryCache, createHttpLink, split } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

// HTTP Link for queries and mutations
const httpLink = createHttpLink({
  uri: import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql',
});

// WebSocket Link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: import.meta.env.VITE_GRAPHQL_WS_ENDPOINT || 'ws://localhost:8000/graphql',
  }),
);

// Auth link for future authentication
const authLink = setContext((_, { headers }) => {
  // Get the authentication token from local storage if it exists
  const token = localStorage.getItem('token');

  return {
    headers: {
      ...headers,
      authorization: token ? `Bearer ${token}` : "",
    }
  };
});

// Split link - use WebSocket for subscriptions, HTTP for queries/mutations
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  authLink.concat(httpLink),
);

// Apollo Client instance
export const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          searchGyms: {
            keyArgs: ['zipcode', 'radius'],
            merge(existing, incoming) {
              return incoming;
            },
          },
          gymsByMetro: {
            keyArgs: ['metro_code'],
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            },
          },
        },
      },
      Gym: {
        fields: {
          sources: {
            merge(existing = [], incoming) {
              return incoming;
            },
          },
          reviews: {
            merge(existing = [], incoming) {
              return incoming;
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      errorPolicy: 'all',
    },
    query: {
      errorPolicy: 'all',
    },
  },
});

// Helper function to clear cache
export const clearApolloCache = () => {
  apolloClient.cache.reset();
};

// Helper function to refetch all active queries
export const refetchAllQueries = () => {
  apolloClient.refetchQueries({
    include: 'active',
  });
};
