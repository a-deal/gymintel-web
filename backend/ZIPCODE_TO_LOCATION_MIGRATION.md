# ZIP Code to Location Migration Summary

## Overview
Updated all GraphQL resolvers in the backend to use 'location' (city names only) instead of 'zipcode' for gym searches and analytics.

## Changes Made

### 1. GraphQL Resolvers (`app/graphql/resolvers.py`)
- Updated `search_gyms_by_location` to remove zipcode references and use location/city instead
- Modified `gym_analytics` to accept `location` parameter instead of `zipcode`
- Updated `market_gap_analysis` to use `location` instead of `zipcode`
- Changed `import_gym_data` to accept `location` parameter
- Updated `_store_cli_results` to handle location-based storage
- Modified metropolitan area resolvers to use `cities` instead of `zip_codes`
- Added TODO comments for CLI integration (CLI still expects zipcodes)

### 2. GraphQL Schema (`app/graphql/schema.py`)
- Already had `source_city` field in Gym type (no changes needed)
- Already had `location` field in GymAnalytics type (no changes needed)
- Already had `cities` field in MetropolitanArea type (no changes needed)

### 3. Database Models (`app/models/gym.py`)
- Replaced `source_zipcode` column with `source_city` column (String(255))
- Updated column comment to reflect city storage

### 4. Geocoding Service (`app/services/geocoding.py`)
- Updated documentation to reflect primary focus on city-to-coordinates conversion
- Modified `search_location` to return location info dict directly (removed tuple return)
- Kept backward compatibility for zipcode inputs

### 5. Seed Data (`app/seed_data.py`)
- Updated sample metropolitan areas to use `cities` instead of `zipcodes`
- Changed all gym seed data to use `source_city` instead of `source_zipcode`
- Updated `refresh_gym_data` function to accept `location` parameter (currently disabled)

### 6. Database Migration
- Created new migration file: `migrations/versions/2025_07_02_1600-add_source_city.py`
- Adds `source_city` column to gyms table with index
- Works in conjunction with existing migration that removes `source_zipcode`

## Notes

### CLI Integration
The CLI bridge service (`app/services/cli_bridge.py`) was NOT modified because it interfaces with an external CLI tool that still expects zipcodes. The CLI bridge acts as an adapter between the zipcode-based CLI and our city-based web application.

### Current Limitations
1. CLI search functionality is temporarily disabled for city-based searches
2. The external CLI tool needs to be updated to support city-based searches
3. For now, the GraphQL API returns empty results when attempting CLI searches

### Next Steps
1. Run database migrations to apply schema changes
2. Update the external CLI tool to support city-based searches
3. Re-enable CLI search functionality in the resolvers
4. Update frontend to use city names instead of zipcodes in API calls

## Migration Commands
```bash
# Run the migrations
cd backend
alembic upgrade head
```
