# Google Places API Setup Guide

This guide covers setting up Google Places API for city autocomplete functionality in the GymIntel Web Application.

## Overview

The Google Places API integration provides:
- **City Autocomplete**: Real-time city name suggestions as users type
- **Input Validation**: Ensures only valid US city names are accepted
- **Geocoding Enhancement**: Better accuracy for city-to-coordinate conversion

## Prerequisites

1. Google Cloud Platform (GCP) account
2. Billing enabled on GCP (required for Places API)
3. A project created in GCP Console

## Setup Steps

### 1. Enable Required APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Navigate to "APIs & Services" → "Library"
4. Search for and enable:
   - **Places API**
   - **Geocoding API** (optional, for backup)

### 2. Create API Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "API Key"
3. Name it: `gymintel-places-api-key`
4. Click "Restrict Key" for security

### 3. Configure API Key Restrictions

#### Application Restrictions
- **HTTP referrers (web sites)** for frontend-only usage
- Add allowed referrers:
  ```text
  http://localhost:3000/*
  http://localhost:5173/*
  https://gymintel-web.vercel.app/*
  https://gymintel-web-staging.vercel.app/*
  https://*.vercel.app/* (for preview deployments)
  ```

#### API Restrictions
- Restrict to specific APIs:
  - Places API
  - Geocoding API

### 4. Set Environment Variables

#### Backend (.env)
```bash
GOOGLE_PLACES_API_KEY=your-api-key-here
```

#### Railway (Production & Staging)
1. Go to Railway Dashboard
2. Select your project
3. Navigate to "Variables"
4. Add: `GOOGLE_PLACES_API_KEY=your-api-key-here`

## Usage in Application

### Backend Integration

The Google Places service is available at `backend/app/services/google_places.py`:

```python
from app.services.google_places import google_places_service

# Get city autocomplete suggestions
suggestions = await google_places_service.autocomplete_cities("Aus")
# Returns: [{"place_id": "...", "description": "Austin, TX, USA", ...}]

# Validate city input
is_valid, details = await google_places_service.validate_city_input("Austin")
# Returns: (True, PlaceDetails object with coordinates, postal code, etc.)
```

### Frontend Integration

The SearchInput component (`frontend/src/components/SearchInput.tsx`) provides:
- Debounced autocomplete (300ms delay)
- Keyboard navigation (arrow keys, enter, escape)
- Visual feedback with city icons
- Auto-submit on selection

### GraphQL Query

```graphql
query CityAutocomplete($inputText: String!, $country: String = "us") {
  cityAutocomplete(inputText: $inputText, country: $country) {
    placeId
    description
    mainText
    secondaryText
  }
}
```

## API Quotas and Pricing

### Free Tier (Monthly)
- **Places Autocomplete**: $200 credit (~40,000 requests)
- **Place Details**: $200 credit (~11,000 requests)
- **Geocoding**: $200 credit (~40,000 requests)

### Pricing Beyond Free Tier
- **Autocomplete**: $2.83 per 1,000 requests
- **Place Details**: $17.00 per 1,000 requests
- **Geocoding**: $5.00 per 1,000 requests

### Optimization Tips
1. **Debounce requests**: Already implemented (300ms)
2. **Cache results**: Consider Redis for repeated queries
3. **Session tokens**: Use for autocomplete sessions (reduces cost)
4. **Restrict to cities**: Already implemented with `types=(cities)`

## Monitoring Usage

### Google Cloud Console
1. Go to "APIs & Services" → "Metrics"
2. Select "Places API"
3. Monitor:
   - Request count
   - Error rate
   - Latency
   - Quota usage

### Set Up Alerts
1. Go to "Monitoring" → "Alerting"
2. Create alert for:
   - Quota approaching limit
   - High error rate
   - Unusual spike in requests

## Security Best Practices

1. **Never expose API key in frontend code**
   - All requests go through backend
   - Frontend uses GraphQL endpoint

2. **Restrict API key**
   - IP restrictions for backend servers
   - API restrictions to only needed services

3. **Monitor for abuse**
   - Set up billing alerts
   - Review usage patterns regularly

4. **Rotate keys periodically**
   - Create new key
   - Update environment variables
   - Delete old key after verification

## Troubleshooting

### Common Issues

1. **"REQUEST_DENIED" error**
   - Check API key is valid
   - Verify Places API is enabled
   - Check billing is enabled

2. **No autocomplete results**
   - Verify `types=(cities)` parameter
   - Check country restriction
   - Try without country filter

3. **CORS errors**
   - Ensure requests go through backend
   - Never call Google API directly from frontend

### Debug Commands

```bash
# Test API key (backend)
cd backend
python -c "from app.config import settings; print(settings.google_places_api_key)"

# Test autocomplete
curl "http://localhost:8000/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { cityAutocomplete(inputText: \"Aus\") { mainText description } }"}'
```

## Implementation Checklist

- [x] Enable Places API in Google Cloud Console
- [x] Create and restrict API key
- [x] Add GOOGLE_PLACES_API_KEY to backend .env
- [x] Create google_places.py service
- [x] Update geocoding.py to use Google Places
- [x] Add cityAutocomplete GraphQL query
- [x] Create SearchInput component with autocomplete
- [x] Update SearchPage and HomePage
- [ ] Add API key to Railway environments
- [ ] Test in staging environment
- [ ] Monitor initial usage
- [ ] Set up billing alerts

## Future Enhancements

1. **Session Tokens**: Implement autocomplete sessions for cost savings
2. **Redis Caching**: Cache popular city searches
3. **International Support**: Remove US-only restriction
4. **Place Photos**: Add city photos to search results
5. **Nearby Search**: Find gyms near selected city center
