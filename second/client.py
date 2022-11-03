from datetime import datetime
import random
import Pyro4
import time

server = Pyro4.Proxy(f"PYRONAME:server")

def run():
    while True:
        a = random.randint(1, 4)
        b = random.randint(3, 6)
        c = random.randint(1, 4)
        print(server.solve(a, b, c))
        time.sleep(1)

if __name__ == '__main__':
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
exit