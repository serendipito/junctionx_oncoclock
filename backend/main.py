from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import random
import string
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import pandas as pd
import numpy as np
import datetime
import json


@app.get("/")
async def root():
    with open('new_treatments.txt', 'r') as f:
        lines = f.readlines()
        data = []
        for line in lines:
                if '{' in line:
                    #print(line.replace("'", '"').rstrip(','))
                    lc = json.loads(line.replace("'", '"').strip().rstrip(','))
                    data.append(lc)

    return data


@app.get("/reset/")
async def reset():
    empty = """{'id': 'english0', 'start_date': '2023-11-22 11:42', 'end_date': '2023-11-22 12:12', 'text': '#1 craniospinal - english', 'subject': 'english'},
{'id': 'english1', 'start_date': '2023-11-23 11:42', 'end_date': '2023-11-23 12:12', 'text': '#2 craniospinal - english', 'subject': 'english'},
{'id': 'english2', 'start_date': '2023-11-24 11:42', 'end_date': '2023-11-24 12:12', 'text': '#3 craniospinal - english', 'subject': 'english'},
{'id': 'junction0', 'start_date': '2023-11-21 08:00', 'end_date': '2023-11-21 08:12', 'text': '#1 breast - junction', 'subject': 'junction'},
{'id': 'junction1', 'start_date': '2023-11-22 08:00', 'end_date': '2023-11-22 08:12', 'text': '#2 breast - junction', 'subject': 'junction'},
{'id': 'hungarian0', 'start_date': '2023-11-23 08:12', 'end_date': '2023-11-23 08:24', 'text': '#1 abdomen - hungarian', 'subject': 'hungarian'},
{'id': 'hungarian1', 'start_date': '2023-11-24 08:12', 'end_date': '2023-11-24 08:24', 'text': '#2 abdomen - hungarian', 'subject': 'hungarian'},
"""
    with open('new_treatments.txt', 'w') as f:
        f.write(empty)
    response = RedirectResponse(url='http://localhost:8080/')
    return response




@app.get("/add/")
async def read_item(case: str = 'craniospinal', num: int = 10, identifier: str = 'def1'):

    task= [case, num, identifier]

    # dictionary for different cases
    map_dict = {'craniospinal': {'machines':[ 'TB1','TB2'],
                                'duration':30,
                                'prob': 0.01},
                'breast':{'machines':['TB1','TB2','VB1','VB2','U'],
                        'duration':12,
                        'prob':0.25},
                'breast_special':{'machines':['TB1','TB2'],
                                'duration':20,
                                'prob':0.05},
                'head_neck':{'machines':['TB1','TB2','VB1','VB2'],
                            'duration':12,
                            'prob':0.1},
                'abdomen':{'machines':['TB1','TB2','VB1','VB2'],
                        'duration': 12,
                        'prob':0.1}
    }

    # time per day in minutes
    time_per_day =480

    # starting time
    starting_time = 8

    try:
        TB1 = np.load('TB1.npy')
        TB2 = np.load('TB2.npy')
        VB1 = np.load('VB1.npy')
        VB2 = np.load('VB2.npy')
        U = np.load('U.npy')
    except:
        # define available machines
        TB1= np.zeros([time_per_day,100])
        TB2= np.zeros([time_per_day,100])
        VB1= np.zeros([time_per_day,100])
        VB2= np.zeros([time_per_day,100])
        U= np.zeros([time_per_day,100])

    machine_dict = {'TB1': TB1, 'TB2': TB2, 'VB1': VB1,'VB2':VB2, 'U':U}

    def add_treatment(task):   

        # get number of required visits
        num_treatments = int(task[1])
        #print(task[0])
        #print(map_dict[task[0]])
        #exit()
        # get possible machines
        possible_machines =  {key: machine_dict[key] for key in map_dict[task[0]]['machines']}
        # get first possible starting date

        # get start time for date
        current_datetime = pd.Timestamp.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day

        # add up all matrices
        workload = np.empty([time_per_day,100])
        for machine in possible_machines.values():
            workload = workload+machine

        # get required duration
        duration =map_dict[task[0]]['duration']
        # get days where we still have that time frame free
        workload_bool = workload.sum(axis=0) < (time_per_day-duration)

        # get first possible start day
        start_day = np.where(np.convolve(workload_bool, np.ones(num_treatments), mode='valid') == num_treatments)[0][0]
        #print(type(start_day))
        #exit()
        entries = list()
        # schedule for each day for the machine which has the most time free still
        for treatment in range(num_treatments):
            # calculate date from today
            treatment_day = start_day + treatment
            # check which machine has the most free time
            starts ={}
            for machine,schedule in possible_machines.items():
                # get schedule for the day
                machine_day = schedule[:,treatment_day]
                # get first possible starting time
                #print(machine_day)
                first_start = np.where(machine_day == 0)[0][0]
                #first_start =list({key: value for key, value in starts.items() if value == min_val}.keys())[0]
                starts[machine] = first_start
            # get first available machine for that day
            chosen_machine = min(starts, key=starts.get)
            # assign treatment to that machine
            machine_dict[chosen_machine][starts[chosen_machine]:starts[chosen_machine]+duration,treatment_day] = 1
            
            # create entry
            # we need unique ids for the javascript, hence we generate a random prefix for each id:
            random_prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            entry = {"id":random_prefix + task[2] + str(treatment), "start_date": (datetime.datetime(year, month, day, starting_time, 0, 0)+  pd.Timedelta(days=treatment_day)+pd.Timedelta(minutes=starts[chosen_machine])).strftime("%Y-%m-%d %H:%M"),\
                  "end_date": (datetime.datetime(year, month, day, starting_time, 0, 0)+pd.Timedelta(days=treatment_day)+  pd.Timedelta(minutes=starts[chosen_machine]+duration)).strftime("%Y-%m-%d %H:%M"), "text": "#"+str(treatment+1)+" "+task[0]+" - " + task[2], "subject": task[2]}
            entries.append(entry)
            #print('Day:', treatment_day)
            #print('Machine: ', chosen_machine)
            #print('Starting Time',starts[chosen_machine])
            #print('End Time:', starts[chosen_machine]+duration)
        np.save('TB1',TB1)
        np.save('TB2',TB2)
        np.save('VB1',VB1)
        np.save('VB2',VB2)
        np.save('U',U)


        return(entries)




    # we save the data (just in case)
    out = add_treatment(task)
    with open('new_treatments.txt', 'a') as f:
        for item in out:
            # write each item on a new line
            f.write("%s,\n" % item)

    #print(out)

    response = RedirectResponse(url='http://localhost:8080/')
    return response
    #return out