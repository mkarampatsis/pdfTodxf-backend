from flask import Flask

from src.blueprints.dxf_viewer import dxfViewer

app = Flask(__name__)

app.register_blueprint(dxfViewer, url_prefix="/dxf-viewer")
# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name