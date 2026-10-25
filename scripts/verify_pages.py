import urllib.request
import sys

pages = [
    '/', '/dashboard/', '/live-monitoring/', '/predictions/',
    '/optimization/', '/alerts/', '/model/', '/sensors/',
    '/reports/', '/upload/', '/methodology/', '/datasets/',
]

all_ok = True
for p in pages:
    try:
        resp = urllib.request.urlopen(f'http://127.0.0.1:8000{p}')
        status = resp.status
        size = len(resp.read())
        print(f'{p:25s}  HTTP {status}  ({size:,} bytes)')
        if status != 200:
            all_ok = False
    except Exception as e:
        print(f'{p:25s}  FAILED: {e}')
        all_ok = False

print()
if all_ok:
    print('ALL PAGES PASSED (HTTP 200)')
else:
    print('SOME PAGES FAILED')
    sys.exit(1)
