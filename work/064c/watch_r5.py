#!/usr/bin/env python3
"""Stop worker r5 exactly at the boundary where helper r5c takes over.

r5 owns [177320, 212780) but helpers r5c [190000,199000) and r5b [199000,...)
already cover the upper part.  When r5's checkpoint reaches an index in
[189000, 190000) we snapshot it as a completed interval and stop it, so the
union of intervals has no overlap.  Nothing else is touched.
"""
import json, os, shutil, signal, subprocess, time

PART = 'results/n12-r5.json.partial'
SNAP = 'results/n12-r5-snapshot.json'
TAG = 's2e_scan11.py --n 12 --range 177320:212780'

while True:
    try:
        s = json.load(open(PART))['summary']
        d = s['done_upto']
        if d >= 189000:
            shutil.copy(PART, SNAP)
            out = subprocess.run(['pgrep', '-f', TAG], capture_output=True,
                                 text=True).stdout.split()
            for pid in out:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except Exception:
                    pass
            print('snapshotted r5 at done_upto=%d and stopped it' % d,
                  flush=True)
            break
    except Exception as e:
        print('watch:', e, flush=True)
    time.sleep(20)
