#!/usr/bin/env python3
"""Claude in Chrome: map each topic to ONE Chrome profile on THIS computer and its extension device ID.

Why: the Claude in Chrome extension registers every Chrome profile on every computer that is signed in
to the same Claude account. Without a map, an agent picks "Browser 1" or "Browser 2", which are unstable
names, and ends up in the wrong profile or even on another computer.

What it does: reads the Chrome profiles of this computer, finds the device ID the Claude extension stored
in each profile, and writes ~/.claude/chrome-profile, e.g.
    Work  ->  profile 'Work' (Profile 3)  ->  deviceId 1a2b...
Nothing leaves the computer; the file is meant to stay local (do not sync it between machines).

Usage:
    python3 chrome_profile_map.py            # print the map
    python3 chrome_profile_map.py --write    # also write ~/.claude/chrome-profile
Edit TOPICS below to match your own profile names.
"""
import json, os, pathlib, platform, re, sys

TOPICS = [  # (topic, Chrome profile names that belong to it; the first one found wins)
    ("Private", ["Personal", "Private"]),
    ("Work (default for everything else)", ["Work", "Business"]),
]
EXT = "fcoeoabgfenejglbffodgkkbkcdhcgfn"   # Claude in Chrome extension ID


def chrome_dir():
    home = pathlib.Path.home()
    if platform.system() == "Darwin": return home / "Library/Application Support/Google/Chrome"
    if platform.system() == "Windows": return pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data"
    return home / ".config/google-chrome"


def profiles():
    base = chrome_dir()
    if not (base / "Local State").exists(): sys.exit(f"No Chrome data found in {base}")
    names = {k: v.get("name") for k, v in json.load(open(base / "Local State"))["profile"]["info_cache"].items()}
    found = {}
    for folder, name in names.items():
        p = base / folder / "Local Extension Settings" / EXT
        if not p.is_dir(): continue
        raw = b"".join(f.read_bytes() for f in sorted(p.iterdir()) if f.is_file())
        m = re.search(rb"bridgeDeviceId[^0-9a-f]{0,20}([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})", raw)
        found[name] = (folder, m.group(1).decode() if m else None)
    return names, found


def main():
    names, found = profiles()
    lines = [f"# Chrome profiles on THIS computer: {platform.node()}",
             "# Rule: a chat uses one profile of THIS computer only, never a device ID from another computer.",
             "# MISSING: open that profile, click the Claude icon, Connect, then run this script again.", ""]
    for topic, candidates in TOPICS:
        hit = next(((c, *found[c]) for c in candidates if c in found), None)
        if hit and hit[2]:
            lines.append(f"{topic}  ->  profile {hit[0]!r} ({hit[1]})  ->  deviceId {hit[2]}")
        else:
            exists = any(n in candidates for n in names.values())
            lines.append(f"{topic}  ->  profile {candidates[0]!r}  ->  MISSING ({'extension not connected in this profile' if exists else 'no such profile on this computer'})")
    text = "\n".join(lines) + "\n"
    print(text)
    if "--write" in sys.argv:
        out = pathlib.Path.home() / ".claude/chrome-profile"
        out.parent.mkdir(exist_ok=True); out.write_text(text)
        print(f"written to {out}")


if __name__ == "__main__":
    main()
