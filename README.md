[![Coverage Status](https://coveralls.io/repos/github/Andela-Sumba/CP1-amity/badge.svg?branch=develop)](https://coveralls.io/github/Andela-Sumba/CP1-amity?branch=develop)

# Amity Space Allocation

Amity is a Python Console Application manages 
Andela's facilities called Amity. Amity creates rooms which can be offices or living spaces. An office has maximum of 6 people allocated to it. A living space can accommodate maximum of 4 people.Amity also creates and allocates a person rooms. A person to be allocated could be a fellow or staff. Staff cannot be allocated livingspaces. Fellows have a choice to choose a living space or not.
This system will be used to automatically allocate spaces to andela employee

### Installation
Clone this repo:
```https://github.com/Andela-Sumba/CP1-amity.git```

Navigate to the CP1-amity directory
```$ cd CP1-amity```

Create a vitual environment:
https://virtualenv.pypa.io/en/stable/userguide/

install packages:

```$ pip install -r requirements.txt```

### Testing

Run tests using the following command:

```$ nosetests --verbose```

### Usage
to launch the app go to your terminal and enter the following command:
```$python app.py -i```


### Help
To get started, type 'help' to see a list of available commands

#### Create room
```Usage: create_room <room_name>... [--ls | --o]```
This command creates rooms in Amity. By default, this method will create an office/offices unless '--ls' is specified 

### Add person
```Usage: add_person <role> <firstname> <surname> [<accommodate>]```
The ```<role>``` argument specifies the role of the person being added which can either be 'Fellow' or 'Staff'.

The ```<accommodate>``` argument tells the system whether or not the person being added wants a room or not. It only accepts 'Y' or 'N' characters which stand for 'Yes' or 'No' respectively. It is an optional argument and its default value is 'N'.

#### Get Person's ID 
```Usage: get_id <firstname> <surname>```
This command gets the person's unique identification number that is important when reallocating the person

### Reallocate Person
```Usage: reallocate_person <id_no> <room_name>```
This command reallocates a person to a new room or different room the command take ```<id_no>```, unique identifier for people in amity ```<room_name>```: name of the room to be reallocated to

### Load People
```usage: load_people <filename>```
This command loads people to amity from a txt file ```<filename>```

### Print allocations
```usage: print_allocations [--o=filename]```
This command prints out all the allocations done by amity and saves them to a text file using the argument ```[--o=filename]```

### Print Unallocations
```usage: print_unallocated [--o=filename]```
This command prints out all unallocated people in amity and also save the output to a text file using the argument ```[--o=filename]```

### Print Room
```usage: print_room <room_name>```
This command prints out all the members of the room specified ```<room_name>```

### Save State
```usage: save_state [--db=sqlite_database]```
This command saves all the data in amity to a database. By default the app save to the database ```amity.db``` but can be specified using ```[--db=sqlite_database]```

### Load State
```usage: load_state [--db=sqlite_database]```
This command load saved data from a specified database, by default the database is ```amity.db``` but can be specified using ```[--db=sqlite_database]```


