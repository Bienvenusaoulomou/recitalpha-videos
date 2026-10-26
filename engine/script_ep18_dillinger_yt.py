import importlib.util as _u
_s = _u.spec_from_file_location("ep18_full", "/home/claude/ep18/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "jail", "rehook", "gun", "guards", "car", "feds"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["All because", ])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
