-- Metric 1: MDU admissions with an admit date in September 2026 (cancelled excluded)
SELECT COUNT(*) AS admissions
FROM admissions
WHERE branch = 'MDU'
  AND status = 'Active'
  AND admit_date BETWEEN '2026-09-01' AND '2026-09-30';
