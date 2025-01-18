from flask import Blueprint, Response, request
from src.helpers.pdfTodxf.example1 import pymain

dxfViewer = Blueprint("dxf-viewer", __name__)

@dxfViewer.route("", methods=["GET"])
def get_file_to_view():
    # return Response(
    #     json.dumps({"count": count}),
    #     mimetype="application/json",
    #     status=200,
    # )
    print("1>>>")
    pymain()
    print("2>>>")
    return "Hello Markos"