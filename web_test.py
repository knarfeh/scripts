#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
import requests


# fork from https://gist.github.com/klb3713/6077267
__author__ = "knarfeh@outlook.com"

HOST = "http://********"
PORT = "****"
URI = "/v1/notifications/940419bf-cfc5-4aab-bf82-7737da0ee374/messages"
TOTAL = 0
SUCCEDED = 0
FAILED = 0
EXCEPT = 0
MAXTIME = 0
MINTIME = 30
TOTALTIME = 0
LESS3S = 0
MORE3S = 0

headers = {
    'content-type': 'application/json',
    'User-Agent': 'Alauda/Notification/1.0'
}

payload = {
  "template_type": "pipeline_result",
  "data": {
    "subject": "this is a pipeline result",
    "content": "failed",
    "time": "2016-11-05T00:00:00.0Z",
    "payload": {
        "pipeline": "pipelin-one",
        "failed_task": "task-one",
        "registry": "private-registry-1",
        "repository": "myrepo",
        "image_tag": "latest",
        "digest": "sha56:asdasdas",
        "started_at": "iso date",
        "ended_at": "iso date"
    }
  }
}


class RequestThread(threading.Thread):

    def __init__(self, thread_name, post_data):
        threading.Thread.__init__(self)
        self.test_count = 0
        self.post_data = post_data

    def run(self):
        self.test_performance()

    def test_performance(self):
        global TOTAL
        global SUCCEDED
        global FAILED
        global EXCEPT
        global LESS3S
        global MORE3S
        global TOTALTIME

        try:
            start_time = time.time()
            url = HOST + ":" + PORT + URI
            res = requests.post(url, json=payload, headers=headers, timeout=20)

            time_span = time.time() - start_time
            if res.status_code == 204:
                SUCCEDED += 1
                TOTALTIME += time_span
            else:
                FAILED += 1

            self.maxtime(time_span)
            self.mintime(time_span)

            if time_span > 3:
                MORE3S += 1
            else:
                LESS3S += 1
        except Exception as e:
            print("Error: {}".format(e))
            EXCEPT += 1
        finally:
            TOTAL += 1

    def maxtime(self, time_span):
        global MAXTIME
        if time_span > MAXTIME:
            MAXTIME = time_span

    def mintime(self, time_span):
        global MINTIME
        if time_span < MINTIME:
            MINTIME = time_span


def test(thread_count, post_data):
    global TOTAL
    global SUCCEDED
    global FAILED
    global EXCEPT
    global LESS3S
    global MORE3S
    global TOTALTIME
    global MINTIME
    global MAXTIME

    TOTAL = 0
    SUCCEDED = 0
    FAILED = 0
    EXCEPT = 0
    LESS3S = 0
    MORE3S = 0
    TOTALTIME = 0
    MINTIME = 100
    MAXTIME = 0

    print("----------task start--------------")
    start_time = time.time()
    i = 0
    TOTAL = 0
    while i < thread_count:
        t = RequestThread("thread" + str(i), post_data)
        t.start()
        i += 1

    t = 0
    while TOTAL < thread_count and t < 60:
        t += 1
        time.sleep(1)

    print("----------task end--------------")
    print("\n\n\n")
    print("total time: {}".format(time.time()-start_time))
    print("thread_count: {}".format(thread_count))
    print("post_data: {}".format(post_data))
    print("total: {}, succeded: {}, failed: {}, except: {}".format(
        TOTAL, SUCCEDED, FAILED, EXCEPT))
    print("response maxtime: {}".format(MAXTIME))
    print("response mintime: {}".format(MINTIME))
    print("great than 3 seconds: %d, percent: %0.2f" %
          (MORE3S, float(MORE3S)/TOTALTIME))
    print("less than 3 seconds: %d, percent: %0.2f" %
          (LESS3S, float(LESS3S)/TOTALTIME))
    print("average time: %0.2f" % (TOTALTIME / SUCCEDED))


def single_test():
    print("HOST: {}, PORT: {}, URI: {}".format(HOST, PORT, URI))
    url = HOST + ":" + PORT + URI
    print("url: {}".format(url))

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=20)
    except Exception as e:
        print("Sending messages to url: {}, error messages: {}".format(url, e))

    if res.status_code == 204:
        print("request ok")
    else:
        print("request failed, status: {}".format(res.status_code))


if __name__ == "__main__":
    test(1000, payload)
    # single_test()
