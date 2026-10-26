# EP14 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep14_full", "/home/claude/ep14/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "claim", "promise", "rehook", "numbers", "deport"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["A hundred billion dollars that never existed.", "And still"])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
