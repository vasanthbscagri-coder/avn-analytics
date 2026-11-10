# AVN Group – Analytics Engineer: take-home assignment

Thank you for your interest in the Analytics Engineer role. This assignment is the kind of work the role does
every month: load data from a hospital system and a CRM, compute agreed metrics exactly, and say plainly what
the numbers mean and what in the data could not be trusted.

**Time:** about 3 to 4 hours. Please do not spend more than 5.
**Deadline:** Tuesday 10 November 2026, 6 pm.
**Submit:** one zip file of your git repository (include the `.git` folder so we can see your commits), emailed
to Mr. R. Thangapandy.

**AI tools are welcome.** We use AI coding assistants every day and expect you to. Tell us in your README which
tools you used and for what. In the interview you will be asked to explain and change your own code live, so
make sure you understand everything you submit.

All data in this pack is made up. No real patient, phone number or amount appears in it.

## The data (`data/`)

| File | What it is |
|---|---|
| `departments.csv` | Department codes and names |
| `patients.csv` | Registered patients with their phone number, as typed at the front desk |
| `admissions.csv` | Inpatient admissions. `branch` is `MDU` (main hospital, Madurai) or `SAT` (satellite clinics). `discharge_date` is blank while the patient is still admitted. `status` is `Active` or `Cancelled` |
| `bills.csv` | Inpatient bills. `gross_amount` includes GST; `gst_amount` is the GST in it. `is_cancelled` = 1 for cancelled bills |
| `crm_api/leads_page_*.json` | Enquiries (leads) exactly as returned by our CRM's API, one file per page. Start at `leads_page_1.json` and follow `info.next_page` until it is `null`. `created_at` is in UTC |

Treat the CSV files as an export from a database you may only read, and the JSON files as responses from an API.
Do not edit the data files by hand.

## The metrics (all for September 2026)

All dates are Indian Standard Time (UTC+5:30). "September" means 1 Sep 2026 00:00 to 30 Sep 2026 23:59 IST.
Only the **main hospital (`MDU`)** counts. **Cancelled admissions never count**, and nor do their bills.

1. **Admissions:** number of admissions with an admission date in September.
2. **Average length of stay (days):** over admissions *discharged* in September, the average of
   (discharge date − admission date) in days, counting a same-day discharge as 1 day.
3. **Net revenue (excluding GST) by department:** sum of (gross amount − GST) of the bills dated in September
   that are not cancelled, by the department of the admission; plus the total.
4. **Lead conversion by channel:** of the leads created in September, the share that became an admission. A lead
   has converted if its phone number belongs to a patient with an admission (counted under the rules above)
   admitted on the lead's date or within the 30 days after it. Give leads, converted leads and the rate for each
   channel, and the total. Phone numbers are written in different ways; the same number must still match.

## What to do

1. **Load.** Write Python that loads all the CSV files and all the API pages into a database: SQLite is fine,
   MySQL or SQL Server if you prefer. Running the load twice must not create duplicate rows.
2. **Compute.** Compute the four metrics **in SQL**, one query per metric, saved as `.sql` files.
3. **Check.** The data has problems, as real data does. Find them. For each one, write down what it is, how you
   handled it, and whether it changes a number above.
4. **Test.** Add at least three automated tests (pytest or similar) for the parts most likely to go wrong.
5. **Explain.** Write a note of no more than one page to the hospital's operations manager, who is not
   technical: the four September numbers, what they mean, and anything in the data they should know about
   before relying on them.
6. **README.** How to set up and run everything in a few commands, and which AI tools you used and how.

## What we look at

- Are the numbers right? We know the correct answers.
- Did you find the problems in the data, and handle them sensibly instead of hiding them?
- Is the code simple, readable, re-runnable and tested? Do the commits tell the story of the work?
- Can a non-technical manager understand and trust your note?

Questions about the assignment can be sent to Mr. Thangapandy. If something is unclear, make a sensible
assumption, write it down, and carry on: that is part of the job too.
