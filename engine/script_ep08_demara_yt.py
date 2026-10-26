# EP08 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep08_full", "/home/claude/ep08/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "careers", "rehook", "navy", "wounded", "bullet", "exposed"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["No charges. He just walked away.", "And the world learned that"])]
REHOOK = _m.REHOOK
LOOPEND = ("NO CHARGES.", "HE WALKED AWAY.", "")
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
