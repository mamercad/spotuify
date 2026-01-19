"""Entry point for Spotuify."""

import sys


def main() -> int:
    """Run the Spotuify application."""
    from .app import SpotuifyApp

    app = SpotuifyApp()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
