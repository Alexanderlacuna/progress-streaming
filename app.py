
import time
from flask import Flask, render_template
import subprocess
# import gevent

from flask import Flask
from flask_socketio import SocketIO,emit
from flask import render_template

__author__ = 'BonfaceKilz'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app)


def background_thread(socket_obj):
    def run_process(cmd):
        socket_obj.emit('console-log',
                        {'data': f"{cmd}\n"})
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True)
        for c in iter(lambda: process.stdout.read(1), b''):
            socket_obj.emit('console-log',
                            {'data': c.decode('utf-8')})
            socket_obj.sleep(0.01)
        socket_obj.emit("console-log",
                        {'data': "DONE"})
    gevent.joinall(
        [gevent.spawn(run_process, "guix pull --dry-run")])


def initial_setup():
    return None


@app.route("/")
def do_mapping():
    return render_template("index.html")


def mapping_a():

    emit("message", {"stage_name": "stage_1", "data": "calling_function_A"})
    return "results A"


def mapping_b(param):
    emit("message", {"stage_name": "stage_1", "data": "calling_function_B"})
    return "results B"


def mapping_c(param):
    emit("message", {"stage_name": "stage_1", "data": "calling_function_A"})
    return "results C"


def call_emitter_function():
    pass


@socketio.on("mapping")
def func_that_does_mapping():

    # stage 1

    emit("running",{"stage_name":"stage_1"})
    time.sleep(3)

    mapping_a()

    

    # stage 2

    emit("running",{"stage_name":"stage_2"})

    mapping_b("data")

    time.sleep(2)

    # stage 3

    emit("running",{"stage_name":"stage_3"})

    mapping_c("Data")

    time.sleep(3)

    # stage two computation


if __name__ == '__main__':
    socketio.run(app, debug=True)
