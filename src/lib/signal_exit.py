import signal

def ctrl_c_exit():
    signal.signal(signal.SIGINT,exit)