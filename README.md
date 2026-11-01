# claude-setting
Шеф, ин бастаи ҷудо фақат барои **Claude Code** аст. Claude Desktop/Cowork ва ChatGPT personalization-ро тағйир намедиҳад.

## Насб
Ба Claude Code ссылкаи репоро дода бигӯ:
> Ин репоро clone кун, CLAUDE.md ва README-ро хон. `python setup.py install` ва `python setup.py doctor`-ро иҷро кун. Баъд дар Claude Code бор шудани instructions ва skills-ро санҷ. Файлҳои мавҷуда ва authentication-ро нигоҳ дор.

```powershell
git clone https://github.com/safarovmurod/claude-setting.git
cd claude-setting
.\Install.ps1
.\Install.ps1 doctor
```
Python 3.11+ ва Claude Code-и расмӣ лозиманд. Ин installer худи барнома ё login-ро насб намекунад. [Насби расмӣ](https://code.claude.com/docs/en/setup). Ҳисоби GitHub бояд ба репои private дастрасӣ дошта бошад.

## Ҷойҳо
- `~/.claude/CLAUDE.md`: import-и дастурҳои шахсӣ; матни пешина нигоҳ дошта мешавад.
- `~/.claude/claude-setting/instructions.md`: гапзанӣ ва coding preferences.
- `~/.claude/skills`: `/frontend-work`, `/project-check`, `/setup-check`.
- `~/.claude/claude-setting/receipt.json` ва `backups`: ownership ва баргардондан.

`python setup.py uninstall` танҳо файлҳои тағйирнадодаи худро бармегардонад. Backup мемонад. Тағйири баъдии худат conflict ҳисоб мешавад ва пӯшонда намешавад.

## Чӣ дохил нашуд
Codex config.toml, AGENTS runtime paths, Codex queue, watcher, scheduled task, 35 скилли омехта ва binary-ҳои нодаркор нусха нашуданд. ~/.claude/settings.json-и мавҷуда ёфт нашуд: setting-и тахминӣ сохта намешавад; permissions, hooks, model, plugins ва account preferences нигоҳ дошта мешаванд. Плагинҳо автоматӣ насб намешаванд.

AUTORUN-и Codex дар Claude кор намекунад. Дар ин баста командаи сохтаи /autorun ё ваъдаи идомаи баъди quota нест. Барои сессия ва лимит аз командаҳои версияи ҷории Claude истифода бар. Мобил/Remote ва барқароршавии воқеии лимит дар ин баста санҷида нашудаанд.

## Санҷиш
`python -m unittest discover -s tests -v`. Doctor танҳо файл ва мавҷудияти CLI-ро месанҷад; кори authenticated ё discovery-и воқеиро исбот намекунад. Ҳолати насби ин ПК: Claude CLI дар PATH ёфт нашуд; профил ба ҳисоби шахсӣ татбиқ нашудааст. Санҷишҳои lifecycle дар home-и муваққатӣ иҷро мешаванд.

Манбаъҳо: [CLAUDE.md](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills), [settings](https://code.claude.com/docs/en/settings). Spec Kit бо pin-и 7370e592f3cd9c06e5b698983957e227c75b30e2 оғоз шуд; .agents-и Codex танҳо дар папкаи таҳия мемонад ва ба репо намеравад; .specify ҳуҷҷатгузории таҳия аст, installer онро насб намекунад.
