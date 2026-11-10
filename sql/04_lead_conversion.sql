-- Metric 4: lead conversion by channel for leads created in September 2026 (IST date).
-- Converted = the lead's phone matches a patient with a valid (MDU, not cancelled) admission
-- on the lead date or within the next 30 days.
WITH sep_leads AS (
    SELECT lead_id, channel, phone_norm, created_date_ist
    FROM leads
    WHERE created_date_ist BETWEEN '2026-09-01' AND '2026-09-30'
),
flagged AS (
    SELECT l.channel,
           EXISTS (
               SELECT 1
               FROM patients p
               JOIN admissions a ON a.patient_id = p.patient_id
               WHERE p.phone_norm = l.phone_norm
                 AND a.branch = 'MDU'
                 AND a.status = 'Active'
                 AND a.admit_date BETWEEN l.created_date_ist AND date(l.created_date_ist, '+30 days')
           ) AS converted
    FROM sep_leads l
)
SELECT channel, COUNT(*) AS leads, SUM(converted) AS converted_leads,
       ROUND(100.0 * SUM(converted) / COUNT(*), 1) AS conversion_rate_pct
FROM flagged GROUP BY channel
UNION ALL
SELECT 'TOTAL', COUNT(*), SUM(converted), ROUND(100.0 * SUM(converted) / COUNT(*), 1)
FROM flagged;
