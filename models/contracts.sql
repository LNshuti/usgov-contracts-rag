MODEL (
  name contracts,
  kind VIEW,
  cron '@daily',
  grain [id]
);

SELECT 
  id,
  contract_name,
  amount,
  date
FROM source_contracts
