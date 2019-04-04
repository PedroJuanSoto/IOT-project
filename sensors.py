from postalservice import message, mailbox
from leaderelection import create_edges, find_MST
from berkeley import berkeley_clock_synch

#The temperature sensor is a pull-based sensor, it responds to the gateway by
#sending the current temperature (see line 28).
class thermostat:
    def __init__(self):
        self.offset = 0
        self.name = "temperature"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the tcome_to_life() function
        self.idnum = "wu"            #on line 30, the thermostat registers itself and finds its correct idnum.
        self.state = -1              #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp(self.offset)   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp(self.offset))
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the temperature sensor is a pull-based sensor it mus have an
#implementation of the query_response() function.
    def query_response(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp(self.offset))
        pipeboxes[self.idnum].deliver_mail(self.offset,report)
#tcome_to_life is the function that models the thermostats behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the thermostat will exist, envirobox is the mailbox from which it recieves
#information about the temperature of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def tcome_to_life(self, rbox, life_of_universe, envirobox, pipeboxes, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("thermo",7,clockboxes)
            parent, children, status = find_MST("thermo", neighbors)
            self.time=berkeley_clock_synch("thermo", self.offset, parent, children, status)
        time_until_we_all_die = 0
        self.register_self(rbox)
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_query(self.offset,self.idnum)
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[self.idnum].timestamp(self.offset)
                if x.time > current_time :
                    self.offset = x.time - current_time + 1
            if x.command == "query":
                self.query_response(pipeboxes)
            temp = envirobox.wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = envirobox.timestamp(self.offset)
                if temp.time > current_time :
                    self.offset = temp.time - current_time + 1
            self.state = temp.data
            time_until_we_all_die = time_until_we_all_die + 1
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("thermo", self.offset, parent, children, status)

#The motion sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class motion_detect:
    def __init__(self):
        self.offset = 0
        self.name = "motion"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the mcome_to_life() function
        self.idnum = "wu"            #on line 68, the motion detector registers itself and finds its correct idnum.
        self.state = "on"            #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp(self.offset)   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp(self.offset))
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the motion detector is a push-based sensor it mus have an
#implementation of the report_state() function.
    def report_state(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp(self.offset))
        pipeboxes[self.idnum].deliver_mail(self.offset,report)
#mcome_to_life is the function that models the motion detector's behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the motion detector will exist, envirotomotdet is the mailbox from which it recieves
#information about the possible "intruders" of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def mcome_to_life(self, rbox, life_of_universe, pipeboxes, envirotomotdet, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("motdet",8,clockboxes)
            parent, children, status = find_MST("motdet", neighbors)
            self.time=berkeley_clock_synch("motdet", self.offset, parent, children, status)
        time_until_we_all_die = 0
        self.register_self(rbox)
        while time_until_we_all_die < life_of_universe:
            isthereintruder = envirotomotdet.wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = envirotomotdet.timestamp(self.offset)
                if isthereintruder.time > current_time :
                    self.offset = isthereintruder.time - current_time + 1
            self.state = isthereintruder.data
            time_until_we_all_die = time_until_we_all_die + 1
            self.report_state(pipeboxes)
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("motdet", self.offset, parent, children, status)

#The door sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class door_detect:
    def __init__(self):
        self.offset = 0
        self.name = "door"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the mcome_to_life() function
        self.idnum = "wu"            #on line 68, the motion detector registers itself and finds its correct idnum.
        self.state = "on"            #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp(self.offset)   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp(self.offset))
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the motion detector is a push-based sensor it mus have an
#implementation of the report_state() function.
    def report_state(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp(self.offset))
        pipeboxes[self.idnum].deliver_mail(self.offset,report)
#mcome_to_life is the function that models the motion detector's behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the motion detector will exist, usertodoortdet is the mailbox from which it recieves
#information about the possible "intruders" of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def dcome_to_life(self, rbox, life_of_universe, pipeboxes, usertodoortdet, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("doorboy",9,clockboxes)
            parent, children, status = find_MST("doorboy", neighbors)
            self.time=berkeley_clock_synch("doorboy", self.offset, parent, children, status)
        time_until_we_all_die = 0
        self.register_self(rbox)
        while time_until_we_all_die < life_of_universe:
            isdooropen = usertodoortdet.wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = usertodoortdet.timestamp(self.offset)
                if isdooropen.time > current_time :
                    self.offset = isdooropen.time - current_time + 1
            self.state = isdooropen.command
            time_until_we_all_die = time_until_we_all_die + 1
            self.report_state(pipeboxes)
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("doorboy", self.offset, parent, children, status)
