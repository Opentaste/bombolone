# -*- coding: utf-8 -*-
"""
api.rank.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Blueprint, g, request

# Imports inside Bombolone
import bombolone.core.rank
from bombolone.core.utils import jsonify, set_message
from bombolone.decorators import authentication, check_rank, get_hash

api_rank = Blueprint('api_rank', __name__)

@api_rank.route('/api/1.0/rank/show.json')
@authentication
@get_hash('rank')
def show():
    """ """
    rank_id = request.args.get("rank-id", None)
    data = core.rank.show(rank_id=rank_id)
    data = set_message(data)
    return jsonify(data)

@api_rank.route('/api/1.0/rank/create.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('rank')
def create():
    """ """
    name = request.json.get("name", None)
    rank = request.json.get("rank", None)
    data = core.rank.create(name=name, rank=rank)
    data = set_message(data)
    return jsonify(data)

@api_rank.route('/api/1.0/rank/update.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('rank')
def update():
    """ """
    rank_id = request.json.get("rank-id", None)
    name = request.json.get("name", None)
    rank = request.json.get("rank", None)
    data = core.rank.update(rank_id=rank_id, name=name, rank=rank)
    data = set_message(data)
    return jsonify(data)

@api_rank.route('/api/1.0/rank/remove.json', methods=['DELETE'])
@authentication
@check_rank(10)
@get_hash('rank')
def remove():
    """ """
    rank_id = request.args.get("_id", None)
    data = core.rank.remove(rank_id=rank_id, my_rank=g.my['rank'])
    data = set_message(data)
    return jsonify(data)
