import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { GymCard } from '../GymCard'

const mockGym = {
  id: '1',
  name: 'Test Gym',
  address: '123 Main St, Test City, TC 12345',
  phone: '(555) 123-4567',
  website: 'https://testgym.com',
  rating: 4.5,
  reviewCount: 150,
  confidence: 0.85,
  matchConfidence: 0.85,
  sources: [
    { name: 'Yelp', confidence: 0.9, lastUpdated: '2023-01-01' },
    { name: 'Google', confidence: 0.8, lastUpdated: '2023-01-01' }
  ],
  reviews: [],
  coordinates: {
    latitude: 40.7128,
    longitude: -74.0060
  },
  createdAt: '2023-01-01',
  updatedAt: '2023-01-01'
}

describe('GymCard', () => {
  it('renders gym information correctly', () => {
    render(<GymCard gym={mockGym} />)

    expect(screen.getByText('Test Gym')).toBeInTheDocument()
    expect(screen.getByText('123 Main St, Test City, TC 12345')).toBeInTheDocument()
    expect(screen.getByText('(555) 123-4567')).toBeInTheDocument()
    expect(screen.getByText('4.5')).toBeInTheDocument()
    expect(screen.getByText('(150 reviews)')).toBeInTheDocument()
  })

  it('displays confidence score', () => {
    render(<GymCard gym={mockGym} />)
    expect(screen.getByText(/85%/)).toBeInTheDocument()
  })

  it('shows data sources', () => {
    render(<GymCard gym={mockGym} />)
    expect(screen.getByText(/Yelp/)).toBeInTheDocument()
    expect(screen.getByText(/Google/)).toBeInTheDocument()
  })

  it('handles missing optional fields gracefully', () => {
    const minimalGym = {
      id: '2',
      name: 'Minimal Gym',
      address: '456 Oak St',
      confidence: 0.75,
      matchConfidence: 0.75,
      sources: [{ name: 'Yelp', confidence: 0.75, lastUpdated: '2023-01-01' }],
      reviews: [],
      coordinates: { latitude: 40.7128, longitude: -74.0060 },
      createdAt: '2023-01-01',
      updatedAt: '2023-01-01'
    }

    render(<GymCard gym={minimalGym} />)
    expect(screen.getByText('Minimal Gym')).toBeInTheDocument()
    // Check for confidence in the badge by looking for "High (75%)"
    expect(screen.getByText(/High.*75%/)).toBeInTheDocument()
  })
})
