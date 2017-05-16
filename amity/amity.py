# coding=utf-8
import os
import random
import sqlite3
import pickle
import sys

from person import Person, Fellow, Staff
from room import Room, LivingSpace, Office

if os.path.exists('amity'):
    os.chdir('amity')


class Amity(object):
    """
        Amity class:
        ________________________________________________________________________________
        Amity class models a room allocation system for one of
        Andela's facilities called Amity. Amity creates rooms which can
        be offices or living spaces. An office has maximum of 6
        people allocated to it. A living space can accommodate maximum of 4 people.
        Amity also creates and allocates a person rooms. A person to be allocated
        could be a fellow or staff. Staff cannot be allocated living
        spaces. Fellows have a choice to choose a living space or not.
        This system will be used to automatically allocate spaces to
        people at random.

        Data structures:
        ______________________
        rooms(list): contains a list of all rooms in the system
        office(dict): This is a dict of all IDs of offices in the amity system
        accommodations(dict): This is a dict of all IDs of accommodations in the amity system
        employees(dict): This is a dict of all IDs of employees in the amity system
        fellows(dict): This is a dict of all IDs of fellows in the amity system
        staff(dict): This is a dict of all IDs of staff in the amity system
        unallocated(list): This a list of all unallocated people
        allocated(list): List of all allocated people

    """
    def __init__(self):
        self.rooms = []
        self.offices = {}
        self.accommodations = {}
        self.employees = {}
        self.fellows = {}
        self.staff = {}
        self.unallocated = []
        self.allocated = []

    def create_room(self, room_list, room_type):
        """
        create rooms in amity that are either of type offices or accommodations
        ________________________________________________________________________
        :param room_list: the unique list of room names
        :param room_type:
        :return: success message
        """
        zero = 0
        total_rooms = len(self.rooms)
        for name in room_list:
            if name in self.rooms:
                name_index = self.rooms.index(name)
                self.rooms.pop(name_index)
                msg = "\nThe room " + name + " already exists cannot create duplicate rooms\n"
                print(msg)
        if len(room_list) is not zero:
            if room_type == "office":
                if "OFFICE" in room_list:
                    return "to specify the type of room use --o for type office, --ls for livingspace"
                for room_name in room_list:
                    new_office = Office(room_name)
                    self.rooms.append(new_office.room_name)
                    self.offices[new_office.room_name] = []
                new_total_rooms = len(self.rooms)
                if new_total_rooms-total_rooms > 1:
                    return str(new_total_rooms-total_rooms) + " offices have been successfully created"
                else:
                    return " The office has been created successfully!"

            elif room_type == "livingspace":
                if "LIVINGSPACE" in room_list:
                    return "to specify the type of room use --o for type office, --ls for livingspace"
                for room_name in room_list:
                    new_accommodation = LivingSpace(room_name)
                    self.rooms.append(new_accommodation.room_name)
                    self.accommodations[new_accommodation.room_name] = []
                new_total_rooms = len(self.rooms)
                if new_total_rooms - total_rooms > 1:
                    return str(new_total_rooms - total_rooms) + " living spaces have been successfully created"
                else:
                    return "The living space has been created successfully!"
            else:
                for room_name in room_list:
                    new_office = Office(room_name)
                    self.rooms.append(new_office.room_name)
                    self.offices[new_office.room_name] = []
                new_total_rooms = len(self.rooms)
                if new_total_rooms-total_rooms > 1:
                    return str(new_total_rooms-total_rooms) + " offices have been successfully created"
                else:
                    return " The office has been created successfully!"

    def add_person(self, role, name, accommodate="N"):
        """
        adds people to amity that are either fellows or staff and the person has
        a choice to either want accommodation or not
        __________________________________________________________________________
        :param name: name of the person to be added to system
        :param role: role of the person in Andela (fellow|staff)
        :param accommodate: Y or N
        :return: success messages that person added successfully, added to office
                 successfully, and added to living space successfully
        """
        self.allocated = False
        if role.upper() == "FELLOW":
            msg = ""
            new_fellow = Fellow(name)
            new_id_no = new_fellow.id_no
            self.employees[new_id_no] = new_fellow.name
            self.fellows[new_id_no] = new_fellow.name
            self.allocate_office(new_id_no)

            if accommodate == "Y":
                self.allocate_accommodation(new_id_no)

            if not self.allocated:
                self.unallocated.append(new_id_no)
                msg += "added to unallocated list\n"

            if new_id_no in self.employees.keys() and self.fellows.keys():
                msg += "The fellow " + new_fellow.name + " has been added successfully to the system\n"
            else:
                msg = "error!!! person not add properly\n"
            return msg

        elif role.upper() == "STAFF":
            msg = ""
            new_staff = Staff(name)
            new_id_no = new_staff.id_no
            self.employees[new_id_no] = new_staff.name
            self.staff[new_id_no] = new_staff.name
            self.allocate_office(new_id_no)

            if accommodate == "Y":  # check that amity does not allocate staff accommodation
                msg += "staff can not be allocated accommodation\n"

            if not self.allocated:
                self.unallocated.append(new_id_no)
                msg += "add to unallocated list\n"

            if new_id_no in self.employees.keys() and self.staff.keys():
                msg += "The staff " + new_staff.name + " has been added successfully to the system\n"
            else:
                msg = "error!!! person not add properly\n"
            return msg

        else:
            return "Please specify the persons role\n"

    def allocate_office(self, new_id_no):
        """
        Allocates office to staff and fellows
        _______________________________________________________
        :param new_id_no: id number of the person
        :return: success or failure message
        """
        zero = 0
        if len(self.rooms) is zero:
            msg = "The system has no available rooms"
            return msg

        vacant_offices = []
        for room in self.rooms:
            if room in self.offices.keys() and len(self.offices[room]) < 6:
                vacant_offices.append(room)
        if len(vacant_offices) == 0:
            print("The system has no available office space")
            if new_id_no in self.unallocated:
                self.unallocated.append(new_id_no)
        else:
            workspace = random.choice(vacant_offices)
            self.offices[workspace].append(new_id_no)
            self.allocated = True
            if new_id_no in self.offices[workspace]:
                print(self.employees[new_id_no] + " has successfully been allocated the office: " + workspace)

    def allocate_accommodation(self, new_id_no):
        """
        Allocates random living space to fellows only
        ______________________________________________________________________________
        :param new_id_no: id number of fellow being allocated:
        :return: success or failure message
        """
        zero = 0
        if len(self.rooms) is zero:
            msg = "The system has no available rooms"
            return msg

        vacant_accommodation = []
        for room in self.rooms:
            if room in self.accommodations.keys() and len(self.accommodations[room]) < 4:
                vacant_accommodation.append(room)
        if len(vacant_accommodation) == 0:
            print("The system has no available accommodations")
            if new_id_no in self.unallocated:
                self.unallocated.append(new_id_no)
        else:
            workspace = random.choice(vacant_accommodation)
            self.accommodations[workspace].append(new_id_no)
            self.allocated = True
            if new_id_no in self.accommodations[workspace]:
                print(self.employees[new_id_no] + " has successfully been allocated the living space: " + workspace)

    def get_person_id(self, search_name):
        """
        The function receive a search name and prints out the id number of person
        ___________________________________________________________
        :param search_name: Name of person you want to get the id
        :return: prints out id_no of the person being searched
        """
        if search_name not in list(self.employees.values()):
            return "The person is not in system"
        else:
            for id_no, name in self.employees.items():
                if name == search_name:
                    output = "ID: "
                    output += id_no
                    if id_no in self.fellows.keys():
                        output += " ROLE: FELLOW "
                        output += "NAME: " + self.employees[id_no]
                    if id_no in  self.staff.keys():
                        output += " ROLE: STAFF "
                        output += "NAME: " + self.employees[id_no]
                    return output

    def reallocate_person(self, id_no, room_name):
        """
        Reallocates person use the person id number from a certain room to another room
        ______________________________________________________________________________
        :param id_no: unique identifier for the person to be reallocated
        :param room_name: name of the room person to be relocated to
        :return: Success message that person has be successfully reallocate
        """
        vacant_room = []
        new_room = room_name.upper()
        if new_room not in self.rooms:
            return "The room " + new_room + " does not exist in amity"
        if new_room in self.accommodations.keys() and len(self.accommodations[new_room]) < 4:
            vacant_room.append(new_room)
        elif new_room in self.offices.keys() and len(self.offices[new_room]) < 6:
            vacant_room.append(new_room)
        for room in vacant_room:
            if id_no in self.offices[room]:
                return "The person is already allocated to the room"
            if id_no in self.staff.keys():
                if room in self.accommodations.keys():
                    return "Staff can not be allocated a living space"
                else:
                    for saved_room, saved_id_no in self.offices.items():
                        for item in self.offices[saved_room]:
                            if item == id_no:
                                self.offices[saved_room].remove(item)
                    if id_no not in self.offices[room]:
                        self.offices[room].append(id_no)
                    else:
                        return "The person is already allocated to the room"
                    if id_no in self.offices[room]:
                        return self.employees[id_no] + " has been successfully moved to: " + room
            if id_no in self.fellows.keys():
                if room in self.accommodations.keys():
                    if id_no in self.accommodations[room]:
                        return "The person is already allocated to the room"
                    for saved_room, saved_id_no in self.accommodations.items():
                        for item in self.accommodations[saved_room]:
                            if item == id_no:
                                self.accommodations[saved_room].remove(item)
                    if id_no not in self.accommodations[room]:
                        self.accommodations[room].append(id_no)
                    else:
                        return "The person is already allocated to the room"
                    if id_no in self.accommodations[room]:
                        print(self.employees[id_no] + " has been successfully moved to: " + room)
                else:
                    for saved_room, saved_id_no in self.offices.items():
                        for item in self.offices[saved_room]:
                            if item == id_no:
                                self.offices[saved_room].remove(item)
                    self.offices[room].append(id_no)
                    if id_no in self.offices[room]:
                        print(self.employees[id_no] + " has been successfully moved to: " + room)

    def print_room(self, room_name):
        """
        Prints out the members or occupants in the room
        _______________________________________________________________________________
        :param room_name: name of room to print
        :return: prints a list of all occupants in the room
        """
        zero = 0
        print_name = room_name.upper()
        if print_name not in self.rooms:
            return "There is no room " + print_name + " in system!"
        if print_name in list(self.offices.keys()) and len(self.offices[print_name]) is zero:
            return print_name + " is empty!"
        elif print_name in list(self.accommodations.keys()) and len(self.accommodations[print_name]) is zero:
            return print_name + " is empty!"
        else:
            header = "The members of room " + print_name + ":\n"
            header += "------------------------------------------\n"
            print(header)
            if print_name in self.rooms:
                if print_name in list(self.offices.keys()):
                    for item in self.offices[print_name]:
                        print(self.employees[item].upper())
                elif print_name in self.accommodations.keys():
                    for item in self.accommodations[print_name]:
                        print(self.employees[item].upper())

    def load_people(self, textfile):
        """
        Load people from a text file to amity
        ____________________________________________________________________________________
        :param textfile:
        :return:
        """
        if not isinstance(textfile, str):
            return TypeError("Amity on accepts string as input")
        elif textfile is not None:
            if os.path.exists('data/input/' + textfile):
                with open('data/input/' + textfile, 'r') as file:
                    people = file.readlines()
                    for person in people:
                        person_details = person.split()
                        role = person_details[0].upper()
                        name = person_details[1].upper() + " " + person_details[2].upper()
                        if len(person_details) > 3:
                            accommodate = person_details[3].upper()
                        else:
                            accommodate = "N"
                        print(self.add_person(role, name, accommodate))
            else:
                return "The file does not exist!"
        return "People have been successfully loaded to amity!"

    def print_allocations(self, filename=None):
        """
        Prints out list of all people who have been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param filename:
        :return:
        """
        occupied_rooms = []
        output = "ROOM ALLOCATIONS\n"
        for room in self.rooms:
            if room in self.accommodations.keys() and len(self.accommodations[room]) is not 0:
                occupied_rooms.append(room)
            elif room in self.offices.keys() and len(self.offices[room]) is not 0:
                occupied_rooms.append(room)
        if len(occupied_rooms) is 0:
            output = "There are no occupied rooms in amity!\n"
        for room_name in occupied_rooms:
            if room_name in self.accommodations.keys():
                output += "\n"
                output += room_name.upper() + "\n"
                output += "-----------------------------------------------\n"
                for item in self.accommodations[room_name]:
                    output += self.employees[item] + "\n"
            elif room_name in self.offices.keys():
                output += "\n"
                output += room_name.upper() + "\n"
                output += "-----------------------------------------------\n"
                for item in self.offices[room_name]:
                    output += self.employees[item] + "\n"

        if filename is not None:
            with open('data/output/' + filename, 'w') as outfile:
                outfile.write(output)
                return "\nAllocations saved to: {}\n".format(filename)
        return output

    def print_unallocated(self, filename=None):
        """
        Prints out list of all people who have not been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param filename:
        :return:
        """
        if len(self.unallocated) is 0:
            return "\nThere are no unallocated people\n"
        else:
            output = "\nUNALLOCATED PEOPLE\n"
            output += "-------------------------------------\n"
            for item in self.unallocated:
                output += self.employees[item] + "\n"
            if filename is not None:
                with open('data/output/' + filename, 'w') as outfile:
                    outfile.write(output)
                    print("\nAllocations saved to: {}\n".format(filename))
        return output

    def save_state(self, filename=None):  # work in progress
        """
        save all data in amity to a specified database
        _____________________________________________________________________________________
        :param filename:
        :return:
        """
        if filename is not None:
            database_name = filename
        self.conn = sqlite3.connect('data/states/' + database_name)
        self.c = self.conn.cursor()
        self.c.execute("DROP TABLE IF EXISTS EMPLOYEES")
        self.c.execute("DROP TABLE IF EXISTS FELLOWS")
        self.c.execute("DROP TABLE IF EXISTS STAFF")
        self.c.execute("DROP TABLE IF EXISTS ROOMS")
        self.c.execute("DROP TABLE IF EXISTS OFFICES")
        self.c.execute("DROP TABLE IF EXISTS ACCOMMODATIONS")
        self.c.execute("DROP TABLE IF EXISTS STATE")
        self.create_db_table(database_name)

        for person_id in self.employees.keys():
            self.c.execute("INSERT INTO EMPLOYEES(NAME, ID_NO) VALUES(?, ?)", [person_id, self.employees[person_id]])
        self.conn.commit()

        for person_id in self.fellows.keys():
            self.c.execute("INSERT INTO FELLOWS(NAME, ID_NO) VALUES(?, ?)", [person_id, self.fellows[person_id]])
        self.conn.commit()

        for person_id in self.staff.keys():
            self.c.execute("INSERT INTO STAFF(NAME, ID_NO) VALUES(?, ?)", [person_id, self.staff[person_id]])
        self.conn.commit()

        for name in self.rooms:
            self.c.execute("INSERT INTO ROOMS(ROOMNAME) VALUES(?)", [name])
        self.conn.commit()

        for room_name in self.offices.keys():
            self.c.execute("INSERT INTO OFFICES(ROOMNAME, OCCUPANTS) \
                            VALUES(?, ?)", [room_name, str(self.offices[room_name])])
        self.conn.commit()

        for room_name in self.accommodations.keys():
            self.c.execute("INSERT INTO ACCOMMODATIONS(ROOMNAME, OCCUPANTS) \
                              VALUES(?, ?)", [room_name, str(self.accommodations[room_name])])
        self.conn.commit()

        data = (self.rooms, self.offices, self.employees, self.accommodations,
                self.fellows, self.staff, self.allocated, self.unallocated)
        save_data = pickle.dumps(data)
        appdata = sqlite3.Binary(save_data)
        self.c.execute("INSERT INTO STATE(State) VALUES(?)", (appdata,))
        self.conn.commit()
        return "\nRecords created successfully!\n"

    def create_db_table(self, database_name):
        """
        creates a database table
        ______________________________________________
        :param database_name: The name of the database that the tables will be create in
        :return: success message that the tables have been created successfully.
        """
        self.conn = sqlite3.connect('data/states/' + database_name)
        self.c = self.conn.cursor()
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEES
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    NAME           TEXT ,
                                    ID_NO            TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS FELLOWS
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME           TEXT ,
                        ID_NO            TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS STAFF
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    NAME           TEXT ,
                                    ID_NO            TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS ROOMS
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ROOMNAME           TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS OFFICES
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ROOMNAME           TEXT ,
                                        OCCUPANTS            TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS ACCOMMODATIONS
                                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        ROOMNAME           TEXT ,
                                        OCCUPANTS            TEXT);''')

            self.c.execute('''CREATE TABLE IF NOT EXISTS STATE
                            (State BLOB);''')
        except sqlite3.IntegrityError:
            return False

    def load_state(self, filename=None):
        """
        Load application state that was saved in the database
        ___________________________________________________________________________________________________
        :param filename:
        :return:
        """
        if filename is not None:
            database_name = filename
        self.conn = sqlite3.connect('data/states/' + database_name)
        self.c = self.conn.cursor()
        self.c.execute("SELECT State FROM STATE")
        data = self.c.fetchone()[0]
        state = pickle.loads(data)
        self.rooms = state[0]
        self.offices = state[1]
        self.employees = state[2]
        self.accommodations = state[3]
        self.fellows = state[4]
        self.staff = state[5]
        self.allocated = state[6]
        self.unallocated = state[7]
        return "\n app data successfully loaded!\n"
