from flask import Blueprint, request

from app.extensions import db
from app.utils.TokenOperate import TokenOperate
from app.utils.ResponseResult import ResponseResult
from app.utils.Public import is_login

donations = Blueprint('donations', __name__)


@donations.route('/donations', methods=['GET'])
def get_donations():
    if request.method == 'GET':
        if not is_login():
            return ResponseResult.get_result('Declined')
        return ResponseResult.get_result('Success')


@donations.route('/donations', methods=['POST'])
def post_donations():
    if request.method == 'POST':
        if not is_login():
            return ResponseResult.get_result('Declined')
        in_json = request.json
        donate_for = int(in_json['demand'])
        donor = int(in_json['donor'])
        express_code = in_json['express_code']
        supplies = in_json['supplies']
        sql = '''
        insert into app.demands("type", publisher, donate_for, express_code)
        values(:type, :publisher, :donate_for, :express_code)
        '''
        db.session.execute(
            sql, {'type': '捐赠', 'publisher': donor, 'donate_for': donate_for, 'express_code': express_code}
        )
        rs = db.session.execute(
            'select id from app.demands where publisher = :publisher order by id desc', {'publisher': donor}
        ).fetchall()
        demand = rs[0][0]
        for supply in supplies:
            sql = '''
            insert into app.supplies("name", specification, number, demand)
            values(:name, :specification,:number,:demand)
            '''
            db.session.execute(
                sql,
                {
                    'name': supply['name'],
                    'specification': supply['specification'],
                    'number': int(supply['number']),
                    'demand': demand
                }
            )
        return ResponseResult.get_result('Success')
