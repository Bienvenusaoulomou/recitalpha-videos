# EP15 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep15_full", "/home/claude/ep15/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "king", "deal", "rehook", "bonds", "audit"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["An empire of matches, built on nothing.", "Because"])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
