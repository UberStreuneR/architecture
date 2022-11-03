import Pyro4

@Pyro4.expose
class SquareEq(object):
    def solve(self, a, b, c):
        result = f"Solving {a}x^2 + {b}x + {c} = 0. "
        D = b**2 - 4*a*c
        if D < 0:
            return result + "No solutions, D < 0"
        elif D == 0:
            return result + f"Solution: x = {-b/(2*a)}"
        x1 = (-b + D**0.5)/(2*a)
        x2 = (-b - D**0.5)/(2*a)
        return result + f"Solutions: x1 = {x1}, x2 = {x2}"

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(SquareEq)
    ns.register('server', str(uri))
    print(f'Ready to listen')
    daemon.requestLoop()

if __name__ == '__main__':
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
exit