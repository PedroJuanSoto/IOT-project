from postalservice import message, mailbox

#The temperature sensor is a pull-based sensor, it responds to the gateway by
#sending the current temperature (see line 28).
class thermostat:
    def __init__(self):
        self.name = "temperature"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the tcome_to_life() function
        self.idnum = "wu"            #on line 30, the thermostat registers itself and finds its correct idnum.
        self.state = -1              #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp()   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp())
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the temperature sensor is a pull-based sensor it mus have an
#implementation of the query_response() function.
    def query_response(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp())
        pipeboxes[self.idnum].deliver_mail(report)
#tcome_to_life is the function that models the thermostats behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the thermostat will exist, envirobox is the mailbox from which it recieves
#information about the temperature of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def tcome_to_life(self, rbox, life_of_universe, envirobox, pipeboxes):
        self.register_self(rbox)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_query(self.idnum)
            if x.command == "query":
                self.query_response(pipeboxes)
            temp = envirobox.wait_on_mail()
            self.state = temp.data
            time_until_we_all_die = time_until_we_all_die + 1

#The motion sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class motion_detect:
    def __init__(self):
        self.name = "motion"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the mcome_to_life() function
        self.idnum = "wu"            #on line 68, the motion detector registers itself and finds its correct idnum.
        self.state = "no"            #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp()   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp())
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the motion detector is a push-based sensor it mus have an
#implementation of the report_state() function.
    def report_state(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp())
        pipeboxes[self.idnum].deliver_mail(report)
#mcome_to_life is the function that models the motion detector's behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the motion detector will exist, envirotomotdet is the mailbox from which it recieves
#information about the possible "intruders" of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def mcome_to_life(self, rbox, life_of_universe, pipeboxes, envirotomotdet):
        self.register_self(rbox)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            isthereintruder = envirotomotdet.wait_on_mail()
            self.state = isthereintruder.data
            time_until_we_all_die = time_until_we_all_die + 1
            self.report_state(pipeboxes)

#The door sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class door_detect:
    def __init__(self):
        self.name = "door"
        self.typer = "sensor"        #Upon "activating" the thermostat by calling the mcome_to_life() function
        self.idnum = "wu"            #on line 68, the motion detector registers itself and finds its correct idnum.
        self.state = "no"            #Without its correct idnum it does not know which mailbox to listen
                                     #in on for commands from the gateway. It begins the registration by
    def register_self(self, mbox):   #creating a temporary "wrongid" using a timestamp and filling out
        wrongid = mbox.timestamp()   #a registration form, it then listens in for the gateway to send a
        self.idnum = wrongid         #message addressed to the "wrongid", which itself contains the "correctid"
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp())
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#Because the motion detector is a push-based sensor it mus have an
#implementation of the report_state() function.
    def report_state(self, pipeboxes):
        report = message("gate", self.idnum, "report", self.state, pipeboxes[self.idnum].timestamp())
        pipeboxes[self.idnum].deliver_mail(report)
#mcome_to_life is the function that models the motion detector's behavior. The rbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the motion detector will exist, usertodoortdet is the mailbox from which it recieves
#information about the possible "intruders" of the enviroment, and the pipeboxes parameter is an array
#of the datatype "mailboxes" (see postalservice.py) which it uses to communicate with the gateway;
#because it does not know which pipe to listen in on, it must register_self() to discover it's self.idnum
    def dcome_to_life(self, rbox, life_of_universe, pipeboxes, usertodoortdet):
        self.register_self(rbox)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            isdooropen = usertodoortdet.wait_on_mail()
            self.state = isdooropen.command
            time_until_we_all_die = time_until_we_all_die + 1
            self.report_state(pipeboxes)
