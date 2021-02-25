from websocket import create_connection
import json
import numpy as np
from skimage.io import imsave
from skimage.io import imread
import pathlib

path = pathlib.Path(__file__).parent.absolute()

def start(ws):
    ws.send(json.dumps( { "data": { "message": "Let's start"} }))

def get_params(ws):
    params = json.loads(ws.recv())
    return params["data"]["width"], params["data"]["height"], params["data"]["number"]

def send_params(ws, totalSteps, noise, shuffle):
    ws.send( json.dumps( { "data": { "width": width, "height": height, "totalSteps": totalSteps, "noise": noise, "shuffle": shuffle } } ) )

def get_digits(ws):
    digit_matrix = json.loads(ws.recv())
    digit = []
    matrix = []
    for d in digit_matrix["data"]:
        matrix.append( digit_matrix["data"][d] )
        digit.append( d )
        imsave(path.absolute().as_posix() + '/from_server' + '/image' + d + '.jpg', np.array(digit_matrix["data"][d]))
    matrix = np.array(matrix)
    digit = np.array(digit)
    return digit, matrix

def ready(ws):
    ws.send(json.dumps({ "data": { "message": "Ready" } } ) )

def get_problem(ws):
    problem = json.loads(ws.recv())
    imsave(path.absolute().as_posix() + '/from_server' + '/problem.jpg', np.array(problem["data"]["matrix"]))
    return problem["data"]["currentStep"], problem["data"]["matrix"]

def solution(digit_set, matrix_set, step, matrix):
    return matrix

def send_solution(ws, step, answer):
    ws.send(json.dumps({ "data": { "step": step, "answer": answer } }))

def get_right_solution(ws):
    right_solution = json.loads(ws.recv())
    return right_solution["data"]["step"], right_solution["data"]["answer"]

def send_bye(ws):
    ws.send(json.dumps({ "data": { "message": "Bye" } }))

def get_report(ws):
    report = json.loads(ws.recv())
    return report["data"]["successes"]

ws = create_connection("wss://sprs.herokuapp.com/first/[session-id]")
start(ws)

width, height, number = get_params(ws)

totalSteps = 10
send_params(ws, totalSteps = totalSteps, noise = 0, shuffle = False)

digit_set, matrix_set = get_digits(ws)

ready(ws)
step, matrix = get_problem(ws)
answer = solution(digit_set, matrix_set, step, matrix)
send_solution(ws, step, answer)
right_solution = json.loads(ws.recv())

print("------------")
print(right_solution)
print("------------")



send_bye(ws)
print("done: ", get_report(ws), " out of: ", totalSteps)
ws.close()

