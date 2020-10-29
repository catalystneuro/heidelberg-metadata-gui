from heideilberg_metadata_gui import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
