import datetime
import re
import psutil
import time

def cpu_time(p):
    if p.cpu_times():
        return time.strftime("%M:%S",
                             time.localtime(sum(p.cpu_times())))
    else:
        return ''


def start_time(p):
    today_day = datetime.date.today()
    if p.create_time():
        ctime = datetime.datetime.fromtimestamp(p.create_time())
        if ctime.date() == today_day:
            return ctime.strftime("%H:%M")
        else:
            return ctime.strftime("%b%d")
    else:
        return ''


def status(p):
    if p.status():
        return p.status()[0].title()
    else:
        return ''


def get_processes(all):
    processes = dict()
    if all:
        for proc in psutil.process_iter():
            for parent in proc.parents():
                pid = parent.pid
                if pid not in processes:
                    processes[pid] = parent
                for ch in parent.children(recursive=True):
                    cpid = ch.pid
                    if cpid not in processes:
                        processes[cpid] = ch

    else:
        for proc in psutil.process_iter():
            pid = proc.pid
            processes[pid] = proc
    return processes


supported_commands = ['ps']

simple_keys = ['e', 'l', 'f']
with_value_keys = ['p', 'u']
supported_arg_keys = simple_keys + with_value_keys

keys_values = {
    'e': False,
    'l': False,
    'f': False,
    'p': [],
    'u': []
}

default_params = {'PID', 'TTY', 'TIME', 'CMD'}
keysParams = {
    'l': {'F', 'S', 'UID', 'PPID', 'C', 'PRI', 'NI', 'ADDR', 'WCHAN'},
    'f': {'UID', 'PPID', 'C', 'STIME'}
}

command = input()

if not re.match(r'^ps', command):
    raise Exception("Unresolved command")

command_args = command.split(' -')
command_args.pop(0)

for arg in command_args:
    arg_parts = arg.split(' ')
    arg_keys = list(arg_parts.pop(0))
    for key in arg_keys:
        if key in supported_arg_keys:
            if key in simple_keys:
                keys_values[key] = True
            if key in with_value_keys:
                keys_values[key] = arg_parts

fields_funcs = {
    'PID': lambda p: p.pid,
    'PPID': lambda p: p.ppid(),
    'TIME': lambda p: cpu_time(p),
    'CMD': lambda p: p.name(),
    'TTY': lambda p: p.terminal(),
    'UID': lambda p: p.username(),
    'C': lambda p: p.cpu_percent(),
    'STIME': lambda p: start_time(p),
    'S': lambda p: status(p)
}

processes = get_processes(keys_values['e'])

if keys_values['u']:
    users_processes = {}
    users = keys_values['u']
    for proc in processes.values():
        if proc.username() in users:
            users_processes[proc.pid] = proc
    processes = users_processes

if keys_values['p']:
    processes = {}
    pidsStr = keys_values['p']
    pids = list(map(int, pidsStr))
    for pid in pids:
        if pid not in processes:
            proc = psutil.Process(pid)
            processes[pid] = proc

if keys_values['l']:
    default_params.update(keysParams['l'])

if keys_values['f']:
    default_params.update(keysParams['f'])

template = ''
for param in default_params:
    template += '{:<10}'

print(template.format(*list(dict.fromkeys(default_params))))

for p in processes.values():
    paramsValues = []
    for param in list(dict.fromkeys(default_params)):
        val = ''
        if param in fields_funcs:
            val = str(fields_funcs[param](p))
        paramsValues.append(val)
    print(template.format(*paramsValues))

#psutil.test()
# p = psutil.Process(146472)
# print(p)
