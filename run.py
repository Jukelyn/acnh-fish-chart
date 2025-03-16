"""
This script runs the application defined in the `app` module from the `src`
package.

The script checks if it is being run as the main module and, if so, starts the
application server.

Modules:
    src.app: The application instance to be run.

Usage:
    Run this script directly to start the application server.
"""
from src import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
