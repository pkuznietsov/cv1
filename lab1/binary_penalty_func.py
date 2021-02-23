from websocket import create_connection
import json
import numpy as np
from skimage.io import imsave


ws = create_connection("wss://sprs.herokuapp.com/first/[session-id]")
ws.send(json.dumps( { "data": { "message": "Let's start"} }))

params =  json.loads(ws.recv())

width = params["data"]["width"]
height = params["data"]["height"]
number = params["data"]["number"]

noise = 0
shuffle = False
totalSteps = 10
ws.send( json.dumps( { "data": { "width": width, "height": height, "totalSteps": totalSteps, "noise": noise, "shuffle": shuffle } } ) )

digit_matrix = json.loads(ws.recv())
matrix = []
for digit in digit_matrix["data"]:
    matrix.append( digit_matrix["data"][digit])
matrix_seq = np.array(matrix)

ws.send( json.dumps( { "data": { "message": "Ready" } } ) )
problem = json.loads(ws.recv())

currentStep = problem["data"]["currentStep"] # number of problem
matrix = problem["data"]["matrix"] # problem in matrix form

answer = matrix
ws.send(json.dumps({ "data": { "step": currentStep, "answer": answer } }))


#ws.send( json.dumps( { "data": { "message": "Ready" } } ) )
#ws.send( json.dumps( { "data": { "message": "Bye" } } ) )
#new_problem = json.loads(ws.recv())
#print(new_problem)



ws.close()
