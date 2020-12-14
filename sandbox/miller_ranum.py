"""
Code snippets from:
Miller, Bradley N., and David L. Ranum. Problem Solving with Algorithms and Data Structures Using Python Wilsonville, OR: Franklin, Beedle & Associates, 2005.

**I did not write this code. I am using it to help my analysis and to practice the Python syntax of creating a class, which I have never done before**
"""
import random


class Queue:
    """
    Adapted from Miller and Ranum. Create a "First In, First Out" data structure.
    """
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Session:
    """
   Adapted from Miller and Ranum.
    """
    def __init__(self, time):
        self.timestamp = time
        self.session_length = 1

    def getStamp(self):
        return self.timestamp

    def getSessionLength(self):
        return self.session_length

    def waitTime(self, current_time):
        return current_time - self.timestamp


def new_person():
    """
    Adapted from Miller and Ranum.
    """
    num = random.randrange(1, 30)  # 1 in 30 chance of yes
    if num == 2:
        return True
    else:
        return False
