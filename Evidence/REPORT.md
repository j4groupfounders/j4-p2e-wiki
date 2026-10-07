# p2-15-wiki — GREEN

Django 5.2.12 → 6.0.4. Source django-wiki/django-wiki @ 04ebb5b51a41ef1fca554d74aa1e5fd8840b8537.
Preregistration: https://github.com/j4groupfounders/j4-upgrades-harness/commit/6cf87daccde1910714fe47fd0c9b552f9302fae1
Baseline: b26f325a715c4eae9a039250b01df7cb1d3c13ef; upgraded: d01bb283e420c2ca547c5cab05fe83d523de9e1f.

- Project tests: **291 passed, 3 pre-existing skips** before and after; exact collected IDs/skips match: True. No removed/newly skipped tests. Helpdesk subtests additionally retained by original assertions.
- Boot/HTTP: five fixed real-server GET snapshots match: True; model fixture snapshots match: True. No unexplained drift or framework behavior exception.
- Independent seeded faults: project-only **2/5**, combined **5/5**. One fresh-checkout matrix job per mutation, no build state shared. Combined miss-rate halving: True.
- **6 workflow runs**, **6.08 actual job-minutes**, including screening failures and all five matrix jobs. Cap 12. Standard public Ubuntu runners, $0 paid API/service calls. Session token cost is not exposed/measured.
- Zero human app/test edits. Permanent agent app/test logic edits: zero (only the preregistered temporary fault injections). Framework upgrade only changes two pinned dependency files; exact diff preserved as upgrade.patch.

## Repairs and limits
Third screening run normalized exactly the random signup honeypot CSS identifier and JS function. Fourth screening replay (if present) confirmed the normalized snapshot. No app/test logic changed.
Harness baseline HTTP boot settings use disposable SQLite, DEBUG=False, local-only allowed hosts and in-memory email. Original app/test source untouched. Original upstream workflows replaced on pilot branches with bounded verification; no upstream modifications/contact.
These are three new Django applications, not three new stacks. Current upstream already advertises compatible framework ranges, so the result supports controlled dependency-upgrade compatibility, not arbitrary legacy migration success.
HTTP remains empty-DB unauthenticated; model probes use fixed unsaved objects. Todo's old due-date fixture is not full clock freezing. Wiki's 3 opt-in browser tests and Helpdesk's 2 upstream skipped attachment tests remain skipped. No authenticated frozen HTTP replay, full route/line coverage, external integrations or production certification.
Seed targets are preregistered measured business/permission surfaces; not an unbiased whole-app mutation score. The extra model checks catch faults beyond the project's suite where applicable.

## Evidence runs
- [37620133864](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37620133864) — j4/p2e-baseline, success, 0.60 job-min
- [37620448986](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37620448986) — j4/p2e-baseline, failure, 0.47 job-min
- [37620677894](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37620677894) — j4/p2e-baseline, success, 0.70 job-min
- [37620939520](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37620939520) — j4/p2e-baseline, success, 0.62 job-min
- [37621137029](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37621137029) — j4/p2e-upgrade, success, 0.65 job-min
- [37621370989](https://github.com/j4groupfounders/j4-p2e-wiki/actions/runs/37621370989) — j4/p2e-seeds, success, 3.05 job-min

## Seed detections

```json
[
  {
    "mutation": 0,
    "tests": 294,
    "skipped": 3,
    "project_detected": false,
    "harness_detected": true,
    "combined": true
  },
  {
    "mutation": 1,
    "tests": 294,
    "skipped": 3,
    "project_detected": true,
    "harness_detected": true,
    "combined": true
  },
  {
    "mutation": 2,
    "tests": 294,
    "skipped": 3,
    "project_detected": true,
    "harness_detected": true,
    "combined": true
  },
  {
    "mutation": 3,
    "tests": 294,
    "skipped": 3,
    "project_detected": false,
    "harness_detected": true,
    "combined": true
  },
  {
    "mutation": 4,
    "tests": 294,
    "skipped": 3,
    "project_detected": false,
    "harness_detected": true,
    "combined": true
  }
]
```
