#!/usr/bin/env python
"""
Welcome to Amity Commandline App
Amity is a simple Commandline room alloaction application
Usage:
    app.py create_room <room_name>...[--ls|--o]
    app.py add_person <role> <firstname> <surname> [<Accomodation>]
    app.py (-i | --interactive)
    app.py (-h | --help)
    app.py (-v | --version)
    app.py quit

arguments:
    <room_name>         Unique name for them Room to be created or querried
    <role>              The role of the Person being added i.e. Fellow or Staff
    <firstname>         First name of the Person
    <surname>           The surname of the Person
    <Accomodation>      Whether Person wants accomodation or not i.e 'N' or 'Y'

Options:
    -i --interactive        Interactive Mode
    -h --help               Show this screen and exit
    -v --version
    --ls --LivingSpace
    --o --Office

"""

import os
import sys
import cmd
import signal
from termcolor import cprint, colored
from pyfiglet import figlet_format
from docopt import docopt, DocoptExit

from amity.amity import Amity
from amity.person import Person,Fellow,Staff
from amity.room import Room,LivingSpace,Office


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action
    """
    def fn(self, args):
        try:
            opt = docopt(fn.__doc__, args)
        except DocoptExit as error:
            # The DocoptExit is thrown when the args do not match
            print('The command entered is invalid!')
            print(error)
            return
        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return
        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def app_header():
    """
        This function creates the header that is displayed when the app
        launches
   """
    os.system("clear")
    print("\n")
    cprint(figlet_format('AMITY', font='epic'), 'yellow')
    cprint('--------------------------------------------------------------------------', 'red')
    cprint("\tAmity is a simple Commandline Room Allocation App.", 'yellow')
    cprint('--------------------------------------------------------------------------', 'red')
    cprint("\n\tType 'help' to see a full list of commands\n", 'white')


def custom_print(arg, color='green'):
    """ This is a simple print function that adds color to printed output. """
    cprint("\n" + arg + "\n", color)


class AmityCLI(cmd.Cmd):
    """
        This class creates Amity Command Line Interface for user interaction
    """
    app_prompt = colored('Amity => ', 'green', attrs=['bold'])
    prompt = app_prompt

    @docopt_cmd
    def do_add_person(self, args):
        """
        ----------------------------------------------------------------------
        Usage: add_person <role> <firstname> <surname> [<accommodate>]
        """
        role = args['<role>'].upper()
        name = args['<firstname>'].upper()
        name += " " + args['<surname>'].upper()
        if role != "FELLOW" and role != "STAFF":
            print("Please check your arguments."
                  "\n- <role> can either be 'Fellow' or 'Staff' "
                  "only.\n- Type 'help add_person' for more information",
                  'red')
            return
        accommodate = args['<accommodate>'] or 'N'
        accommodate = accommodate.upper()
        if accommodate != 'Y' and accommodate != 'N':
            print("Please check your arguments."
                  "\n- <Accommodate> can either be 'Y' or "
                  "'N' only.\n- Type 'help add_person' for "
                  "more information", 'red')
            return
        print(amity.add_person(role, name, accommodate))

    @docopt_cmd
    def do_create_room(self, args):

        """
        Creates rooms in Amity. Using this command I
        should be able to create as many rooms as possible
        by specifying multiple room
        names after the create_room command.
        -----------------------------------------------------
        Usage: create_room <room_name>... [--ls | --o]
        """
        room_args = []
        for room_name in args["<room_name>"]:
            room_args.append(room_name.upper())
        if args['--ls'] is True:
            room_type = "livingspace"
        elif args['--o'] is True:
            room_type = "office"
        else:
            room_type = "office"
        print(amity.create_room(room_args, room_type))

    @docopt_cmd
    def do_reallocate_person(self, args):
        """
        Reallocate the
        person with the id_no to new_room_name .
        -----------------------------------------------------
        Usage: reallocate_person <id_no> <room_name>
        """
        id_no = args["<id_no>"]
        room_name = args["<room_name>"]
        print(amity.reallocate_person(id_no, room_name))

    @docopt_cmd
    def do_load_people(self, args):
        """
        Adds people to rooms from a text file
        -----------------------------------------------------
        usage: load_people <filename>
        """

        print(amity.load_people(args['<filename>']))

    @docopt_cmd
    def do_print_allocations(self, args):
        """
        Prints a list of allocations onto the screen.
        Specifying the optional -o option here outputs
        the registered allocations to a txt file.
        -----------------------------------------------------
        usage: print_allocations [--o=filename]
        """
        print(amity.print_allocations(args['--o']))

    @docopt_cmd
    def do_print_unallocated(self, args):
        """
        Prints a list of allocations onto the screen.
        Specifying the optional -o option here outputs
        the registered allocations to a txt file
        -----------------------------------------------------
        usage: print_unallocated [--o=filename]
        """
        print(amity.print_unallocated(args['--o']))

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Prints the names of all the people in room_name on the
        screen.
        -----------------------------------------------------
        usage: print_room <room_name>
        """
        print(amity.print_room(arg['<room_name>']))

    @docopt_cmd
    def do_save_state(self, args):
        """
        Persists all the data stored in the app to a
        SQLite database. Specifying the --db parameter explicitly stores the data in the
        SQlite database specified.
        -----------------------------------------------------
        usage: save_state [--db=sqlite_database]
        """
        if not args['--db']:
            args['--db'] = 'amity.db'
        print(amity.save_state(args['--db']))

    @docopt_cmd
    def do_load_state(self, args):
        """
        Loads data from a database into the application.
        -----------------------------------------------------
        usage: load_state [--db=sqlite_database]
        """
        if not args['--db']:
            args['--db'] = 'amity.db'
        print(amity.load_state(args['--db']))

    @docopt_cmd
    def do_get_id(self, args):
        """
        gets the id number that belongs to the person add prints it
       _________________________________________________________
        Usage: get_id <firstname> <surname>
        """
        search_name = args['<firstname>'].upper()
        search_name += " " + args['<surname>'].upper()
        print(amity.get_person_id(search_name))

    def do_quit(self, args):
        """ Quits the interactive mode """
        print("Goodbye!")
        print("Closing Amity...")
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    app_header()
    amity = Amity()
    AmityCLI().cmdloop()
