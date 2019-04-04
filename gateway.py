from postalservice import message, mailbox
from leaderelection import create_edges, find_MST
from berkeley import berkeley_clock_synch

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
        self.offset = 0

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
        correctid = message( wrongid, "gate", "correctid", correctidnum, rbox.timestamp(self.offset))
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
    def query_state(self, idnum, pipeboxes, life, death, backbox, berkeley_or_lamport):
        hola = message(idnum , "gate", "query", "", pipeboxes[idnum].timestamp(self.offset))
        pipeboxes[idnum ].deliver_mail(self.offset,hola)
        if life +1< death:                 #sometimes there is a deadlock issue
            x = pipeboxes[idnum].wait_on_query(self.offset,"gate")#on the last iteration of the
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[idnum].timestamp(self.offset)
                if x.time > current_time :
                    self.offset = x.time - current_time + 1
            self.should_i_alert_heater(x.data, backbox)        #while loop and therefore
            newstatus = message("backend", "gate", "temp_change", x.data, backbox.timestamp(self.offset))
            backbox.deliver_mail(self.offset,newstatus)                   #the gateway ignores the final messsage

#The gateway uses change_state() to control the devices (i.e. the lightbulb and heater)
    def change_state(self, idnum, state, pipeboxes):
        ff = message(idnum,"gate","change", state, pipeboxes[idnum].timestamp(self.offset))
        pipeboxes[idnum].deliver_mail(self.offset,ff)

    def should_i_alert_heater(self, temp, backbox):
        oldbelief = self.alertheater
        if temp < 1:                   #a simple function that computes whether
            self.alertheater = "on"    #or not it is cold.
        if temp > 0:
            self.alertheater = "off"
        if oldbelief != self.alertheater:
            newstatus = message("backend", "gate", "heater_change", self.alertheater, backbox.timestamp(self.offset))
            backbox.deliver_mail(self.offset,newstatus)
        else:
            oldstatus = message("backend", "gate", "no_change", "", backbox.timestamp(self.offset))
            backbox.deliver_mail(self.offset,oldstatus)



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
    def gcome_to_life(self, rbox, life_of_universe, num_of_devices, pipeboxes, usertogate, gatetobackend, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("gate",2,clockboxes)
            parent, children, status = find_MST("gate", neighbors)
            self.time=berkeley_clock_synch("gate", self.offset, parent, children, status)
        self.activate_devices(rbox, num_of_devices)
        activate_enviroment = message("enviro", "gate", "activate", "", rbox.timestamp(self.offset))
        rbox.deliver_mail(activate_enviroment)
        activate_user_interface = message("user", "gate", "activate", "", rbox.timestamp(self.offset))
        rbox.deliver_mail(activate_user_interface)
        activate_backend = message("backend", "gate", "activate", self.registry, rbox.timestamp(self.offset))
        rbox.deliver_mail(activate_backend)
        time_until_we_all_die = 0
        oldmotdetdata = "no"
        while time_until_we_all_die < life_of_universe:
            time_until_we_all_die = time_until_we_all_die + 1
            self.change_state(self.heateridnum, self.alertheater, pipeboxes)
            self.query_state(self.thermoidnum, pipeboxes, time_until_we_all_die, life_of_universe, gatetobackend, berkeley_or_lamport)
            isthere_intruder = pipeboxes[self.mot_detidnum].wait_on_query(self.offset,"gate")
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[self.mot_detidnum].timestamp(self.offset)
                if isthere_intruder.time > current_time :
                    self.offset = isthere_intruder.time - current_time + 1
            oldbulbstatus = self.should_i_turn_on_bulb
            if oldmotdetdata != isthere_intruder.data:
                newmotdetbstatus = message("backend", "gate", "motion_change", isthere_intruder.data, gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,newmotdetbstatus)
            else:
                oldstatus = message("backend", "gate", "no_change", "", gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,oldstatus)
            oldmotdetdata = isthere_intruder.data
            if self.mode == "home":
                if isthere_intruder.data == "yes":
                    self.should_i_turn_on_bulb = "on"
                    self.time_since_last_intruder = 0
                else:
                    self.time_since_last_intruder = self.time_since_last_intruder + 1
                    if self.time_since_last_intruder == 5:
                        self.should_i_turn_on_bulb = "off"
                hola = message("user","gate", "", "", usertogate.timestamp(self.offset))
                usertogate.deliver_mail(self.offset,hola)
            elif self.mode == "away":
                self.should_i_turn_on_bulb = "off"
                intruder_alert = message("user","gate", "", isthere_intruder.data, usertogate.timestamp(self.offset))
                usertogate.deliver_mail(self.offset,intruder_alert)
            self.change_state(self.lit_bubidnum, self.should_i_turn_on_bulb, pipeboxes)
            if oldbulbstatus != self.should_i_turn_on_bulb:
                newbulbstatus = message("backend", "gate", "bulb_change", self.should_i_turn_on_bulb, gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,newbulbstatus)
            else:
                oldstatus = message("backend", "gate", "no_change", "", gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,oldstatus)
            userstatus = usertogate.wait_on_query(self.offset,"gate")
            if berkeley_or_lamport == "lamport":
                current_time = usertogate.timestamp(self.offset)
                if userstatus.time > current_time :
                    self.offset = userstatus.time - current_time + 1
            oldpresencestatus = self.mode
            if userstatus.data == "home":
                self.mode = "home"
            elif userstatus.data == "away":
                self.mode = "away"
            if oldpresencestatus != self.mode:
                newpresencestatus = message("backend", "gate", "presence_change", self.mode, gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,newpresencestatus)
            else:
                oldstatus = message("backend", "gate", "no_change", "", gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,oldstatus)
            doorstatus = pipeboxes[self.door_detidnum].wait_on_query(self.offset,"gate")
            if berkeley_or_lamport == "lamport":
                current_time = pipeboxes[self.door_detidnum].timestamp(self.offset)
                if doorstatus.time > current_time :
                    self.offset = doorstatus.time - current_time + 1
            if doorstatus.data == "statechange":
                newdoorstatus = message("backend", "gate", "door_change", self.mode, gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,newdoorstatus)
            else:
                oldstatus = message("backend", "gate", "no_change", "", gatetobackend.timestamp(self.offset))
                gatetobackend.deliver_mail(self.offset,oldstatus)
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("gate", self.offset, parent, children, status)




#The door sensor is a push-based sensor which means that it
#pushes a notification to the gateway whenever it senses motion
class backend:
    def __init__(self):
        self.registry = []
        self.database = []
        self.thermoidnum = ""
        self.heateridnum = ""
        self.mot_detidnum = ""
        self.lit_bubidnum = ""
        self.door_detidnum = ""
        self.sec_beaconidnum = ""
        self.offset = 0

    def bcome_to_life(self, rbox, life_of_universe, gatetobackend, clockboxes, berkeley_or_lamport):
        if berkeley_or_lamport == "berkeley":
            neighbors = create_edges("backend", 3,clockboxes)
            parent, children, status = find_MST("backend", neighbors)
            self.time=berkeley_clock_synch("backend", self.offset, parent, children, status)
        addressbook = rbox.wait_on_mail("backend")
        self.registry = addressbook.data
        for j, x in enumerate(self.registry):
            if x[1] == "sensor" and x[2] == "temperature":
                self.thermoidnum = j
            elif x[1] == "device" and x[2] == "temperature":
                self.heateridnum = j
            elif x[1] == "sensor" and x[2] == "motion":
                self.mot_detidnum = j
            elif x[1] == "device" and x[2] == "motion":
                self.lit_bubidnum = j
            elif x[1] == "sensor" and x[2] == "door":
                self.door_detidnum = j
        security_beacon = ["","sensor","security"]
        self.sec_beaconidnum =len(self.registry)
        self.registry.append(security_beacon)
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe-2:
            # for q in self.registry:
            #     print(q)
            time_until_we_all_die = time_until_we_all_die + 1
            for q in range(6):
                christmastime = gatetobackend.wait_on_mail(self.offset)
                if berkeley_or_lamport == "lamport":
                    current_time = gatetobackend.timestamp(self.offset)
                    if christmastime.time > current_time :
                        self.offset = christmastime.time - current_time + 1
                if christmastime.command == "no_change":
                    pass
                else:
                    if christmastime.command == "temp_change":
                        if self.registry[self.thermoidnum][0] !=christmastime.data:
                            self.database.append(christmastime)
                            self.registry[self.thermoidnum][0] =christmastime.data
                    elif christmastime.command == "heater_change":
                        self.database.append(christmastime)
                        self.registry[self.heateridnum][0] =christmastime.data
                    elif christmastime.command == "motion_change":
                        self.database.append(christmastime)
                        self.registry[self.mot_detidnum][0] =christmastime.data
                    elif christmastime.command == "bulb_change":
                        self.database.append(christmastime)
                        self.registry[self.lit_bubidnum][0] =christmastime.data
                    elif christmastime.command == "door_change":
                        self.database.append(christmastime)
                        self.registry[self.door_detidnum][0] =christmastime.data
                    elif christmastime.command == "presence_change":
                        self.database.append(christmastime)
                        self.registry[self.sec_beaconidnum][0] =christmastime.data
            if berkeley_or_lamport == "berkeley":
                self.time=berkeley_clock_synch("backend", self.offset, parent, children, status)
        if berkeley_or_lamport == "berkeley":
            self.time=berkeley_clock_synch("backend", self.offset, parent, children, status)
            self.time=berkeley_clock_synch("backend", self.offset, parent, children, status)
        for q in range(8):
            christmastime = gatetobackend.wait_on_mail(self.offset)
            if berkeley_or_lamport == "lamport":
                current_time = gatetobackend.timestamp(self.offset)
                if christmastime.time > current_time :
                    self.offset = christmastime.time - current_time + 1
            if christmastime.command == "no_change":
                pass
            else:
                if christmastime.command == "temp_change":
                    if self.registry[self.thermoidnum][0] !=christmastime.data:
                        self.database.append(christmastime)
                        self.registry[self.thermoidnum][0] =christmastime.data
                elif christmastime.command == "heater_change":
                    self.database.append(christmastime)
                    self.registry[self.heateridnum][0] =christmastime.data
                elif christmastime.command == "motion_change":
                    self.database.append(christmastime)
                    self.registry[self.mot_detidnum][0] =christmastime.data
                elif christmastime.command == "bulb_change":
                    self.database.append(christmastime)
                    self.registry[self.lit_bubidnum][0] =christmastime.data
                elif christmastime.command == "door_change":
                    self.database.append(christmastime)
                    self.registry[self.door_detidnum][0] =christmastime.data
                elif christmastime.command == "presence_change":
                    self.database.append(christmastime)
                    self.registry[self.sec_beaconidnum][0] =christmastime.data
        for q in self.registry:
            print(q)
        for z in self.database:
            z.printmessage(self.offset,"reader")
