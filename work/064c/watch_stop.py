#!/usr/bin/env python3
"""Generic boundary watcher: snapshot a worker's checkpoint and stop it once it
reaches a given index, so a helper covering the tail leaves no overlap.

usage: watch_stop.py <partial-file> <snapshot-file> <pgrep-tag> <stop_at>
"""
import json, os, shutil, signal, subprocess, sys, time

part, snap, tag, stop_at = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
while True:
    try:
        d = json.load(open(part))['summary']['done_upto']
        if d >= stop_at:
            shutil.copy(part, snap)
            for pid in subprocess.run(['pgrep', '-f', tag], capture_output=True,
                                      text=True).stdout.split():
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except Exception:
                    pass
            print('snapshot at done_upto=%d, stopped %s' % (d, tag), flush=True)
            break
    except Exception as e:
        print('watch:', e, flush=True)
    time.sleep(20)
