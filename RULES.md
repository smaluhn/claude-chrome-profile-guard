## Claude in Chrome: only this computer, one profile per topic

Paste this section into your global `CLAUDE.md` (for example `~/.claude/CLAUDE.md`).

1. **Never use a hard-coded device ID or a browser name like "Browser 1".** Those names change. Only the deviceId counts, and the mapping lives in `~/.claude/chrome-profile` (written by `chrome_profile_map.py --write`, local to this computer, never synced).
2. **Before the first browser action** in a chat: read `~/.claude/chrome-profile`, take the line for the chat's topic, call `select_browser` with that deviceId.
3. **Selecting is not enough, verify it.** Call `list_connected_browsers`: that deviceId must show `"inUse": true` and `"onThisComputer": true`. If not, select again and check again. Only then open a tab.
4. **Only profiles of this computer.** An entry without `onThisComputer: true` runs on another machine and is never selected, even if it is connected. If a chat ever controls another computer's browser: stop and tell the user.
5. **The selection does not stick.** After every "Claude in Chrome is not connected", after every empty `tabs_context_mcp` and at the start of each new block of work: select again before opening the next tab.
6. **A sign-in screen first means wrong profile.** Re-select and reload once before telling the user they are logged out.
7. **Single-page apps** (cloud consoles, support tickets) can keep showing the previous page after a URL change: hard-reload and check the heading before writing anything.
8. **Just opening a page** (no reading, no clicking) does not need the extension: `open -na "Google Chrome" --args --profile-directory="<folder from the map>" <url>` (macOS).
9. **Missing line:** if the map says MISSING, ask the user to open that profile, click the Claude icon and Connect, then rerun the script. Never fall back to another profile.
