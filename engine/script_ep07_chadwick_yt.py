# EP07 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep07_full", "/home/claude/ep07/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "drop", "secret", "rehook", "banks", "loans", "carnegie"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["She died in prison.", "And yet,"])]
REHOOK = _m.REHOOK
LOOPEND = ("SHE DIED IN PRISON.", "AND YET...", "")
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
