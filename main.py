# -*- coding: utf-8 -*-
import time
import string
import urllib2
import argparse
import sys
parser = argparse.ArgumentParser()

parser.add_argument('--interval', type=int, default='300', help='seconds')
args = parser.parse_args()

dict = {}
url = 'http://www.pedalro.kr/station/station.do?method=stationState&menuIdx=st_01'

ts = time.strftime("%Y-%m-%d-%I-%M", time.localtime())
filename = str(ts) + ".csv"
count = 1

while True:
    response = ''
    try :
        response = urllib2.urlopen(url);
    except urllib2.URLError, err:
        print "URL Open Error :", err.reason
        # 나중에 GUI 만들면 자동으로 STOP되게 하던가
        # 일단은 10초후에 재시도하도록 해놓음
        time.sleep(args.interval)
        continue

    print("%d번째 저장입니다.") % (count)
    ts = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    str = ''

    for line in response:
        if "			title : " in line:
            s = line.lstrip()
            s = s.lstrip("title : '")
            s = s.rstrip("\n")
            s = s.split("|")
            dict[s[0]] = s[3]
    if count == 1:
        str += 'ts,' + ",".join(dict.keys()) + '\n'

    str += ts + "," + ",".join(dict.values()) + '\n'

    count += 1
    print(str)
    f = open(filename, "a")
    f.write(str)
    f.close()
    dict.clear()
    time.sleep(args.interval)
