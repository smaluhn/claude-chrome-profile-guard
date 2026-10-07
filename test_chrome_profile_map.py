#!/usr/bin/env python3
"""Self-check without a real Chrome: builds a fake Chrome folder and checks the map.
Run: python3 test_chrome_profile_map.py"""
import json, pathlib, tempfile, importlib.util, io, contextlib

spec = importlib.util.spec_from_file_location("m", pathlib.Path(__file__).with_name("chrome_profile_map.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

with tempfile.TemporaryDirectory() as d:
    base = pathlib.Path(d)
    (base / "Local State").write_text(json.dumps({"profile": {"info_cache": {
        "Default": {"name": "Personal"}, "Profile 1": {"name": "Work"}, "Profile 2": {"name": "Spare"}}}}))
    for folder, dev in (("Default", "11111111-2222-3333-4444-555555555555"), ("Profile 1", None)):
        ext = base / folder / "Local Extension Settings" / m.EXT; ext.mkdir(parents=True)
        (ext / "000003.log").write_bytes(b"\x00junk bridgeDeviceId\x22:\x22" + dev.encode() + b"\x22" if dev else b"no id yet")
    m.chrome_dir = lambda: base
    names, found = m.profiles()
    assert found["Personal"] == ("Default", "11111111-2222-3333-4444-555555555555"), found
    assert found["Work"] == ("Profile 1", None), found          # extension present, not connected
    assert "Spare" not in found                                  # no extension in that profile
    out = io.StringIO()
    with contextlib.redirect_stdout(out): m.main()
    text = out.getvalue()
    assert "deviceId 11111111-2222-3333-4444-555555555555" in text
    assert "MISSING (extension not connected in this profile)" in text
print("ok")
