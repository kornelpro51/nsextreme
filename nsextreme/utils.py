from tempfile import gettempdir
from os.path import join
import uuid


def get_request():
    """Walk up the stack, return the nearest first argument named "request"."""
    import inspect
    frame = None
    try:
        for f in inspect.stack()[2:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames[:1] == ("request",):
                return frame.f_locals["request"]
            elif code.co_varnames[:2] == ("self", "request",):
                return frame.f_locals["request"]
    finally:
        del frame


def generate_tempfilename(suffix):
    return join(gettempdir(), '-'.join(['ns', str(uuid.uuid4())]) + suffix)
