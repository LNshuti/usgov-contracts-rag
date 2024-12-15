-- models/dim_location.sql
MODEL (
    name       'dim_location',
    kind       'incremental',
    owner      'data_eng_team',
    cron       '@daily',
    description 'Dimension table for location data (place of performance).',
    audits     ['not_null(location_key)', 'unique(location_key)']
);

WITH distinct_locations AS (
    SELECT DISTINCT
        popstreetaddress AS street_address,
        popcity AS city,
        popstate AS state,
        popzip AS zip,
        popcountry AS country
    FROM source.contract_data
    WHERE popcity IS NOT NULL
)
, with_keys AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY city, state, zip) AS location_key,
        street_address,
        city,
        state,
        zip,
        country
    FROM distinct_locations
)
SELECT * FROM with_keys;
