# Database Migration Notes

## Overview
This document describes the database migrations created to remove ZIP code dependencies and align the database schema with the SQLAlchemy models.

## Migrations Created

### 1. Migration: `2988e3a4a9f4_remove_zipcode_fields.py`
**Purpose**: Remove the `source_zipcode` field from the `gyms` table.

**Changes**:
- Drops the `ix_gyms_source_zipcode` index
- Removes the `source_zipcode` column from the `gyms` table

**Rationale**: The application is transitioning from ZIP code-based searches to location-based searches that support both city names and ZIP codes.

### 2. Migration: `71f376dbb795_sync_models_with_schema.py`
**Purpose**: Sync the database schema with the SQLAlchemy models. The initial migration created tables that don't match the current model definitions.

**Major Changes**:
1. **Gyms table**: Convert location from GEOGRAPHY to GEOMETRY type
2. **Data Sources table**:
   - Rename `source_type` → `name`
   - Rename `data` → `api_response`
   - Add `confidence` column
   - Remove `url` and `created_at` columns
3. **Reviews table**: Transform from individual reviews to aggregated review data
   - Remove individual review fields
   - Add aggregation fields (review_count, sentiment_score, etc.)
4. **Users table**:
   - Remove `username`, `full_name`, `is_superuser`
   - Add `is_verified`, `first_name`, `last_name`, etc.
5. **Saved Searches table**:
   - Expand from simple `search_params` JSON to individual columns
   - Add alert and notification fields
6. **Metropolitan Areas table**:
   - Add many new fields for market intelligence
   - Remove `state` and `area_sq_miles`
   - Remove `zipcodes` JSON column

### 3. Migration: `19952fea7e7d_transition_saved_searches_to_location.py`
**Purpose**: Transition SavedSearch from zipcode-based to location-based searches.

**Changes**:
- Rename `zipcode` column to `location`
- Expand field size from 10 to 100 characters
- Add `resolved_latitude` and `resolved_longitude` columns
- Update indexes accordingly

## Running the Migrations

To apply these migrations:

```bash
cd backend
python3 -m alembic upgrade head
```

To check current migration status:

```bash
python3 -m alembic current
```

To see migration history:

```bash
python3 -m alembic history
```

## Rollback Instructions

To rollback all migrations:

```bash
python3 -m alembic downgrade 001
```

To rollback one migration at a time:

```bash
python3 -m alembic downgrade -1
```

## Important Notes

1. **Data Loss Warning**: The sync migration (`71f376dbb795`) will aggregate existing review data. Individual review details will be lost.

2. **PostGIS Requirement**: The database must have the PostGIS extension installed for spatial data support.

3. **ZIP Code Transition**: After these migrations, ZIP codes can still be used as location inputs, but they'll be stored in the generic `location` field along with city names.

4. **Model Alignment**: These migrations bring the database schema in line with the SQLAlchemy models defined in `app/models/`.

## Future Considerations

- Consider adding a migration to populate `resolved_latitude` and `resolved_longitude` for existing saved searches
- The `metropolitan_areas.zipcodes` column was removed but might be useful for analytics - consider if this data should be preserved elsewhere
