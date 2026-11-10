-- Metric 3: net revenue (gross - GST) of non-cancelled bills dated in September 2026,
-- for MDU, non-cancelled admissions, grouped by the admission's department. Plus total.
WITH sep AS (
    SELECT COALESCE(d.name, 'UNKNOWN DEPT (' || a.dept_id || ')') AS department,
           b.gross_amount - b.gst_amount AS net
    FROM bills b
    JOIN admissions a ON a.admission_id = b.admission_id
    LEFT JOIN departments d ON d.dept_id = a.dept_id
    WHERE a.branch = 'MDU'
      AND a.status = 'Active'
      AND b.is_cancelled = 0
      AND b.bill_date BETWEEN '2026-09-01' AND '2026-09-30'
)
SELECT department, SUM(net) AS net_revenue FROM sep GROUP BY department
UNION ALL
SELECT 'TOTAL', SUM(net) FROM sep;
