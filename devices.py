from postalservice import message, mailbox
from leaderelection import create_edges, find_MST
from berkeley import berkeley_clock_synch

#The heater is a device that turns itself on with the change_state() function on line
#14 upon the request of the gateway (line 35&36). Its state then affects the
#probability of the enviroment gettting warmer via its interaction through
#the envirobox parameter in line 31
class heater:
    def __init__(self):
        self.offset = 0
        self.name = "temperature"
        self.typer = "device"             #Upon "activating" the heater by calling the hcome_to_life() function
        self.idnum = "wu"                 #on line 31, the heater registers itself and finds its correct idnum.
        self.state = "off"                #Without its correct idnum it does not know which mailbox to listen
                                          #in on for commands from the gateway. It begins the registration by
    def change_state(self, state):        #creating a temporary "wrongid" using a timestamp and filling out
        self.state = state                #a registration form, it then listens in for the gateway to send a
                                          #message addressed to the "wrongid", which itself contains the "correctid"
    def register_self(self, mbox):
        wrongid = mbox.timestamp(self.offset)
        self.idnum = wrongid
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp(self.offset))
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#hcome_to_life is the function that models the heater's behavior. The mbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the heater will exist, envirobox is the mailbox from which actuates
#itself to affect the probability distribution of the temperature of the enviroment,
#and the pipeboxes parameter is an array of the datatype "mailboxes" (see postalservice.py)
#which it uses to communicate with the gateway; because it does not know which pipe to listen in on,
#it must register_self() (line 17) to discover it's self.idnum
    def hcome_to_life(self, mbox, life_of_universe, pipeboxes, envirobox, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("heater",1,clockboxes)
            parent, children, status = find_MST("heater", neighbors)
            self.time=berkeley_clock_synch("heater", self.offset, parent, children, status)
        time_until_we_all_die = 0
        self.register_self(mbox)
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[self.idnum].timestamp(self.offset)
                if x.time > current_time :
                    self.offset = x.time - current_time + 1
            self.change_state(x.data)
            ff = message("envirobox","heater","change", self.state, envirobox.timestamp(self.offset))
            envirobox.deliver_mail(self.offset,ff)
            time_until_we_all_die = time_until_we_all_die + 1
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("heater", self.offset, parent, children, status)

#The light_bulb is a device that turns itself on with the change_state() function on line
#52 upon the request of the gateway (line 73&74). Its state then affects the
#probability of an intruder on the property via its interaction through
#the lit_bubtoenviro parameter in line 69
class light_bulb:
    def __init__(self):
        self.offset = 0
        self.name = "motion"
        self.typer = "device"           #Upon "activating" the lightbulb by calling the lcome_to_life() function
        self.idnum = "wu"               #on line 69, the lightbulb registers itself and finds its correct idnum.
        self.state = "off"              #Without its correct idnum it does not know which mailbox to listen
                                        #in on for commands from the gateway. It begins the registration by
    def change_state(self, state):      #creating a temporary "wrongid" using a timestamp and filling out
        self.state = state              #a registration form, it then listens in for the gateway to send a
                                        #message addressed to the "wrongid", which itself contains the "correctid"
    def register_self(self, mbox):
        wrongid = mbox.timestamp(self.offset)
        self.idnum = wrongid
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp(self.offset))
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#lcome_to_life is the function that models the light_bulb's behavior. The mbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the light_bulb will exist, lit_bubtoenviro is the mailbox from which actuates
#itself to affect the probability distribution of the intruder probabilty of the enviroment,
#and the pipeboxes parameter is an array of the datatype "mailboxes" (see postalservice.py)
#which it uses to communicate with the gateway; because it does not know which pipe to listen in on,
#it must register_self() (line 55) to discover it's self.idnum
    def lcome_to_life(self, mbox, life_of_universe, pipeboxes, lit_bubtoenviro, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("litbub",5,clockboxes)
            parent, children, status = find_MST("litbub", neighbors)
            self.time=berkeley_clock_synch("litbub", self.offset, parent, children, status)
        time_until_we_all_die = 0
        self.register_self(mbox)
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[self.idnum].timestamp(self.offset)
                if x.time > current_time :
                    self.offset = x.time - current_time + 1
            self.change_state(x.data)
            ff = message("envirobox","lit_bub","change", self.state, lit_bubtoenviro.timestamp(self.offset))
            lit_bubtoenviro.deliver_mail(self.offset,ff)
            time_until_we_all_die = time_until_we_all_die + 1
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("heater", self.offset, parent, children, status)
