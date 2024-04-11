# contents of conftest.py
import sys
from pathlib import Path

# Assuming conftest.py is located directly inside the tests folder,
# and we want to add the src folder to sys.path
root_dir = Path(__file__).parent.parent
src_dir = root_dir

sys.path.insert(0, str(src_dir))
