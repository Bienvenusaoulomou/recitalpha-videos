import importlib.util as _u
_s = _u.spec_from_file_location("ep17_full", "/home/claude/ep17/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "rule", "rehook", "hunter", "call", "locate", "end"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["Brought down by a phone call. Because", ])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
