import datetime
import json

from flask import Blueprint, request

from app.extensions import db
from app.utils.TokenOperate import TokenOperate
from app.utils.ResponseResult import ResponseResult

from app.views.public import get_token_and_id

demands = Blueprint('demands', __name__)


@demands.route('/all_demands', methods=['GET'])
def get_all_demands():
    if request.method == 'GET':
        sql = '''
        select
            t2.d_id,
            t2.d_title,
            t2.d_content,
            t2.publisher,
            t2.u_phone,
            t2.d_pub_time,
            t2.d_is_review,
            t1.reviewer,
            t2.d_is_cancel
        from
            (
            select
                t2.d_id,
                t2.d_title,
                t2.d_content,
                coalesce(t1.u_name, t1.u_nick) as publisher,
                t1.u_phone,
                t2.d_pub_time,
                t2.d_is_review,
                t2.d_reviewer,
                t2.d_is_cancel
            from
                (select u_id, u_nick, u_name, u_phone from app.users) as t1
            right join
                (select d_id, d_title, d_content, d_publisher, d_pub_time, d_is_review, d_reviewer, d_is_cancel from app.demands) as t2
            on
                t1.u_id = t2.d_publisher
            ) as t2
        left join
            (select u_id, coalesce(u_name, u_nick)as reviewer from app.users) as t1
        on
            t2.d_reviewer = t1.u_id
        order by
            d_pub_time desc
        '''
        rs = db.session.execute(sql).fetchall()
        data = [
            {
                'id': r[0],
                'title': r[1],
                'content': json.loads(r[2]),
                'publisher': r[3],
                'phone': r[4],
                'pub_time': str(r[5]),
                'is_review': '已审核' if r[6] else '未审核',
                'reviewer': r[7],
                'is_cancel': '已撤销' if r[8] else '展示中'
            } for r in rs
        ]
        return ResponseResult.get_result('Success', data)


@demands.route('/demands', methods=['GET'])
def get_some_no_cancel_demands():
    if request.method == 'GET':
        # 获取请求参数
        num = int(request.args['num']) if request.args['num'] else 1000
        page = int(request.args['num']) * int(request.args['page']) if request.args['page'] else 0
        # print(num, page)
        sql = '''
        select
            t2.d_id,
            t2.d_title,
            t2.d_content,
            t2.publisher,
            t2.u_phone,
            t2.d_pub_time,
            t2.d_is_review,
            t1.reviewer,
            t2.d_is_cancel
        from
            (
            select
                t2.d_id,
                t2.d_title,
                t2.d_content,
                coalesce(t1.u_name, t1.u_nick) as publisher,
                t1.u_phone,
                t2.d_pub_time,
                t2.d_is_review,
                t2.d_reviewer,
                t2.d_is_cancel
            from
                (select u_id, u_nick, u_name, u_phone from app.users) as t1
            right join
                (select d_id, d_title, d_content, d_publisher, d_pub_time, d_is_review, d_reviewer, d_is_cancel from app.demands where d_is_cancel = false) as t2
            on
                t1.u_id = t2.d_publisher
            ) as t2
        left join
            (select u_id, coalesce(u_name, u_nick)as reviewer from app.users) as t1
        on
            t2.d_reviewer = t1.u_id
        order by
            d_pub_time desc
        limit :num
        offset :page
        '''
        rs = db.session.execute(sql, {'num': num, 'page': page}).fetchall()
        data = [
            {
                'id': r[0],
                'title': r[1],
                'content': json.loads(r[2]),
                'publisher': r[3],
                'phone': r[4],
                'pub_time': str(r[5]),
                'is_review': r[6],
                'reviewer': r[7],
                'is_cancel': r[8]
            } for r in rs
        ]
        # print(data)
        return ResponseResult.get_result('Success', data)


@demands.route('/my_pub_demands', methods=['GET'])
def get_my_pub_demands():
    if request.method == 'GET':
        # token验证
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        # 验证通过
        num = int(request.args['num'])
        page = int(request.args['num']) * int(request.args['page'])
        # 查询sql
        sql = '''
        select
        t2.d_id,
        t2.d_title,
        t2.d_content,
        coalesce(t1.u_name, t1.u_nick),
        t1.u_phone,
        t2.d_pub_time,
        t2.d_is_review,
        t2.d_is_cancel
        from
        (select u_id, u_nick, u_name, u_phone from app.users) as t1
        right join
        (select d_id, d_title, d_content, d_publisher, d_pub_time, d_is_review, d_is_cancel from app.demands where d_publisher = :u_id and d_is_cancel = false) as t2
        on
        t1.u_id = t2.d_publisher and
        t2.d_publisher = :u_id
        order by
        d_pub_time desc
        limit :num
        offset :page
        '''
        rs = db.session.execute(sql, {'num': num, 'page': page, 'u_id': u_id}).fetchall()
        data = [
            {
                'id': r[0],
                'title': r[1],
                'content': json.loads(r[2]),
                'publisher': r[3],
                'phone': r[4],
                'pub_time': str(r[5]),
                'is_review': r[6],
                'is_cancel': r[7]
            } for r in rs
        ]
        return ResponseResult.get_result('Success', data)


@demands.route('/my_cancel_demands', methods=['GET'])
def get_my_cancel_demands():
    if request.method == 'GET':
        # token验证
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        # 验证通过
        num = int(request.args['num'])
        page = int(request.args['num']) * int(request.args['page'])
        # 查询sql
        sql = '''
        select
        t2.d_id,
        t2.d_title,
        t2.d_content,
        coalesce(t1.u_name, t1.u_nick),
        t1.u_phone,
        t2.d_pub_time,
        t2.d_is_review,
        t2.d_is_cancel
        from
        (select u_id, u_nick, u_name, u_phone from app.users) as t1
        right join
        (select d_id, d_title, d_content, d_publisher, d_pub_time, d_is_review, d_is_cancel from app.demands where d_publisher = :u_id and d_is_cancel = true) as t2
        on
        t1.u_id = t2.d_publisher and
        t2.d_publisher = :u_id
        order by
        d_pub_time desc
        limit :num
        offset :page
        '''
        rs = db.session.execute(sql, {'num': num, 'page': page, 'u_id': u_id}).fetchall()
        data = [
            {
                'id': r[0],
                'title': r[1],
                'content': json.loads(r[2]),
                'publisher': r[3],
                'phone': r[4],
                'pub_time': str(r[5]),
                'is_review': r[6],
                'is_cancel': r[7]
            } for r in rs
        ]
        return ResponseResult.get_result('Success', data)


@demands.route('publish_demand', methods=['POST'])
def do_publish():
    if request.method == 'POST':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        if len((request.json['title']).strip()) == 0:
            return ResponseResult.get_result('Error', [{'msg': ''}])
        d_title = request.json['title']
        d_publisher = int(request.json['publisher'])
        d_content = json.dumps(request.json['content'], ensure_ascii=False)
        d_pub_time = str(datetime.datetime.now().replace(microsecond=0))
        # print(d_title,d_publisher,d_content,d_pub_time)
        sql = '''
                insert into app.demands(d_title, d_content, d_publisher, d_pub_time) values(:d_title, :d_content, :d_publisher, :d_pub_time)
                '''
        db.session.execute(sql, {'d_title': d_title, 'd_content': d_content, 'd_publisher': d_publisher,
                                 'd_pub_time': d_pub_time})
        return ResponseResult.get_result('Success')


@demands.route('/modify_demand', methods=['POST'])
def modify_demand_by_id():
    if request.method == 'POST':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        # 验证通过，更新数据库
        d_id, d_content = int(request.json['id']), json.dumps(request.json['content'], ensure_ascii=False)
        sql = '''
        update app.demands set d_content = :d_content where d_id = :d_id
        '''
        db.session.execute(sql, {'d_content': d_content, 'd_id': d_id})
        return ResponseResult.get_result('Success')


@demands.route('/cancel_demand', methods=['POST'])
def cancel_demand_by_id():
    if request.method == 'POST':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        d_id = int(request.json['id'])
        sql = '''
        update app.demands set d_is_cancel = true where d_id = :d_id
        '''
        db.session.execute(sql, {'d_id': d_id})
        return ResponseResult.get_result('Success')


@demands.route('/do_review', methods=['PUT'])
def do_review():
    if request.method == 'PUT':
        token, u_id = get_token_and_id()
        if not TokenOperate.check_token(token, u_id):
            return ResponseResult.get_result('Declined')
        d_id = int(request.json['d_id'])
        reviewer = int(request.headers['uid'])
        review_time = datetime.datetime.now().replace(microsecond=0)
        sql = '''
        update app.demands set d_is_review = true, d_reviewer = :reviewer, d_review_time = :review_time where d_id = :d_id
        '''
        db.session.execute(sql, {'reviewer': reviewer, 'd_id': d_id, 'review_time':review_time})
        return ResponseResult.get_result('Success')
