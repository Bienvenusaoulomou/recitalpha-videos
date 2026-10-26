import importlib.util as _u
_s = _u.spec_from_file_location("ep20_full", "/home/claude/ep20/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "cargo", "attack", "rehook", "garage", "money", "closed", "twist"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["To this day, the full story is a mystery. Because", ])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
