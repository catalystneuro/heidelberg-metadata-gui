import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from datetime import datetime
from dash_cool_components import KeyedFileBrowser
import os
from pathlib import Path
import dash


def make_file_picker(id_suffix):
    filepicker = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Form(
                                [
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Choose NWB file:"),
                                            dbc.Input(
                                                type="text", id='nwb_' + id_suffix,
                                                placeholder="Path/to/local.nwb"
                                            ),
                                        ],
                                    ),
                                    dbc.Button('Submit', id='submit_nwb_' + id_suffix),
                                ],
                            )
                        ],
                        className='col-md-4'
                    ),
                ],
                style={'align-items': 'center', 'justify-content': 'center', 'text-align': 'center'}
            )
        ]
    )

    return filepicker


def make_upload_file(id_suffix):
    uploader = dbc.Container([
        dbc.Row([
            dbc.Col([
                dcc.Upload(
                    id=id_suffix,
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."],
                    ),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    multiple=False,
                ),
            ], className='col-md-4')],
            style={'justify-content': 'center'}
        )
    ])

    return uploader


def make_json_file_buttons(id_suffix):
    """Makes JSON load, save and view buttons"""
    json_buttons = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    children=[
                        dcc.Upload(
                            children=dbc.Button('Load JSON', color='dark'),
                            id='load_json_' + id_suffix
                        )
                    ],
                    width={'size': '30px'},
                    style={'margin-left': '10px'}
                ),
                dbc.Col(
                    children=[dbc.Button('Save JSON', color='dark', id='save_json_' + id_suffix)],
                    width={'size': '30px'},
                    style={'margin-left': '10px'}
                ),
                dbc.Col(
                    children=[dbc.Button('Show JSON', color='dark', id='show_json_' + id_suffix)],
                    width={'size': '30px'},
                    style={'margin-left': '10px'}
                ),
            ],
            justify="start",
        ),
    ])

    return json_buttons


def make_filebrowser_modal(parent_app, modal_id="modal-filebrowser", display=None):
    """File Explorer Example"""
    explorer = FileBrowserComponent(
        parent_app=parent_app,
        id_suffix=modal_id,
        display=display
    )

    modal = dbc.Container(
        dbc.Row(
            [
                dbc.Modal(
                    [
                        dbc.ModalBody(explorer),
                        dbc.ModalFooter(
                            dbc.Button("Close", id=modal_id + "-close", color='dark', className="ml-auto")
                        ),
                    ],
                    id=modal_id,
                    size="xl"
                ),
            ], style={'justify-content': 'center'}
        )
    )
    return modal


class FileBrowserComponent(html.Div):
    def __init__(self, parent_app, id_suffix, root_dir=None, display=None):
        super().__init__([])
        self.parent_app = parent_app
        self.id_suffix = id_suffix

        if root_dir is None:
            self.root_dir = parent_app.server.config['DATA_PATH']
        else:
            self.root_dir = root_dir

        self.make_dict_from_dir(display=display)

        # Button part
        input_group = dbc.InputGroup([
            dbc.InputGroupAddon(
                dbc.Button('Choose file', color='dark', id="button_file_browser_" + id_suffix),
                addon_type="prepend",
            ),
            dbc.Input(id="chosen-filebrowser-" + id_suffix, placeholder=""),
            dbc.InputGroupAddon(
                dbc.Button('Submit', color='dark', id='submit-filebrowser-' + id_suffix),
                addon_type='prepend',
            )
        ])

        # Collapsible part - file browser
        self.container = self.make_file_browser()

        self.children = [
            dbc.Container([
                input_group,
                dbc.Collapse(
                    dbc.Card(dbc.CardBody(
                        self.container
                    )),
                    id="collapse_file_browser_" + id_suffix,
                ),
            ])
        ]

        @self.parent_app.callback(
            [
                Output("collapse_file_browser_" + id_suffix, "is_open"),
                Output("chosen-filebrowser-" + id_suffix, 'value')
            ],
            [
                Input("button_file_browser_" + id_suffix, "n_clicks"),
                Input('keyedfilebrowser-' + id_suffix, 'selectedPath')
            ],
            [State("collapse_file_browser_" + id_suffix, "is_open")],
        )
        def toggle_collapse(n, path, is_open):

            ctx = dash.callback_context
            trigger_source = ctx.triggered[0]['prop_id'].split('.')[0]

            if path is None:
                path = ''
            if trigger_source == f'button_file_browser_{self.id_suffix}':
                return not is_open, path
            return is_open, path

    def make_file_browser(self):
        dir_schema = self.paths_tree
        explorer = dbc.Container(
            dbc.Row(
                dbc.Col(
                    KeyedFileBrowser(
                        id='keyedfilebrowser-' + self.id_suffix,
                        files=dir_schema
                    ),
                ),
                style={'justify-content': 'left'}
            ),
            fluid=True
        )

        return explorer

    def make_dict_from_dir(self, display):

        keys_list = []
        paths_list = []
        for path, dirs, files in os.walk(self.root_dir):
            curr_path = path + '/'
            if curr_path.startswith('/'):
                curr_path = curr_path[1:]
            if curr_path not in paths_list:
                paths_list.append(curr_path)
            if len(files) > 0 and display != 'directory':
                for file in files:
                    aux_dict = {}
                    file_path = Path(path) / file

                    mod_datetime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    delta = datetime.utcnow() - mod_datetime
                    size = os.path.getsize(file_path)

                    aux_dict['key'] = str(file_path).replace("\\", "/")
                    aux_dict['modified'] = delta.days
                    aux_dict['size'] = size

                    keys_list.append(aux_dict)

        splitter = Path(self.root_dir).parent.name
        for path in paths_list:
            aux_dict = dict()
            aux_dict['key'] = str(path).replace("\\", '/')
            aux_dict['modified'] = None
            aux_dict['size'] = 0
            keys_list.append(aux_dict)

        # Simplify file explorer to start on the base path defined on config
        for e in keys_list:
            splitted = e['key'].split(splitter, maxsplit=1)[1]
            if splitted.startswith('/'):
                splitted = splitted[1:]
                e['key'] = splitted

        self.paths_tree = keys_list
