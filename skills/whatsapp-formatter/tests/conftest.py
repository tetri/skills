import sys
from pathlib import Path

# Add parent directory to path so we can import formatter
sys.path.insert(0, str(Path(__file__).parent.parent))

# Ignore __init__.py in parent directory
collect_ignore = ["../__init__.py"]