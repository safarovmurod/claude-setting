# claude-setting
Шеф, ин бастаи ҷудо фақат барои **Claude Code** аст. Claude Desktop/Cowork ва ChatGPT personalization-ро тағйир намедиҳад.

## Насб (автоматӣ, як команда)
Дар PowerShell:

```powershell
irm https://raw.githubusercontent.com/safarovmurod/claude-setting/main/bootstrap.ps1 | iex
```
`bootstrap.ps1` худаш ZIP-и репоро ба папкаи муваққатӣ мекашад, боз мекунад, `setup.py install`-ро иҷро мекунад, баъд `doctor`-ро нишон медиҳад ва папкаи муваққатиро тоза мекунад. Clone лозим нест. Ин роҳ репои **публик** мехоҳад; ин репо публик аст ва санҷида шуд. Матнҳои дохили `bootstrap.ps1` танҳо лотинӣ ҳастанд: UTF-8 BOM роҳи `irm | iex`-ро мешиканад, вале бе BOM Windows PowerShell 5.1 матни кириллиро вайрон мехонад.

## Насб (clone, варианти дуюм)
```powershell
git clone https://github.com/safarovmurod/claude-setting.git
Set-Location claude-setting
.\bootstrap.ps1
.\bootstrap.ps1 -Action doctor
```
Дар clone `bootstrap.ps1` чизе download намекунад — ҳамон папкаи назди худашро насб мекунад ва баъд `doctor` мегӯяд. `.\Install.ps1` ва `.\Install.ps1 doctor` ҳам кор мекунанд.

Python 3.11+ ва Claude Code-и расмӣ лозиманд. Ин installer худи барнома ё login-ро насб намекунад. [Насби расмӣ](https://code.claude.com/docs/en/setup).

## Қоида дар кадом ҷо кор мекунад

| Ҷой | Куҷо кор мекунад |
|---|---|
| **Personalization** дар claude.ai → Settings | **ҳама ҷо**: облако, локалӣ, desktop, мобил, ҳар репо |
| `~/.claude/CLAUDE.md` (аз `bootstrap.ps1`) | танҳо дар Claude Code-и ҳамон ПК, вале дар ҳама проектҳо |
| `CLAUDE.md`-и дохили репо | танҳо дар ҳамон як репо |

Сессияи облакӣ (claude.ai/code) `~/.claude`-и ПК-ро **намебинад** — он дар контейнери дигар кор мекунад. Пас барои он ки қоидаҳо дар облако ва дар ҳар репо кор кунанд, **Personalization ҳатмист**.

Матни тайёр барои Personalization дар [`personalization.md`](personalization.md) аст: copy кун, ба claude.ai гузор, баъд **чати нав** кушо (чати кӯҳна матни кӯҳнаро нигоҳ медорад).

## Ҷойҳо
- `~/.claude/CLAUDE.md`: import-и дастурҳои шахсӣ; матни пешина нигоҳ дошта мешавад.
- `~/.claude/claude-setting/instructions.md`: гапзанӣ ва coding preferences — муроҷиат «шеф», mentor-и frontend, проекти нав React + TypeScript (TSX) + Vite (проекти JavaScript бо ҳамон JSX), формати хатогӣ ва тартиби дарс. Дизайн: аввал `package.json` санҷида мешавад — Tailwind ҳаст → HTML + Tailwind, MUI ҳаст → MUI, ҳеҷ чиз нест → пурсида мешавад ва баъди интихоб худаш насб мекунад.
- `~/.claude/skills`: `/frontend-work`, `/project-check`, `/setup-check`.
- `~/.claude/claude-setting/receipt.json` ва `backups`: ownership ва баргардондан.

`python setup.py uninstall` танҳо файлҳои тағйирнадодаи худро бармегардонад. Backup мемонад. Тағйири баъдии худат conflict ҳисоб мешавад ва пӯшонда намешавад.

## Чӣ дохил нашуд
Codex config.toml, AGENTS runtime paths, Codex queue, watcher, scheduled task, 35 скилли омехта ва binary-ҳои нодаркор нусха нашуданд. ~/.claude/settings.json-и мавҷуда ёфт нашуд: setting-и тахминӣ сохта намешавад; permissions, hooks, model, plugins ва account preferences нигоҳ дошта мешаванд. Плагинҳо автоматӣ насб намешаванд.

AUTORUN-и Codex дар Claude кор намекунад. Дар ин баста командаи сохтаи /autorun ё ваъдаи идомаи баъди quota нест. Барои сессия ва лимит аз командаҳои версияи ҷории Claude истифода бар. Мобил/Remote ва барқароршавии воқеии лимит дар ин баста санҷида нашудаанд.

## Санҷиш
`python -m unittest discover -s tests -v`. Doctor танҳо файл ва мавҷудияти CLI-ро месанҷад; кори authenticated ё discovery-и воқеиро исбот намекунад. Ҳолати насби ин ПК (2026-11-03): Claude CLI 2.1.316 дар PATH ёфт шуд, профил насб шуд, `doctor` → `files_ok: true`. Personalization-и claude.ai дастӣ монд — онро installer намегузорад. Санҷишҳои lifecycle дар home-и муваққатӣ иҷро мешаванд.

Манбаъҳо: [CLAUDE.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings). Spec Kit бо pin-и 7370e592f3cd9c06e5b698983957e227c75b30e2 оғоз шуд; .agents-и Codex танҳо дар папкаи таҳия мемонад ва ба репо намеравад; .specify ҳуҷҷатгузории таҳия аст, installer онро насб намекунад.
