#!flask/bin/python
from flask import jsonify
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask import abort
from flask import make_response

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('finance', __name__, url_prefix='/finance')

from logic import finance as fin
from flask import current_app

@bp.route('/index', methods=["GET"])
def index():
    return render_template('finance/search.html')

@bp.route('/detail/<string:code>', methods=["GET"])
def detail(code):
    current_app.logger.error("detail:"+code)
    return render_template('finance/detail.html',stockcode=code)

# 000858 ;000651;002466 ;002415 ;000423

#########################for  api data#######################################################################################################
@bp.route('/stockscore/<string:stockcode>', methods=['GET'])
def getScore(stockcode):   
    # print(stockcode)
    current_app.logger.info("getScore:"+stockcode)
    return fin.getStockScore(stockcode)

@bp.route('/indstockscore/<string:indname>', methods=['GET'])
def indstockscore(indname):   
    # import pdb;pdb.set_trace()
    current_app.logger.info("indstockscore:"+indname)
    return fin.getIndustryStockScore(indname)

@bp.route('/industryList', methods=['GET'])
def industryList():   
    return fin.getAllIndustry()

