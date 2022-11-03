from concurrent.futures import ThreadPoolExecutor
import time
import random
import threading

class PingPong:
    def __init__(self) -> None:
        self.ping_lock = threading.Lock()
        self.pong_lock = threading.Lock()
        self.pong_lock.acquire()

    def ping(self):
        self.ping_lock.acquire()
        print("Ping")
        time.sleep(0.3)
        self.pong_lock.release()

    def pong(self):
        self.pong_lock.acquire()
        print("Pong")
        time.sleep(0.3)
        self.ping_lock.release()
    
    def run(self):
        with ThreadPoolExecutor(max_workers=2) as executor:
            for i in range(random.randint(5, 10)):
                executor.submit(self.pong)
                executor.submit(self.ping)

if __name__ == '__main__':
    game = PingPong()
    game.run()