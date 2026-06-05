import socket, threading, sys

def handle(c):
    data = c.recv(4096)
    if not data:
        c.close()
        return
    line = data.split(b'\r\n')[0].decode()
    if line.startswith('CONNECT '):
        h, p = line.split(' ')[1].split(':')
        p = int(p)
        r = socket.socket()
        r.settimeout(30)
        try:
            r.connect((h, p))
            c.send(b'HTTP/1.1 200 OK\r\n\r\n')
            threading.Thread(target=lambda: pipe(r, c), daemon=True).start()
            pipe(c, r)
        except Exception as e:
            try:
                c.send(f'HTTP/1.1 502 Bad Gateway\r\n\r\n{str(e)}'.encode())
            except:
                pass
        finally:
            r.close()

def pipe(a, b):
    try:
        while True:
            d = a.recv(4096)
            if not d:
                break
            b.sendall(d)
    except:
        pass

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 1080))
s.listen(100)
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle, args=(conn,), daemon=True).start()
