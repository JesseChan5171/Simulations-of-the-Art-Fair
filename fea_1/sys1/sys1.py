import numpy as np
import pandas as pd
import scipy.linalg as la
from numpy.linalg import matrix_power
import matplotlib.pyplot as plt
import heapq
import sys
import random
import math
from datetime import datetime, timedelta
import ast

# the object for Student(Customer)
class Student:
    # key is ID, 0-based
    # constructor
    def __init__(self, ID):
        self.ID = ID
        self.arrival_time_record = []
        self.preference_record = []

    # setter for arrival_time
    def set_arrival_time(self, arrival_time):
        self.arrival_time = arrival_time
        self.arrival_time_record.append(arrival_time)

        # setter for preference

    def set_preference(self, preference):
        self.preference = preference
        self.preference_record.append(preference)

    def __lt__(self, other):
        return self.ID < other.ID

    # used in initialization at the beginning of each day
    def retrieve_arrival_time_and_preference(self, day):
        self.arrival_time = self.arrival_time_record[day - 1]
        self.preference = self.preference_record[day - 1].copy()
        self.is_arrived = False
        self.next_event_time = self.arrival_time
        self.next_event_type = "arrival"
        self.is_departed = False


# the object for Booth(Server)
class Booth:
    # key is ID, 0-based
    # constructor
    def __init__(self, ID, service_time):
        self.idle = True
        self.ID = ID
        self.service_time = service_time
        self.serving = -1
        self.next_event_time = 0
        self.booth_queue = []

    # When a student comes in front of this booth
    def set_busy(self, sID, arrival_time):
        if self.idle:
            self.idle = False
            self.serving = sID
            self.next_event_time = arrival_time + self.service_time
        else:
            self.booth_queue.append((sID, arrival_time))

    # When a student depart from this booth, set_next() method is called
    # The purpose is either moving next student to the boost, or set booth to idle
    # This method returns the waiting time of the next student
    # TODO: Task 1 - calculate the waiting time of the student
    def set_next(self):
        waiting_time = 0

        if len(self.booth_queue) > 0:
            item = self.booth_queue.pop(0)
            self.serving = item[0]
            self.next_event_time = self.next_event_time + self.service_time
            self.idle = False
            #if len(self.booth_queue) == 0:
               # return 0
            #waiting_time = self.next_event_time - self.booth_queue[0][1]
            waiting_time = (self.next_event_time-self.service_time) - item[1]
            return waiting_time

        self.idle = True
        self.serving = -1
        return waiting_time

    # When a student comes in front of this booth, and this booth is busy
    def enqueue_student(self, sID, arrival_time):
        self.booth_queue.append((sID, arrival_time))

    # used in initialization at the beginning of each day
    def reset(self):
        self.idle = True
        self.next_event_time = 0
        self.serving = -1
        self.booth_queue = []


# Function for calculating the travelling time between two booths, or one booth to exit/entrance
# TODO: Task 2 - implement traveling_time function
def traveling_time(location1, location2, n=20):
    tr_t = 0.0
    location1 = int(location1)
    location2 = int(float(location2))

    # Booth to booth

    tr_t = abs(math.floor((location2 + 1 + 1) / 2) - math.floor((location1 + 1 + 1) / 2))

    return tr_t


# Convert time (in min) back to string format
# for example, 121 time unit = 2hr + 1min, means "13:01"
# You should return "24:983" instead of "24:983" in this example
# TODO: Task 3 - implement the string formating function for time
def change_to_time_format(value):
    value = int(value)
    for_t = ''
    init = "11:00"
    date_format_str = '%H:%M'

    init_time = datetime.strptime(init, date_format_str)
    new_t = init_time + timedelta(minutes=value)

    cu_min = '{0:02d}'.format(int(new_t.minute))
    str_t = str(new_t.hour) + ':' + str(cu_min)
    return str_t


# initialize both customers and servers at the beginning of each day
def initialization(student_list, booth_list, current_day):
    # reset student and booth

    for tmp_student in student_list:
        tmp_student.retrieve_arrival_time_and_preference(current_day)

    for tmp_booth in booth_list:
        tmp_booth.reset()

    return student_list, booth_list


# determine time of next event
def timing_routine(student_list, booth_list, current_time, termination_time, total_booth):
    # time of next event can depend on arrival
    min_student_time = termination_time * 100
    for tmp_student in student_list:
        min_student_time = min(min_student_time, tmp_student.next_event_time)

    # time of next event can depend on booth
    min_booth_time = termination_time * 100
    for tmp_booth in booth_list:
        if not tmp_booth.idle:
            min_booth_time = min(min_booth_time, tmp_booth.next_event_time)

    debug = True
    if debug:
        if min_student_time < min_booth_time:
            print("student task")
        elif min_student_time > min_booth_time:
            print("booth task")
        else:
            print("both task")

    # advance to the time
    current_time = min(min_student_time, min_booth_time)

    return current_time


# extract and evaulate all jobs happens at current time
# TODO: Task 4 - complete the traveling time consideration in the simulation
# TODO: Task 5 - complete the simulation log, all departure events (both booths and Art Fair) are missing
# TODO: Task 6 - calculate waiting time, traveling time and tour time
def call_event(student_list, booth_list, current_day, current_time, termination_time, total_booth, simulation_log):
    current_waiting_time = 0
    current_traveling_time = 0
    current_tour_time = 0

    # student events
    # the idea is to use a state machine
    # "arrival" -> "traveling" -> "waiting" <-> "traveling" -> "depart"
    for tmp_student in student_list:
        if tmp_student.next_event_time == current_time:
            if tmp_student.next_event_type == "arrival":
                datum = {"Day": current_day, "Time": change_to_time_format(current_time),
                         "Event": "Student " + str(tmp_student.ID + 1) + " arrives Art Fair", "len(Queue)": "NA"}
                simulation_log = simulation_log.append(datum, ignore_index=True)
                tmp_student.next_event_time = current_time + math.floor((int(tmp_student.preference[0])+1 + 1) / 2)
                tmp_student.next_event_type = "traveling"
                current_traveling_time += math.floor((int(tmp_student.preference[0])+1 + 1) / 2)
            elif tmp_student.next_event_type == "traveling":
                target_booth = tmp_student.preference.pop(0)
                datum = {"Day": current_day, "Time": change_to_time_format(current_time),
                         "Event": "Student " + str(tmp_student.ID + 1) + " arrives at booth " + str(target_booth + 1),
                         "len(Queue)": str(len(booth_list[target_booth].booth_queue) + 1)}
                simulation_log = simulation_log.append(datum, ignore_index=True)
                booth_list[target_booth].enqueue_student(tmp_student.ID, current_time)
                current_tour_time += booth_list[target_booth].service_time
                tmp_student.next_event_time = termination_time * 100
                tmp_student.next_event_type = "waiting"
            elif tmp_student.next_event_type == "waiting":
                tmp_student.next_event_time = termination_time * 100
            elif tmp_student.next_event_type == "departure":
                tmp_student.next_event_time = termination_time * 100
                tmp_student.is_departed = True
                if change_to_time_format(current_time) == "15:00":
                    # print("A")
                    pass
                datum = {"Day": current_day, "Time": change_to_time_format(current_time),
                         "Event": "Student " + str(
                             int(tmp_student.ID) + 1) + " departs Art Fair", "len(Queue)": "NA"}
                simulation_log = simulation_log.append(datum, ignore_index=True)
                tmp_student.next_event_type = "none"

    # booth events
    for tmp_booth in booth_list:
        if tmp_booth.idle and len(tmp_booth.booth_queue) > 0:
            tmp_booth.next_event_time = current_time
            tmp_booth.set_next()


        elif not tmp_booth.idle and tmp_booth.next_event_time == current_time:
            if len(student_list[tmp_booth.serving].preference) == 0:
                student_list[tmp_booth.serving].next_event_type = "departure"
                sh_dis = 0
                to_sc = math.floor((n - (tmp_booth.ID + 1) + 2) / 2.0)
                to_lib = math.floor((int(tmp_booth.ID)+1 + 1) / 2)

                if to_sc > to_lib:
                    sh_dis = to_lib

                else:
                    sh_dis = to_sc

                student_list[tmp_booth.serving].next_event_time = current_time + sh_dis
                datum_bd = {"Day": current_day, "Time": change_to_time_format(current_time),
                         "Event": "Student " + str(
                             int(student_list[tmp_booth.serving].ID) + 1) + " departs at booth " + str(tmp_booth.ID+1), "len(Queue)": str(len(tmp_booth.booth_queue))}
                simulation_log = simulation_log.append(datum_bd, ignore_index=True)
                current_traveling_time += sh_dis
            else:

                student_list[tmp_booth.serving].next_event_type = "traveling"
                student_list[tmp_booth.serving].next_event_time = current_time + traveling_time(tmp_booth.ID,
                                                                                                student_list[
                                                                                                    tmp_booth.serving].preference[
                                                                                                    0])
                datum_bt = {"Day": current_day, "Time": change_to_time_format(current_time),
                         "Event": "Student " + str(student_list[tmp_booth.serving].ID + 1) + " departs at booth " + str(
                             tmp_booth.ID + 1), "len(Queue)": str(len(tmp_booth.booth_queue))}
                simulation_log = simulation_log.append(datum_bt, ignore_index=True)

                current_traveling_time += traveling_time(tmp_booth.ID, student_list[tmp_booth.serving].preference[0])
            current_waiting_time += tmp_booth.set_next()
    current_tour_time += (current_waiting_time + current_traveling_time)


    return student_list, booth_list, simulation_log, current_waiting_time, current_traveling_time, current_tour_time


# output student record to a csv file
# pay attention: you need to change the 0-based numbers to 1-based numbers in the output
# TODO: Task 7 - output of preference lists are missing
def output_student(student_list, student_file, D):
    header_list = ["student_id"]
    for i in np.arange(D):
        header_list.append("arrival_time_day_" + str(i + 1))
    for i in np.arange(D):
        header_list.append("preference_day_" + str(i + 1))
    record_student = pd.DataFrame([], columns=header_list)

    for tmp_student in student_list:
        student_dict = {"student_id": tmp_student.ID + 1}

        for i in np.arange(D):
            student_dict["arrival_time_day_" + str(i + 1)] = change_to_time_format(tmp_student.arrival_time_record[i])
            student_dict["preference_day_" + str(i + 1)] = str([x+1 for x in tmp_student.preference_record[i]])

        record_student = record_student.append(student_dict, ignore_index=True)

    record_student.to_csv(student_file, index=False)


# output config to a csv file
# TODO: Task 8 - complete the config file
def output_config(D, n, N, Booth_promotion_time, config_file, student_file, log_file, summary_file):
    header_list = ["ColA", "ColB"]
    record_config = pd.DataFrame([], columns=header_list)

    col_a_ls = ["D", "n", "N", "Booth_promotion_time", "Student_file", "Log_file", "Summary_file"]
    col_b_ls = [str(D), str(n), str(N), str(Booth_promotion_time), str(student_file), str(log_file), str(summary_file)]

    for col_a, col_b in zip(col_a_ls, col_b_ls):
        record_config = record_config.append({"ColA": col_a, "ColB": col_b}, ignore_index=True)

    record_config.to_csv(config_file, index=False, header=False)

def traveling_time2(location1, location2, n):
    if str(location2) == "Library":
        return math.floor((location1+1)/2)


def sort_preference(preference_list):
    dist = lambda booth_id: traveling_time2("Library", booth_id + 1, n)
    preference_list = sorted(preference_list, key=dist)
    return preference_list

def reo_eas (pref_ls):
    return sorted(pref_ls)

# main program
curr_time = 0
isFileInput = False
student_list = []

if len(sys.argv) == 2 and len(sys.argv[1]) > 3:
    # initialization with a config file

    isFileInput = True
    config = pd.read_csv(sys.argv[1], header=None, index_col=0, skip_blank_lines=True)
    print(config)

    D = int(config[1].D)
    n = int(config[1].n)
    N = int(config[1].N)
    Booth_promotion_time = list(map(int, config[1].Booth_promotion_time.split("[")[1].split("]")[0].split(",")))
    student_file = config[1].Student_file
    log_file = config[1].Log_file
    summary_file = config[1].Summary_file

    student_df = pd.read_csv(student_file, header=0, skip_blank_lines=True)

    # retrive the data from student_df(dataframe) to student_list(list of student objects)
    # pay attention: all numbers in the dataframe are 1-based, you need to change them back to 0-based
    # TODO: Task 9 - retrive the preference list, from string to list of ints
    # For example: (dataframe) "[1, 2, 3]" -> (list of int) [0, 1, 2]
    for ind, row in student_df.iterrows():
        tmp_student = Student(row["student_id"] - 1)
        for d in np.arange(D):
            s = row["arrival_time_day_" + str(d + 1)].split(":")
            tmp_student.set_arrival_time((int(s[0]) - 11) * 60 + int(s[1]))
            s_2 = row["preference_day_" + str(d + 1)]

            one_base_list = list(map(int, row["preference_day_"+str(d+1)].split("[")[1].split("]")[0].split(",")))
            tmp_student.set_preference([x-1 for x in one_base_list])


            # tmp_student.set_preference(s_2_0)
        student_list.append(tmp_student)


else :
    # initialization with random numbers
    # get the seed set
    print(sys.argv[1])
    i_seed = int(sys.argv[1])
    D = 2
    n = 20
    N = 100
    Booth_promotion_time = []
    config_file = f"config_default_random{i_seed}.csv"
    student_file = f"student_default_random{i_seed}.csv"
    log_file = f"simulation_log{i_seed}.csv"
    summary_file = f"simulation_summary{i_seed}.csv"

    # generate DN arrival time for the students
    np.random.seed(i_seed)
    sid = 0
    while sid < N:
        tmp_student = Student(sid)
        i = 0
        while i < D:
            tmp_student.set_arrival_time(int(np.random.uniform(400)))
            i = i + 1
        student_list.append(tmp_student)
        sid = sid + 1

    # generate DN list of distinct integers as the preference of the students
    # TODO: Task 10 - generate the preference lists
    np.random.seed(i_seed+1)
    random.seed(i_seed+1)
    for tmp_student in student_list:
        i = 0
        while i < D:
            preference = []
            ran_p = min(np.random.uniform(5) + 1, n)
            while len(preference) < ran_p:
                dis_int = random.randint(0, n-1)
                if dis_int not in preference:
                    preference.append(dis_int)
            preference = reo_eas(preference)
            tmp_student.set_preference(preference)
            i = i + 1

    # generate n numbers as the promotion time of the booths
    # TODO: Task 11 - generate the promotion time
    np.random.seed(i_seed+2)
    i = 0
    while i < n:
        Booth_promotion_time.append(int(min((1+np.random.exponential(5)),10)))
        i = i + 1

# main simulation
# initialization before simulation
termination_time = 420
current_day = 1
booth_list = []
bid = 0
# create the list of booth objects
for promotion_time in Booth_promotion_time:
    new_booth = Booth(bid, promotion_time)
    booth_list.append(new_booth)
    bid = bid + 1

simulation_log = pd.DataFrame([], columns=["Day", "Time", "Event", "len(Queue)"])
simulation_summary = pd.DataFrame([], columns=["Day", "TotalWaitingTime", "TotalTravelingTime", "TotalTourTime"])

debug = True
total_day_wait = 0
while current_day <= D:

    # initialization for a day in the simulation
    student_list, booth_list = initialization(student_list, booth_list, current_day)
    current_time = 0
    is_system_clear = True
    total_waiting_time = 0
    total_traveling_time = 0
    total_tour_time = 0

    while current_time < termination_time or not is_system_clear:

        if debug:
            # print(current_time)
            print(change_to_time_format(current_time))

        # determine the time
        current_time = timing_routine(student_list, booth_list, current_time, termination_time, n)

        # update different lists and log sheet
        student_list, booth_list, simulation_log, current_waiting_time, current_traveling_time, current_tour_time = call_event(
            student_list, booth_list, current_day, current_time, termination_time, n, simulation_log)

        # check if Art Fair is clear
        # TODO: Task 12 - determine the condition for all students departing from the Art Fair
        #is_system_clear = True

        count_T = 0
        for std in student_list:
            if std.is_departed == False:
                is_system_clear = False
                break
            elif std.is_departed == True:
                count_T += 1

        if count_T == len(student_list):
            is_system_clear = True

        # if time's up, clear student's preference list when they are in the waiting queue of booths
        if current_time > termination_time:
            for tmp_student in student_list:
                if tmp_student.next_event_type == "waiting":
                    tmp_student.preference = []

        # statistics meausre update, used in the summary
        total_waiting_time = total_waiting_time + current_waiting_time
        total_traveling_time = total_traveling_time + current_traveling_time
        total_tour_time = total_tour_time + current_tour_time



    # at the end of each day, append a row of statistics to the summary file
    datum = {"Day": current_day, "TotalWaitingTime": total_waiting_time, "TotalTravelingTime": total_traveling_time,
             "TotalTourTime": total_tour_time}
    simulation_summary = simulation_summary.append(datum, ignore_index=True)
    current_day = current_day + 1
    total_day_wait += total_waiting_time

# output statistics
if not isFileInput:
    # output student record to student_file
    output_student(student_list, student_file, D)
    # output config file to config_file
    output_config(D, n, N, Booth_promotion_time, config_file, student_file, log_file, summary_file)

simulation_log.to_csv(log_file, index=False)
simulation_summary.to_csv(summary_file, index=False)

with open('tot_w.txt', 'a') as f:
    print(total_day_wait, file=f)
