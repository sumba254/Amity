
import random
from abc import ABCMeta
from abc import abstractmethod


class Person(object):
    """
        class Person:
        ______________
        The Person class is an abstract class that handles the creation of Peopl
        in the amity application. Relies on the information it gets from
        the child classes Fellow and Office
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.id_no = str(random.choice(range(1, 10000000)))


class Fellow(Person):
    """
        Fellow Class
        ________________
        This is a Child Class that inherits from the Person
        Super Class. It passes information to the Parent Constructor
        so as to dictate how the Person is created. It also handles
        other responsibilities related to a Fellow.
    """

    def __init__(self, name):
        super(Fellow, self).__init__(name, "fellow")


class Staff(Person):
    """
        Staff Class
        ________________
        This is a Child Class that inherits from the Person
        Super Class. It passes information to the Parent Constructor
        so as to dictate how the Person is created. It also handles
        other responsibilities related to a Staff.
    """
    def __init__(self, name):
        super(Staff, self).__init__(name, "staff")
