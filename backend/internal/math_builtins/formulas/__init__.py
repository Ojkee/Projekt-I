import importlib
import pkgutil

package = __name__

for _, modname, _ in pkgutil.iter_modules(__path__):
    importlib.import_module(f"{package}.{modname}")
