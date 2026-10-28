# OTBI Report Fix: Cost Accounting to General Ledger Reconciliation

An Oracle Transactional Business Intelligence (OTBI) analysis used to reconcile one balance sheet account (cost accounting distributions sent to the GL) was not tying to the General Ledger. The gap was large enough that finance could not use the report.

I found four separate causes, fixed three of them directly in OTBI, and brought the gap down to a few dollars.

---

## How I worked

1. Compared the OTBI export with the GL detail **batch by batch**, not just by grand total.
2. Used Python (pandas) on the Excel exports to find duplicate rows, missing batches and period mismatches.
3. Changed one filter at a time, re-ran, and compared again.

## What was wrong and how I fixed it

| # | Cause | Symptom | Fix in OTBI |
|---|---|---|---|
| 1 | The fiscal calendar join matched quarter-end dates to both the normal period and the adjusting period | Some lines appeared twice (adjusting periods `ADJ-…`) | Filter: Accounting Period Name **does not contain** `ADJ` |
| 2 | The report filtered on **GL Transfer Date** | Entries for the last month that were transferred in the first days of the next month were missing | Removed the transfer date filter, added **GL Transfer Status = Yes** |
| 3 | The date filter used a date range, and the end date cut off entries with a time on the last day | Small missing amounts on the last day | Replaced the date range with **Accounting Period Name is in Jan … Aug** |
| 4 | PO Line Number came from a receipt folder that has one row per receipt | Some batches showed three copies of the same line | Took PO Number and Line Number from the **Purchase Order** folder instead |

## Result

- Before: a gap of tens of thousands of dollars.
- After: the report tied to the GL within **about $9** for the full year to date.
- The remaining few dollars sit in 10 batches where the cost side has split or partial line amounts. Fully closing those needs a SQL report through Subledger Accounting (`XLA_DISTRIBUTION_LINKS` to GL journal lines), because OTBI subject areas cannot reach that level.

## Lessons

- A report that matches "99%" can still hide two errors cancelling each other out. Always check by batch.
- For GL reconciliation, filter by **accounting period**, the same way the GL does, not by date.
- In OTBI, a column from the wrong subject-area folder can multiply rows silently.
- Save OTBI changes in the shared copy. A personal copy in My Folders does not change what other people run.

## Final filter set

```
Account                      = <balance sheet account>
Accounting Period Name       is in   Jan-YY … current period
Accounting Period Name       does not contain   ADJ
GL Transfer Status           = Yes
PO Number / Line Number      from the Purchase Order folder
```

## Tools

Oracle OTBI · Oracle Fusion Cost Management · General Ledger · Python (pandas, openpyxl) · Excel

> No client names, account numbers or amounts from the real data are included.
