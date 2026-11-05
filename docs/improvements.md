# Portfolio Engineering Improvements

### 2026-11-05 07:16 UTC — ChatGPT Portfolio Iteration
- Run ID: 20261105T071645Z-econ-8f2c
- Repo / Base SHA: 1998x-stack/economics-principles-tutorial / 47890d561c27130f3807561a336c9fbcc665ae71
- Historical context: docs/improvements.md returned GitHub 404 before any modification; zero existing PRs. README documents direct local index.html use, but existing fetch('courses.json') contradicts that. Six recent commits reviewed; previous index grid repair preserved.
- Product problem & expected user value: A learner opening the tutorial from disk may see no course cards because file:// JSON fetch is restricted in common browsers. Offline first-use should show all 28 chapters.
- Engineering diagnosis & evidence: index.html inline IIFE fetches sibling courses.json and displays error on rejection. Unvalidated course.file was assigned to href; error strings were interpolated into innerHTML.
- Options & decision: (1) offline catalog P1 score 16 (benefit 5 + correctness 4 + evidence 5 + testability 5 - cost 2 - risk 1); (2) chapter search P2 score 9; (3) mobile navigation P2 score 7. Choose (1) for reproducible first-use failure.
- Changes: index.html now loads local generated courses-data.js synchronously, validates chapter link filenames and uses textContent for errors/footer; generator and Node regression suite added; README updated. courses.json remains canonical.
- Validation: A: actual GitHub branch JS executed in V8 DOM fixture, 28 cards, first/last links, invalid href rejection and missing-data error observed. A: nine V8/static data consistency assertions passed. D: Node suite and Python --check not run on a full checkout; real Chromium file:// E2E not run. These remain review gates.
- Security & regression review: No secrets, workflow, license, deployment or permission changes; relative links restricted to NN.html. No external dependencies. Generated file must be refreshed when JSON changes.
- Risk & rollback: Browser compatibility not yet proven in Chromium; revert this PR to restore original HTTP-only fetch behavior if needed.
- Follow-up: Run real Chromium file:// and HTTP regression, plus node --test tests/offline-catalog.test.cjs and python3 scripts/build_course_data.py --check.
- Commit: b252d2ab749f277d30bad943a4cd570cddbe7e52 (initial code and history commit)
- PR: https://github.com/1998x-stack/economics-principles-tutorial/pull/1
