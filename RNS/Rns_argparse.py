import argparse

from Remote_network_service import NetworkServiceChecker

DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 8080

arg_parse = argparse.ArgumentParser(description="remote network service")

arg_parse.add_argument('--host' , action="store" , dest="host" , default=DEFAULT_SERVER_HOST)
arg_parse.add_argument('--port' , action="store" , dest="port" , type= int , default=DEFAULT_SERVER_PORT)
arg_parse.add_argument('--timeout' , action="store" , dest="timeout" , type=int , default=DEFAULT_TIMEOUT)

given_args = arg_parse.parse_args()

host , port , timeout = given_args.host , given_args.port , given_args.timeout

checker = NetworkServiceChecker(host , port, timeout=timeout)
print("checking for network service {} : {}".format(host,port))
if checker.check():
    print("service is avalaible again")