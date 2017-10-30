import argparse

from asyncio import get_event_loop

from todo_crm import init


parser = argparse.ArgumentParser()
parser.add_argument('--port')

args = parser.parse_args()
port = args.port or '8080'
    
loop = get_event_loop()
loop.run_until_complete(init(loop, port))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

