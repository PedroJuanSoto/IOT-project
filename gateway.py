from postalservice import message, mailbox

#The core of the program is in the gateway class. The gateway class has a
#simple data structure and most of its complexity lies in the large number
#of functions and the equally large number of roles and tasks that are
#performed by the gateway. self.registry is where the gateway keeps the information
#about which device types and names are which but in practice this information is
#more efficiently used by the self.thermoidnum, self.heateridnum, self.mot_detidnum,
#and self.lit_bubidnum which is effectively a quick "addressbook" which it uses
#to quickly locate which "pipebox" to use to communicate the required task and/or
#information. It uses self.alertheater to store whether the heater needs to be
#on, self.should_i_turn_on_bulb to keep track of whether or not it should activate
#the lightbulb, self.time_since_last_intruder to count to five in order to
#keep track of when to turn off the lightbulb, and self.mode to keep track of
#whether or not the user is home. Most of the code for the gateway can be
#broken down into two parts: registering the devices(and sensors) and
#managing the devices(and sensors). In order to make the code (and in particular the
#monlithic gcome_to_life()) more understandle and safe/secure this class was
#made highly modular.
class gateway:
    def __init__(self):
        self.registry = []
        self.mode = "home"
        self.thermoidnum = ""
        self.heateridnum = ""
        self.mot_detidnum = ""
        self.lit_bubidnum = ""
        self.door_detidnum = ""
        self.alertheater = "no"
        self.should_i_turn_on_bulb = "no"
        self.time_since_last_intruder = 0

    def activate_devices(self, rbox, num_of_devices):  #The call to activate_devices()
        while num_of_devices>0:                        #in line XX begins the process of
            z = self.check_registration_mail(rbox)     #correctly registering all devices
            if z == 1:                                 #so that they know which mailbox to
                num_of_devices = num_of_devices - 1    #listen in on and num_of_devices
                                                       #keeps track of the number of devices
    def check_registration_mail(self, rbox):           #that need to be registered
        newmail = rbox.check_mail("gate")
        if newmail == -1:                      #in check_registration_mail() the gateway
            return 0                           #listens in on the registration mailbox
        if newmail.command == "register":      #until it finds a device in need of an id
            self.register_device(rbox, newmail)
            return 1                           #in register_device() the gateway takes a
                                               #"registration form" out of the registration
    def register_device(self, rbox, registrationform):  #box and appends the data to its
        devicedata = registrationform.data     #registry. the wrongid is a timestamp used
        correctidnum = len(self.registry)      #by the device to temporaily identify itself
        self.registry.append(devicedata)       #in the registration box until it is given a
        wrongid = registrationform.fromy       #"correctid" which it then stores in update_addressbook()
        correctid = message( wrongid, "gate", "correctid", correctidnum, rbox.timestamp())
        rbox.deliver_mail(correctid)
        self.update_addressbook(devicedata, correctidnum)

    def update_addressbook(self, devicedata, correctidnum):
        if devicedata[1] == "sensor" and devicedata[2] == "temperature":
            self.thermoidnum = correctidnum
        elif devicedata[1] == "device" and devicedata[2] == "temperature":
            self.heateridnum = correctidnum
        elif devicedata[1] == "sensor" and devicedata[2] == "motion":
            self.mot_detidnum = correctidnum
        elif devicedata[1] == "device" and devicedata[2] == "motion":
            self.lit_bubidnum = correctidnum
        elif devicedata[1] == "sensor" and devicedata[2] == "door":
            self.door_detidnum = correctidnum

#The gateway uses query_state() to query the status of a pull-based sensor
#(i.e. the thermostat)
    def query_state(self, idnum, pipeboxes, life, death, backbox):
        hola = message(idnum , "gate", "query", "", pipeboxes[idnum].timestamp())
        pipeboxes[idnum ].deliver_mail(hola)
        if life +1< death:                 #sometimes there is a deadlock issue
            x = pipeboxes[idnum].wait_on_query("gate")#on the last iteration of the
            self.should_i_alert_heater(x.data, backbox)        #while loop and therefore
                                                      #the gateway ignores the final messsage

#The gateway uses change_state() to control the devices (i.e. the lightbulb and heater)
    def change_state(self, idnum, state, pipeboxes):
        ff = message(idnum,"gate","change", state, pipeboxes[idnum].timestamp())
        pipeboxes[idnum].deliver_mail(ff)

    def should_i_alert_heater(self, temp, backbox):
        oldbelief = self.alertheater
        if temp < 1:                   #a simple function that computes whether
            self.alertheater = "on"    #or not it is cold.
        if temp > 0:
            self.alertheater = "off"
        if oldbelief != self.alertheater:
            newstatus = message("backend", "gate", "heater_change", self.alertheater, backbox.timestamp())
            backbox.deliver_mail(newstatus)
        else:
            oldstatus = message("backend", "gate", "no_change", "", backbox.timestamp())
            backbox.deliver_mail(oldstatus)



#The heart of the smart home simulation is the gcome_to_life() which models the
#behavior of a smart gateway device that monitors and controls the various sensors
#and devices of a virtual smarthome. gcome_to_life() begins by registering all of
#the devices (line 105) and giving them an idnum. This first step is very important
#because each device(or sensor) needs to have its own individual "pipebox" in order
#to reduce the probability of concurrency issues and information bottlenecks
#(and also to reduce the probability of errors like "EOFError: Ran out of input"
#and "_pickle.UnpicklingError: could not find MARK"). Then after registering the
#devices the gateway alerts the user process and the virtual enviroment process,
#(lines 106-107) which seems silly but this step is also neccessary to prevent any
#concurrency issues or any potential "end of file"/"pickling" errors that occur because
#ofa lack of synchronization. It then checks on the thermostat with and alerts the
#heater if it needs to be turned on (lines 113-114). The rest of the code is dedicated
#to simaltanously communicating with the motion detector and the user process
#(while keeping track of whether time_since_last_intruder =5) so that it knows
#whether or not to turn on the lights or(XOR) alert the user. The order of events
#in gcome_to_life() where chosen as so, because the authors of the program to chose
#to emphasize program correctness/security over "realistic" and/or "optimal" design.
    def gcome_to_life(self, rbox, life_of_universe, num_of_devices, pipeboxes, usertogate, gatetobackend):
        self.activate_devices(rbox, num_of_devices)
        activate_enviroment = message("enviro", "gate", "activate", "", rbox.timestamp())
        rbox.deliver_mail(activate_enviroment)
        activate_user_interface = message("user", "gate", "activate", "", rbox.timestamp())
        rbox.deliver_mail(activate_user_interface)
        activate_backend = message("backend", "gate", "activate", self.registry, rbox.timestamp())
        rbox.deliver_mail(activate_backend)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            time_until_we_all_die = time_until_we_all_die + 1
            self.change_state(self.heateridnum, self.alertheater, pipeboxes)
            self.query_state(self.thermoidnum, pipeboxes, time_until_we_all_die, life_of_universe, gatetobackend)
            isthere_intruder = pipeboxes[self.mot_detidnum].wait_on_query("gate")
            if self.mode == "home":
                if isthere_intruder.data == "yes":
                    self.should_i_turn_on_bulb = "on"
                    self.time_since_last_intruder = 0
                else:
                    self.time_since_last_intruder = self.time_since_last_intruder + 1
                    if self.time_since_last_intruder == 5:
                        self.should_i_turn_on_bulb = "off"
                hola = message("user","gate", "", "", usertogate.timestamp())
                usertogate.deliver_mail(hola)
            elif self.mode == "away":
                self.should_i_turn_on_bulb = "off"
                intruder_alert = message("user","gate", "", isthere_intruder.data, usertogate.timestamp())
                usertogate.deliver_mail(intruder_alert)
            self.change_state(self.lit_bubidnum, self.should_i_turn_on_bulb, pipeboxes)
            userstatus = usertogate.wait_on_query("gate")
            if userstatus.data == "home":
                self.mode = "home"
            elif userstatus.data == "away":
                self.mode = "away"
            doorstatus = pipeboxes[self.door_detidnum].wait_on_query("gate")




#The door sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class backend:
    def __init__(self):
        self.registry = []
        self.database = []

    def bcome_to_life(self, rbox, life_of_universe, gatetobackend):
        addressbook = rbox.wait_on_mail("backend")
        self.registry = addressbook.data
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe-2:
            time_until_we_all_die = time_until_we_all_die + 1
            christmastime = gatetobackend.wait_on_mail()
            if christmastime.command == "no_change":
                pass
            else:
                self.database.append(christmastime)
