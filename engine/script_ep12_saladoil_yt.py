# EP12 YouTube cut (~45 s, seamless loop back into the hook)
import importlib.util as _u
_s = _u.spec_from_file_location("ep12_full", "/home/claude/ep12/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "receipts", "rehook", "trick", "numbers", "crash"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["Tanks of water, worth a fortune on paper.", "Because"])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
