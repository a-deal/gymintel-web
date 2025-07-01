import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { MockedProvider } from '@apollo/client/testing'
import App from '../App'

const AppWithProviders = () => (
  <BrowserRouter>
    <MockedProvider mocks={[]} addTypename={false}>
      <App />
    </MockedProvider>
  </BrowserRouter>
)

describe('App', () => {
  it('renders without crashing', () => {
    render(<AppWithProviders />)
    expect(document.body).toBeInTheDocument()
  })

  it('displays the GymIntel branding', () => {
    render(<AppWithProviders />)
    expect(screen.getByText(/gymintel/i)).toBeInTheDocument()
  })
})
