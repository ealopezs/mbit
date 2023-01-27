from flask import Blueprint, request, make_response
from . import controller

bp = Blueprint('images', __name__, url_prefix='/')

#1. POST
@bp.route("/image", methods=['POST'])
def post_image():
    min_confidence = int(request.args.get("min_confidence", 8))

    base64_image = request.json["data"]
    
    tags = controller.tags_image(base64_image, min_confidence)
    
    return tags

#2. GET
@bp.get("/tags")
def get_tags():
    mindate = str(request.args.get("min_date", ''))
    maxdate = str(request.args.get("max_date", ''))
    
    response = controller.get_tags_db(mindate, maxdate)

    return response


