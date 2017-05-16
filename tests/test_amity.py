# coding=utf-8
import os
import unittest
import sqlite3

from amity.amity import Amity
from amity.person import Person
from amity.room import Room

class TestAmity(unittest.TestCase):
    """
    Tests the amity system core functions
    """
    def setUp(self):
        self.amity = Amity()

    def test_create_room(self):
        """Tests that amity creates rooms of either office or living space"""
        self.assertIn("created successfully", self.amity.create_room(["earth"], "office"))

    def test_amity_does_not_create_duplicte_rooms(self):
        """Test that amity does not create duplicate rooms"""
        self.amity.create_room(["void"], "office")
        response = self.amity.create_room(["void"], "livingspace")
        self.assertEqual(1, len(self.amity.rooms))

    def test_add_person(self):
        """Test that amity can add a person to a the amity system"""
        role = "FELLOW"
        name = "SAKAZUKI AKAINO"
        accommodate = "Y"
        response = self.amity.add_person(role, name, accommodate)
        self.assertIn("has been added successfully to the system", response)

    def test_add_person_allocates_rooms(self):
        """Test that when a person is added to a room the person is allocated a room"""
        self.amity.create_room(["mars"], "office")
        self.amity.create_room(["earth"], "livingspace")
        response = self.amity.add_person("fellow", "monkey luffy", "y")
        self.assertIn("successfully", response)

    def test_add_person_staff_cannot_be_allocated_livingspace(self):
        """Tests that a staff member can not be allocated to a living space"""
        self.amity.create_room(["pluto"], "livingspace")
        response = self.amity.add_person("staff", "Sakazuki Akainu", "Y")
        self.assertIn("staff can not be allocated accommodation", response)

    def test_add_person_cannot_allocate_person_to_a_full_room(self):
        """Tests that amity does not add people to full rooms"""
        self.amity.create_room(["jupiter"], "office")
        self.amity.add_person("staff", "Monkey Garp")
        self.amity.add_person("staff", "Kuzan Aokiji")
        self.amity.add_person("staff", "Bosalino Kizaru")
        self.amity.add_person("staff", "Monkey Dragon")
        self.amity.add_person("staff", "Sakazuki Akainu")
        self.amity.add_person("staff", "shem ogumbe")
        response = self.amity.add_person("staff", "nico robin")
        self.assertIn("unallocated", response)

    def test_add_person_allocates_accommodation(self):
        role = "FELLOW"
        name = "SAKAZUKI AKAINO"
        accommodate = "Y"
        self.amity.create_room(["mars"], "livingspace")
        response = self.amity.add_person(role, name, accommodate)
        self.assertIn("successfully", response)

    def test_unallocated_person(self):
        """Tests that people that have not been allocated space are stored somewhere"""

        response = self.amity.add_person("staff", "Kuzan Aokiji")
        self.assertIn("unallocated", response)

    def test_reallocate_person(self):
        """Test that amity can reallocate people to other rooms"""
        self.amity.create_room(["venus"], "livingspace")
        id_no = self.amity.get_person_id("Daniel Sumba")
        response = self.amity.reallocate_person(id_no, "venus")
        self.assertIn("has been successfully moved", response)

    def test_print_room(self):
        response = self.amity.print_room("void")
        self.assertIn("VOID", response)

    def test_get_person_id(self):
        self.amity.add_person("FELLOW", "SOGEKING USSOP", "Y")
        response = self.amity.get_person_id("SOGEKING USSOP")
        self.assertIn("SOGEKING USSOP", response)

    def test_print_room_empty_room(self):
        self.amity.create_room(["JUPITER"], "livingspace")
        response = self.amity.print_room("jupiter")
        self.assertIn("is empty", response)

    def test_print_unallocated(self):
        """The that amity output to a file and that the file exists"""
        self.amity.add_person("staff", "Bosalino Kizaru")
        self.amity.add_person("staff", "Monkey Dragon")
        self.amity.add_person("staff", "Sakazuki Akainu")
        self.amity.add_person("staff", "shem ogumbe")
        response = self.amity.print_unallocated()
        self.assertIn("UNALLOCATED", response)

    def test_load_people(self):
        """Test that amity can add people from a .txt file"""
        response = self.amity.load_people("people.txt")
        self.assertIn("successfully", response)

    def test_save_state(self):
        response = self.amity.save_state("test.db")
        self.assertIn("Records created successfully!", response)

    def test_load_state(self):
        database_name = "test.db"
        self.amity.load_state(database_name)
        self.assertIn("app data successfully loaded", self.amity.load_state(database_name))

    def test_print_allocations(self):
        self.amity.create_room(["jupiter"], "offices")
        self.amity.add_person("staff", "Bosalino Kizaru")
        self.amity.add_person("staff", "Monkey Dragon")
        self.amity.add_person("staff", "Sakazuki Akainu")
        self.amity.add_person("staff", "shem ogumbe")
        response = self.amity.print_allocations()
        self.assertIn("ROOM ALLOCATIONS", response)

    def tearDown(self):
        self.amity = None

if __name__ == '__main__':
    unittest.main()