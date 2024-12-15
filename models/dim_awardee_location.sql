-- models/dim_awardee_location.sql
MODEL (
    name       'dim_awardee_location',
    kind       'incremental',
    owner      'data_eng_team',
    cron       '@daily',
    description 'Dimension table for awardee location data.',
    audits     ['not_null(awardee_location_key)', 'unique(awardee_location_key)']
);

WITH distinct_awardee_locs AS (
    SELECT DISTINCT
        state,
        city,
        zipcode,
        countrycode
    FROM source.contract_data
    WHERE city IS NOT NULL
),
with_keys AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY city, state, zipcode) AS awardee_location_key,
        state,
        city,
        zipcode,
        countrycode
    FROM distinct_awardee_locs
)
SELECT * FROM with_keys;
