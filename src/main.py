"""Main entry point for the dialogue editor"""

import sys
import traceback


def main():
    """Run the dialogue editor"""
    try:
        from .ui.main_window import MainWindow
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

