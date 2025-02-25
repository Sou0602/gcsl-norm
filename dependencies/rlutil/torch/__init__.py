import rlutil.torch.nn
from rlutil.torch.pytorch_util import set_gpu, default_device, to_numpy
from types import ModuleType
import torch.optim as optim
import pdb
def _replace_funcs(global_dict):
    import torch as th
    class DeviceWrapped(object): 
        def __init__(self, fn):
            self.fn = fn

        def __call__(self, *args, device=None, **kwargs):
            if device is None:
                device = default_device()
            return self.fn(*args, device=device, **kwargs)

        def __repr__(self):
            return '<device-wrapped function %s>' % self.fn.__name__

    for _key in dir(th):
        if _key in ['ScriptClassFunction']:
            global_dict[_key] = _value
        _value = getattr(th, _key) 
        # hacky way of determining if device is an argument
        # (cannot use inspect because torch functions are builtins)
        if _value.__doc__ and 'device (:class:`torch.device`, optional):' in _value.__doc__:
            print(_key)
            global_dict[_key] = DeviceWrapped(_value)
        elif isinstance(_value, ModuleType):
            pass
        else:
            global_dict[_key] = _value

_replace_funcs(globals())
pdb.set_trace()