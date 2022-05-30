from re import L
import threading
from threading import Event, Thread
import time
# check_calls = 0

# def check_every_2(in_game_condition):
#     threading.Timer(2, check_every_2).start()
#     check_calls += 1
#     if check_calls == 5:
#         in_game_condition.clear()


# in_game_condition = Event()
# check_every_2(in_game_condition)
# it = 0

# def busy_wait(in_game_condition):

#     while in_game_condition.is_set():
#         print("busy waiting...")

# while in_game_condition.is_set():
#     it += 1
#     print(it)
#     busy_wait(in_game_condition)

condition = Event()
condition.set()

def check_condition(condition):
    threading.Timer(2.0, check_condition, args=[condition]).start()
    print("condition set: " + str(condition.is_set()))

def printit():
    threading.Timer(2.0, printit).start()
    print("printit!")

check_condition(condition)

while True:
    print("busy waiting...")
    time.sleep(0.5)