import importlib.util as _u
_s = _u.spec_from_file_location("ep19_full", "/home/claude/ep19/script.py"); _m = _u.module_from_spec(_s); _s.loader.exec_module(_m)
_keep = ["hook", "pitch", "papers", "rehook", "tolls", "more", "caught"]
SCENES = [x for x in _m.SCENES if x[0] in _keep] + [("loopend", ["If you believe that, I have a bridge to sell you. Because", ])]
REHOOK = _m.REHOOK
CAPTION_OVERRIDES = _m.CAPTION_OVERRIDES
