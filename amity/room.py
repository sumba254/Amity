from abc import ABCMeta
from abc import abstractmethod


class Room(object):
    """
        Class: Room
        -----------
        The room class is a super class that handles the creation of Rooms
        in the amity application. Relies on the information it gets from
        the child classes LivingSpace and Office
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, room_name, room_type, capacity):
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity


class Office(Room):
    """
        Class: Office
        _____________
        class Office is child class that inherits from the Person class.
        it contains the specific attributes related to a room of type office
    """

    def __init__(self, room_name):
        super(Office, self).__init__(room_name, "office", capacity=6)


class LivingSpace(Room):
    """
        Class: LivingSpace
        __________________
        class LivingSpace is child class that inherits from the Person class.
        it contains the specific attributes related to a room of type LivingSpace
    """

    def __init__(self, room_name):
        super(LivingSpace, self).__init__(room_name, "livingspace", capacity=4)
