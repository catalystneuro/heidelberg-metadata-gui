from . import init_app
from pathlib import Path
from threading import Timer
import webbrowser
import os


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description='Metadata editing GUI interface, with automatic metadata fetching.',
    )

    parser.add_argument(
        "--data_path",
        default='.',
        help="Path to datasets."
    )
    parser.add_argument(
        "--port",
        default='5000',
        help="Path to datasets."
    )
    parser.add_argument(
        "--dev",
        default=False,
        help="Run in development mode."
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def cmd_line_shortcut():
    run_args = parse_arguments()

    # Set ENV variables for app
    data_path = str(Path(run_args.data_path))
    os.environ['DATA_PATH'] = data_path
    os.environ['FLASK_ENV'] = 'production'

    print(f'Metadata editing GUI running on localhost:{run_args.port}')
    print(f'Data path: {data_path}')
    if run_args.dev:
        os.environ['FLASK_ENV'] = 'development'
        print('Running in development mode')

    # Initialize app
    app = init_app()

    # Open browser after 1 sec
    def open_browser():
        webbrowser.open_new(f'http://localhost:{run_args.port}/')

    Timer(1, open_browser).start()

    # Run app
    app.run(
        host='0.0.0.0',
        port=run_args.port,
        debug=run_args.dev,
        use_reloader=run_args.dev
    )
