/**
 * GymIntel Web Application - Main App Component
 */

import React from 'react';
import { ApolloProvider } from '@apollo/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { apolloClient } from './lib/apollo';
import { HomePage } from './pages/HomePage';
import { SearchPage } from './pages/SearchPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { MetroPage } from './pages/MetroPage';
import { Layout } from './components/Layout';

function App() {
  return (
    <ApolloProvider client={apolloClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Layout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/metro/:code" element={<MetroPage />} />
              <Route path="/metro" element={<MetroPage />} />
            </Routes>
          </Layout>
        </div>
      </Router>
    </ApolloProvider>
  );
}

export default App;