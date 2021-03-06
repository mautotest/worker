# -*- coding: utf-8 -*-
# -----------------------------------------------------
# @Software: PyCharm
# @File: app.py
# @Author: majiayang
# @Institution: huawei, China
# @E-mail: 609921831@qq.com.com
# @Site:
# @Time: 12月 21, 2020
# -----------------------------------------------------
from flask import Flask,request
from common.status import s, StatusType
from job import start_heart, start_work
from common.result import Result
import logging
import datetime
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    app.logger.info('Hello World!')
    return 'Hello World:' + s.status


# 分配任务
@app.route('/worker', methods=["POST"])
def work():
    cmd = request.form["cmd"]
    app.logger.info('get work!========>cmd:{}'.format(cmd))
    if s.status != StatusType.ONELINE:
        return Result().bulid_fail()
    s.status = StatusType.PENDING
    date = datetime.datetime.now() + datetime.timedelta(seconds=3)
    args = [cmd,"12345"]
    from queue import Queue
    test_queue = Queue()
    job = start_work(date=date, args=args,test_queue=test_queue)
    return Result({"status": StatusType.PENDING, "job": job.id}).bulid_success()


if __name__ == '__main__':
    start_heart()
    logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='## %Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    worker_port = os.environ.get("MTEST_WORKER_PORT", 5022)
    app.run(port=worker_port)
