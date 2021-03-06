# 镜像相关api
from flask import Blueprint, jsonify, current_app
from common_tool import get_request_json_obj
from shell import build_java_project_image
from db.image_model import insert_image

image_blue: Blueprint = Blueprint('image_api', __name__)


@image_blue.route('/image/create', methods=['POST'])
def create_image():
    """创建镜像"""
    create_image_req = get_request_json_obj()
    # 非空参数校验
    if 'git_address' in create_image_req:
        git_address = create_image_req['git_address']
    else:
        return jsonify({'err_no': 202004281633, 'err_msg': 'param error-git_address cannot be null'})
    if 'image_name' in create_image_req:
        image_name = create_image_req['image_name']
    else:
        return jsonify({'err_no': 202004281633, 'err_msg': 'param error-image_name cannot be null'})

    image_dict = {
        'git_address': git_address,
        'git_branch': create_image_req.get('git_branch', 'master'),
        'image_name': image_name
    }

    # 创建镜像并获取镜像id
    image_id = build_java_project_image(image_dict)

    image_dict['image_id'] = image_id
    err_no, err_msg = insert_image(image_dict)

    return jsonify({'err_no': err_no, 'err_msg': err_msg})
