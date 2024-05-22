import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
print(root_dir)
src_dir = root_dir

sys.path.insert(0, str(src_dir))
