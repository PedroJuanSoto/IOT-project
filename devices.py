from postalservice import message, mailbox
from leaderelection import create_edges, find_MST

#The heater is a device that turns itself on with the change_state() function on line
#14 upon the request of the gateway (line 35&36). Its state then affects the
#probability of the enviroment gettting warmer via its interaction through
#the envirobox parameter in line 31
class heater:
    def __init__(self):
        self.name = "temperature"
        self.typer = "device"             #Upon "activating" the heater by calling the hcome_to_life() function
        self.idnum = "wu"                 #on line 31, the heater registers itself and finds its correct idnum.
        self.state = "off"                #Without its correct idnum it does not know which mailbox to listen
                                          #in on for commands from the gateway. It begins the registration by
    def change_state(self, state):        #creating a temporary "wrongid" using a timestamp and filling out
        self.state = state                #a registration form, it then listens in for the gateway to send a
                                          #message addressed to the "wrongid", which itself contains the "correctid"
    def register_self(self, mbox):
        wrongid = mbox.timestamp()
        self.idnum = wrongid
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp())
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#hcome_to_life is the function that models the heater's behavior. The mbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the heater will exist, envirobox is the mailbox from which actuates
#itself to affect the probability distribution of the temperature of the enviroment,
#and the pipeboxes parameter is an array of the datatype "mailboxes" (see postalservice.py)
#which it uses to communicate with the gateway; because it does not know which pipe to listen in on,
#it must register_self() (line 17) to discover it's self.idnum
    def hcome_to_life(self, mbox, life_of_universe, pipeboxes, envirobox, clockboxes):
        self.register_self(mbox)
        neighbors = create_edges("heater",clockboxes)
        find_MST("heater", neighbors)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_mail()
            self.change_state(x.data)
            ff = message("envirobox","heater","change", self.state, envirobox.timestamp())
            envirobox.deliver_mail(ff)
            time_until_we_all_die = time_until_we_all_die + 1

#The light_bulb is a device that turns itself on with the change_state() function on line
#52 upon the request of the gateway (line 73&74). Its state then affects the
#probability of an intruder on the property via its interaction through
#the lit_bubtoenviro parameter in line 69
class light_bulb:
    def __init__(self):
        self.name = "motion"
        self.typer = "device"           #Upon "activating" the lightbulb by calling the lcome_to_life() function
        self.idnum = "wu"               #on line 69, the lightbulb registers itself and finds its correct idnum.
        self.state = "off"              #Without its correct idnum it does not know which mailbox to listen
                                        #in on for commands from the gateway. It begins the registration by
    def change_state(self, state):      #creating a temporary "wrongid" using a timestamp and filling out
        self.state = state              #a registration form, it then listens in for the gateway to send a
                                        #message addressed to the "wrongid", which itself contains the "correctid"
    def register_self(self, mbox):
        wrongid = mbox.timestamp()
        self.idnum = wrongid
        registrationform = message("gate", wrongid, "register", [self.state, self.typer, self.name], mbox.timestamp())
        mbox.deliver_mail(registrationform)
        self.idnum = mbox.wait_on_mail(wrongid).data

#lcome_to_life is the function that models the light_bulb's behavior. The mbox parameter is
#the registrationbox() that it uses to register itself, life_of_universe is the duration of
#time for which the light_bulb will exist, lit_bubtoenviro is the mailbox from which actuates
#itself to affect the probability distribution of the intruder probabilty of the enviroment,
#and the pipeboxes parameter is an array of the datatype "mailboxes" (see postalservice.py)
#which it uses to communicate with the gateway; because it does not know which pipe to listen in on,
#it must register_self() (line 55) to discover it's self.idnum
    def lcome_to_life(self, mbox, life_of_universe, pipeboxes, lit_bubtoenviro, clockboxes):
        self.register_self(mbox)
        neighbors = create_edges("litbub",clockboxes)
        find_MST("litbub", neighbors)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            x = pipeboxes[self.idnum].wait_on_mail()
            self.change_state(x.data)
            ff = message("envirobox","lit_bub","change", self.state, lit_bubtoenviro.timestamp())
            lit_bubtoenviro.deliver_mail(ff)
            time_until_we_all_die = time_until_we_all_die + 1
