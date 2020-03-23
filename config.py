import datetime as dt
import os

# ip = "192.168.1.134"
ip = "127.0.0.1"

# connections with instances of KSP
# conns = [
#    {'name': "Game ml1", "address": ip, "rpc_port": 50000, "stream_port": 50001},
# ]
# conns = [
#    {'name': "Game ml1", "address": ip, "rpc_port": 50000, "stream_port": 50001},
#    {'name': "Game ml2", "address": ip, "rpc_port": 50002, "stream_port": 50003},
#    {'name': "Game ml3", "address": ip, "rpc_port": 50004, "stream_port": 50005},
#    {'name': "Game ml4", "address": ip, "rpc_port": 50006, "stream_port": 50007},
# ]
# conns = [
#    {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50000, "stream_port": 50001},
#    {'name': "Game ml2", "address": "192.168.1.12", "rpc_port": 50002, "stream_port": 50003},
#    {'name': "Game ml3", "address": "192.168.1.12", "rpc_port": 50004, "stream_port": 50005},
#    {'name': "Game ml4", "address": "192.168.1.12", "rpc_port": 50006, "stream_port": 50007},
#    {'name': "Game ml5", "address": "192.168.1.12", "rpc_port": 50008, "stream_port": 50009},
#    {'name': "Game ml6", "address": "192.168.1.12", "rpc_port": 50010, "stream_port": 50011},
#    #{'name': "Game ml7", "address": "192.168.1.5", "rpc_port": 50012, "stream_port": 50013},
#    #{'name': "Game ml8", "address": "192.168.1.5", "rpc_port": 50014, "stream_port": 50015},
#    #{'name': "Game ml9", "address": "192.168.1.5", "rpc_port": 50016, "stream_port": 50017},
#    {'name': "Game ml10", "address": "127.0.0.1", "rpc_port": 50018, "stream_port": 50019},
#    {'name': "Game ml11", "address": "127.0.0.1", "rpc_port": 50020, "stream_port": 50021},
# ]

conns = [
   {'name': "Game ml1", "address": "192.168.1.8", "rpc_port": 50000, "stream_port": 50001},
   {'name': "Game ml1", "address": "192.168.1.8", "rpc_port": 50002, "stream_port": 50003},
   {'name': "Game ml1", "address": "192.168.1.8", "rpc_port": 50004, "stream_port": 50005},
   {'name': "Game ml1", "address": "192.168.1.8", "rpc_port": 50006, "stream_port": 50007},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50008, "stream_port": 50009},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50010, "stream_port": 50011},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50012, "stream_port": 50013},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50014, "stream_port": 50015},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50016, "stream_port": 50017},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50018, "stream_port": 50019},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50020, "stream_port": 50021},
   {'name': "Game ml1", "address": "192.168.1.12", "rpc_port": 50022, "stream_port": 50023},
]

# A3C PARAMETERS
OUTPUT_GRAPH = True
LOG_DIR = './log'
result_file = os.path.join(LOG_DIR, "res"+str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+".csv").replace(' ', '_'))
fieldnames = ['counter', 'altitude', 'reward']
N_WORKERS = len(conns)
MAX_EP_STEP = 200000
GLOBAL_NET_SCOPE = 'Global_Net'
UPDATE_GLOBAL_ITER = 10
GAMMA = 0.90
ENTROPY_BETA = 0.01
LR_A = 0.0001
LR_C = 0.001

# environment parameters
turn_start_altitude = 250
turn_end_altitude = 45000
MAX_ALT = 45000
CONTINUOUS = True


