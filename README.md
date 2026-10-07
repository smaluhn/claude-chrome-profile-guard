# Claude in Chrome profile guard

**What it solves:** the Claude in Chrome extension shows up once per Chrome profile and per computer signed in to the same Claude account. An agent then sees "Browser 1, Browser 2, Browser 3 ..." and easily picks the wrong one: the private profile instead of the work one, a profile that is logged out, or even the browser on your other laptop. Pages then show sign-in screens, or worse, actions happen in the wrong account.

**How it works:** one topic per Chrome profile (for example Private, Work). A small script reads, on each computer, which device ID the extension has in which profile and writes that map to `~/.claude/chrome-profile`. Rules in your `CLAUDE.md` tell Claude to always select by that device ID, verify the selection, and never use a browser from another computer.

## What is in here

| File | What it is |
|---|---|
| `chrome_profile_map.py` | the script: reads this computer's Chrome profiles, writes `~/.claude/chrome-profile` |
| `RULES.md` | the rules to paste into your global `CLAUDE.md` |
| `USE-CASES.md` | eight real situations and which rule prevents each mistake |
| `examples/settings.json` | optional hook that shows the map at the start of every session |
| `examples/project-CLAUDE.md` | the two lines a project adds to name its Chrome topic |
| `test_chrome_profile_map.py` | self-check with a fake Chrome folder, no browser needed |

## Install (10 minutes, per computer)

1. **Create one Chrome profile per topic** (Chrome menu, profile icon, Add). In each profile install Claude in Chrome, click its icon and **Connect**.
2. **Copy `chrome_profile_map.py`** somewhere, open it and edit `TOPICS` to your profile names. Then run:
   ```bash
   python3 chrome_profile_map.py --write
   ```
   Check the output: every topic needs a deviceId. MISSING means that profile is not connected yet (step 1).
3. **Add the rules:** paste `RULES.md` into your global `CLAUDE.md`. In each project's `CLAUDE.md` (or the first message of a chat) name the topic, e.g. "This project uses the Chrome topic Work".
4. **Optional, show the map in every session:** merge `examples/settings.json` into `~/.claude/settings.json` (a SessionStart hook that prints the map).
5. **Rerun the script** after you add a profile, reinstall the extension or set up a new computer. Never copy the map between computers: device IDs are different on each.

## Test it

Ask Claude in a new chat: "Use the Chrome topic Work and open example.com". It should read the map, select the device ID, show you that `list_connected_browsers` reports `inUse: true` and `onThisComputer: true` for it, and only then open the page in the right window.

Self-check of the script, no browser needed: `python3 test_chrome_profile_map.py` prints `ok`.

## Notes

- Works on macOS out of the box; Windows and Linux paths are in the script but less tested.
- The script only reads local Chrome files and writes one text file. It sends nothing anywhere.
- Learned the hard way: tabs landing in a logged-out profile day after day, a chat steering the browser of another computer, and an action in the wrong account. The verify step (rule 3) is the one that fixed it.
- License: MIT (see `LICENSE`).
