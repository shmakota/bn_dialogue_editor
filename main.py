"""Entry point script"""

import sys
import traceback

try:
    from src.main import main
    main()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)

