-- models/dim_agency.sql
MODEL (
    name       'dim_agency',
    kind       'incremental', -- or 'full', depending on loading strategy
    owner      'data_eng_team',
    cron       '@daily',
    description 'Dimension table for agencies and sub-tier agencies.',
    audits     ['not_null(agency_key)', 'unique(agency_key)']
);

WITH distinct_agencies AS (
    SELECT DISTINCT
        department_ind_agency AS agency_name,
        sub_tier AS sub_tier_name,
        cgac AS cgac_code
    FROM source.contract_data
),
with_keys AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY agency_name, sub_tier_name, cgac_code) AS agency_key,
        agency_name,
        sub_tier_name,
        cgac_code
    FROM distinct_agencies
)
SELECT * FROM with_keys;
