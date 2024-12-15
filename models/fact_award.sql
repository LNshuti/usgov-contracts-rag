-- models/fact_award.sql
MODEL (
    name       'fact_award',
    kind       'incremental',
    owner      'data_eng_team',
    cron       '@daily',
    description 'Fact table containing awards linked to dimension tables.'
);

WITH src AS (
    SELECT
        c.department_ind_agency AS agency_name,
        c.sub_tier AS sub_tier_name,
        c.cgac AS cgac_code,
        c.awardnumber,
        c.awarddate,
        c.award,
        c.awardee,
        c.type,
        c.basetype,
        c.posteddate,
        c.office,
        c.fpds_code,
        c.aac_code,
        c.active,
        c.popstreetaddress AS street_address,
        c.popcity AS pop_city,
        c.popstate AS pop_state,
        c.popzip AS pop_zip,
        c.popcountry AS pop_country,
        c.state AS aw_state,
        c.city AS aw_city,
        c.zipcode AS aw_zip,
        c.countrycode AS aw_country
    FROM source.contract_data AS c
),
agencies AS (
    SELECT agency_key, agency_name, sub_tier_name, cgac_code FROM dim_agency
),
locations AS (
    SELECT location_key, street_address, city, state, zip, country FROM dim_location
),
awardee_locs AS (
    SELECT awardee_location_key, state, city, zipcode, countrycode FROM dim_awardee_location
),
fact AS (
    SELECT
        a.agency_key,
        l.location_key,
        al.awardee_location_key,
        s.awardnumber,
        s.awarddate,
        s.award,
        s.awardee,
        s.type,
        s.basetype,
        s.posteddate,
        s.office,
        s.fpds_code,
        s.aac_code,
        s.active
    FROM src s
    LEFT JOIN agencies a
        ON s.agency_name = a.agency_name
       AND s.sub_tier_name = a.sub_tier_name
       AND s.cgac_code = a.cgac_code
    LEFT JOIN locations l
        ON s.street_address = l.street_address
       AND s.pop_city = l.city
       AND s.pop_state = l.state
       AND s.pop_zip = l.zip
       AND s.pop_country = l.country
    LEFT JOIN awardee_locs al
        ON s.aw_state = al.state
       AND s.aw_city = al.city
       AND s.aw_zip = al.zipcode
       AND s.aw_country = al.countrycode
)
SELECT * FROM fact;
