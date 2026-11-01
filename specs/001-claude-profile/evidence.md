# Evidence

- Repo: safarovmurod/claude-setting. Автонасби `bootstrap.ps1` репои публик мехоҳад; visibility-ро худи соҳиб иваз мекунад.
- 7 lifecycle/security tests pass locally and from a clean clone.
- Windows and Linux CI passed for commit 8a4c154: https://github.com/safarovmurod/claude-setting/actions/runs/41299091099 .
- Profile bytes and manifest hashes preserved across clones.
- PowerShell entrypoint parses successfully.
- No personal credentials, sessions, databases or original Claude directories were exported.
- Current Windows user profile was not changed. Claude CLI was absent from PATH; authenticated runtime, skill discovery and mobile behavior remain unverified.
- Қоидаҳои кӯҳнаи профил (муроҷиати «шеф», React + TypeScript) бардошта шуданд; ҷояшон қоидаҳои mentor-и frontend (ака Мансур, JSX/TSX, тартиби интихоби китобхонаи дизайн) гузошта шуд. manifest hash-ҳо аз нав ҳисоб шуданд.
- `bootstrap.ps1` дар ин муҳит иҷро нашуд: PowerShell нест. Он дар Windows санҷида нашудааст.
