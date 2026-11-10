# Data issues found

| # | Issue | How handled | Changes a number? |
|---|---|---|---|
| 1 | Bill `B00002` appears twice (identical rows) | Primary key on `bill_id`; the load keeps one | Yes - revenue would be 86,400 too high (5,202,500 vs 5,116,100) |
| 2 | Two leads (`L00260`, `L00280`) appear twice in the CRM pages | Primary key on `lead_id`; keep one | Yes - leads total would be 158 instead of 156 |
| 3 | Lead times are UTC; the month is defined in IST | Convert to IST at load (`created_at_ist`, `created_date_ist`) | Yes - counting by UTC date gives 160 leads instead of 156 |
| 4 | Phone numbers in 5+ formats (`+91 55500 00001`, `05550000001`, `55500-00001`, `915550000001`, ...) | Normalise to the bare 10 digits at load (`phone_norm`) | Yes - without it almost no lead would match a patient |
| 5 | 13 bills belong to cancelled admissions | Excluded by joining to admissions and requiring status = Active | Yes - including them adds revenue (5,232,300 vs 5,116,100) |
| 6 | 13 bills have `is_cancelled = 1` | Excluded | Yes (part of the above total) |
| 7 | Admission `A0003` uses department `D9`, which is not in `departments.csv` | Kept: shown as "UNKNOWN DEPT (D9)" via LEFT JOIN, never dropped | Yes - 42,500 sits in its own row; the total stays right |
| 8 | Admission `A0019`: discharged 14 Sep, admitted 17 Sep (discharge before admit) | Left out of average length of stay; flagged for the hospital to correct | Yes - LOS would be 6.80 instead of 6.91 |
| 9 | 20 admissions have no discharge date (still admitted) | Not in length of stay (only admissions discharged in September count) | No - correct by definition |
| 10 | 29 September bills belong to admissions admitted outside September | Counted by bill date, as the brief says | No - by design |
| 11 | Leads whose phone matches no patient | Counted as leads, not as converted | No - by design |

Assumptions: a same-day discharge counts as 1 day; every other stay is discharge date minus admit date;
a lead's own date is day 0 of the 30-day window; leads and patients are matched on phone only.
