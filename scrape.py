import requests
import threading
import functools

def f(y, OK_dts, lk):
    b_url = 'http://audio.radio24.ilsole24ore.com/radio24_audio'

    for m in range(1, 12 +1):
        for d in range(1, 31 +1):
            fname = [
                '{:04}'.format(y),
                '{:02}'.format(m),
                '{:02}'.format(d),
            ]
            fname = ''.join(fname)[2:]
            fname += '-lazanzara.mp3'

            url = '/'.join([b_url, '{:04}'.format(y), fname])
            r = requests.head(url)
            print('*** Trying {}'.format(url))
            if r.status_code != 200: continue
            lst = [
                '{:04}'.format(y),
                '{:02}'.format(m),
                '{:02}'.format(d),
            ]
            OK_dts.append('-'.join(lst))
            print(OK_dts)

    with lk: lk.notify()

ts = []
OK_dts = []
lk = threading.Condition()

for y in range(2008, 2015 +1):
    ts.append(threading.Thread(target=f, args=(y, OK_dts, lk)))

for t in ts: t.start()

with lk:
    all_done = lambda ts=ts: \
                  not functools.reduce(lambda x,y: x or y, \
                                          [t.is_alive() for t in ts])
    lk.wait_for(all_done)

with open('episodes.timestamp', 'a') as f:
    for x in OK_dts:
        f.write(x)
        f.write('\n')
