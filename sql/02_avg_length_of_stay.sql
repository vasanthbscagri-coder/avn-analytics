-- Metric 2: average length of stay (days) for MDU admissions DISCHARGED in September 2026.
-- Same-day discharge counts as 1 day. Rows where discharge is before admit are bad data
-- and are left out (see DATA_ISSUES.md).
WITH stays AS (
    SELECT julianday(discharge_date) - julianday(admit_date) AS days
    FROM admissions
    WHERE branch = 'MDU'
      AND status = 'Active'
      AND discharge_date BETWEEN '2026-09-01' AND '2026-09-30'
      AND discharge_date >= admit_date
)
SELECT ROUND(AVG(CASE WHEN days = 0 THEN 1 ELSE days END), 2) AS avg_length_of_stay_days,
       COUNT(*) AS admissions_counted
FROM stays;
