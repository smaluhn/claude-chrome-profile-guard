# Use cases

Real situations this guard is built for. Each one names what goes wrong without it and which rule prevents it (rule numbers refer to `RULES.md`).

## 1. Private and work in one browser

You keep a private Chrome profile (personal mail, bank, family) and a work profile (company mail, cloud consoles, client tools).
- **Without the guard:** Claude picks "Browser 1", which happens to be the private profile, and drafts a business reply from your personal mail account, or opens a cloud console that shows a sign-in screen.
- **With it:** the chat's topic is Work, the map points to the work profile's device ID, and the verify step (rule 3) confirms it before any tab opens.

## 2. One profile per client or project

Agencies and freelancers keep each client in its own Chrome profile, so logins, cookies and extensions never mix.
- **Without the guard:** a task for client A runs in client B's profile, where B's analytics, CMS or ad account is logged in.
- **With it:** each project's `CLAUDE.md` names its topic ("This project uses the Chrome topic Client A"), and rule 2 makes the chat select exactly that profile.

## 3. Two computers on the same Claude account

A desktop at home and a laptop for travel, both with Claude in Chrome connected.
- **Without the guard:** a chat on the laptop steers the desktop's browser at home, because that one was connected first. You see nothing happen and the desktop clicks around on its own.
- **With it:** only browsers marked `onThisComputer: true` are allowed (rule 4), and the map is written per computer and never copied (README step 5).

## 4. "You are logged out" that is not true

The agent reports that you are logged out of a service you are clearly logged into.
- **Cause:** the tab opened in a profile where you never signed in to that service, often after the extension reconnected and silently fell back to another profile.
- **With it:** a sign-in screen first triggers a re-select and one reload (rule 6), and the selection is renewed after every reconnect (rule 5).

## 5. Accounts that look identical

Two accounts of the same app, for example two business messaging or mail accounts, look the same in a browser tab. The window title proves nothing.
- **With it:** the agent works in the profile mapped to the right topic, says which account it is about to act as, and stops on any mismatch. For messaging apps, combine this with a check inside the page (for example the logged-in phone number) before typing anything.

## 6. Cloud consoles and support tickets

Single-page apps such as cloud consoles keep showing the previous ticket or project after a URL change.
- **Without the guard:** a reply meant for ticket B lands in ticket A, which is still on screen.
- **With it:** hard-reload and check the heading before writing (rule 7).

## 7. Just open a page for the user

Sometimes the agent only needs to put a page in front of you (a sign-up form, a dashboard) and you take over.
- **With it:** no extension at all, just `open -na "Google Chrome" --args --profile-directory="<folder>" <url>` with the folder from the map (rule 8). Fast, and no risk of acting in the page.

## 8. A team

Every team member installs the guard on their own computers with their own topics. Nothing is shared between machines except the rules: device IDs are personal and per computer.
