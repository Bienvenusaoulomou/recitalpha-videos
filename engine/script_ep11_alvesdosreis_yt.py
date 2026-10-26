# EP11 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep11_full", "/home/claude/ep11/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "contract", "printer", "rehook", "notes", "caught"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["Twenty years in prison, all from one forged contract.", "Because"])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
