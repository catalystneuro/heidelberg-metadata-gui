from heidelberg_metadata_gui import init_app
from pathlib import Path
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
        "--debug",
        default=False,
        help="Set debug."
    )
    parser.add_argument(
        "--port",
        default='5000',
        help="Path to datasets."
    )

    # Parse arguments
    args = parser.parse_args()

    return args


def cmd_line_shortcut():
    run_args = parse_arguments()

    # Set ENV variables for app
    data_path = str(Path(run_args.data_path).resolve())
    os.environ['DATA_PATH'] = data_path

    print(f'Metadata editing GUI running on localhost:{run_args.port}')
    print(f'Debug mode: {run_args.debug}')
    print(f'Data path: {data_path}')

    app = init_app()
    app.run(
        host='0.0.0.0',
        port=run_args.port,
        debug=run_args.debug,
        use_reloader=run_args.debug
    )
