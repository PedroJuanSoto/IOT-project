from multiprocessing import Process, Queue, cpu_count, Pipe
from postalservice import message, mailbox, registration_box, silent_mailbox
from enviroment import enviroment
from gateway import gateway, backend
from sensors import thermostat, motion_detect, door_detect
from devices import heater, light_bulb
from userinterface import user_interface

print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("Hello! Welcome to Haibin and Pedro's Smart Home Simulation")
print("There is only two possible commands inside the simulation:")
print("You can type in the string \"home\" or the string \"away\",")
print("to respectively perform the action of staying home or going away.")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("You can also hold down the enter key if you wish to stay at your")
print("current location for a long time (it is a great way to test the program")
print("for a large number of loops.")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("Just a few questions before we start:")
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("Would you like to see all the communications between the gateway and")
print("the devices?")
print("(Please enter \"yes\" or \"no\")")
yes_or_no_one = input('')
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("Would you like to see all the interactions between the enviroment and")
print("the devices?")
print("(Please enter \"yes\" or \"no\")")
yes_or_no_two = input('')
print("-----------------------------------------------------------------------")
print("-----------------------------------------------------------------------")
print("For how many \"hours\" would you like to run the simulation")
print("(1 virtual hour is one gateway while loop,")
print("i.e. 100000 virtual hours = approx. 1 real minute)")
print("(Please enter a positive integer 3<x<10^7 )")
length_of_life = int(input(''))

print(length_of_life)

x = [1,1,1,1,1,1,1,1,1,1,1,1]
if yes_or_no_one == "no":
    x[0]=0
    x[1]=0
    x[4]=0
    x[6]=0
    x[8]=0
    x[10]=0
    x[11]=0
if yes_or_no_two == "no":
    x[2]=0
    x[3]=0
    x[5]=0
    x[7]=0
    x[9]=0
if length_of_life<4 or length_of_life>10000000:
    print("Time has no meaning anymore")
    print("The universe will now slowly collapse")
    print("-------------------------------------")
    print("--------------------------")
    print("-------------------")
    print("-------------")
    print("--------")
    print("----")
    print("...")
    print("..")
    print(".")
    print(".")
    print(".")
    exit()


#the create_the_universe() function creates a universe that lives as long as the
#parameter "how_much_time_do_we_really_have_at_the_end_of_the_day" which is entered by the user.
#This parameter is limited to 10^7 because the authors of this program have only tested the
#program for that many while loops.
def create_the_universe(z, how_much_time_do_we_really_have_at_the_end_of_the_day):
    home= enviroment()
    thermo =thermostat()
    gate = gateway()
    heatboy = heater()
    motdet = motion_detect()
    lit_bub = light_bulb()
    user = user_interface()
    doordet = door_detect()
    backman = backend()

    registrationbox = registration_box()
    time_of_death = how_much_time_do_we_really_have_at_the_end_of_the_day

#these if/elif statements control whether or not the user would like to see
#every bit of communication that occurs between the various processes. A 1
#makes the respective communication visible and a 0 silences that pipe.
    if z[0]==1:
        a = mailbox()
        gatetodevice0 = a
    elif z[0]==0:
        a = silent_mailbox()
        gatetodevice0 = a

    if z[1]==1:
        c = mailbox()
        gatetodevice1 = c
    elif z[1]==0:
        c = silent_mailbox()
        gatetodevice1 = c

    if z[2]==1:
        e = mailbox()
        envirotothermo = e
    elif z[2]==0:
        e = silent_mailbox()
        envirotothermo = e

    if z[3]==1:
        g = mailbox()
        heatertoenviro = g
    elif z[3]==0:
        g = silent_mailbox()
        heatertoenviro = g

    if z[4]==1:
        x = mailbox()
        gatetodevice2 = x
    elif z[4]==0:
        x = silent_mailbox()
        gatetodevice2 = x

    if z[5]==1:
        y = mailbox()
        envirotomotdet = y
    elif z[5]==0:
        y = silent_mailbox()
        envirotomotdet = y

    if z[6]==1:
        w = mailbox()
        gatetodevice3 = w
    elif z[6]==0:
        w = silent_mailbox()
        gatetodevice3 = w

    if z[7]==1:
        y = mailbox()
        lit_bubtoenviro = y
    elif z[7]==0:
        y = silent_mailbox()
        lit_bubtoenviro = y

    if z[8]==1:
        u = mailbox()
        usertogate = u
    elif z[8]==0:
        u = silent_mailbox()
        usertogate = u

    if z[9]==1:
        qqqq = mailbox()
        usertodoor = qqqq
    elif z[9]==0:
        qqqq = silent_mailbox()
        usertodoor = qqqq

    if z[10]==1:
        l = mailbox()
        gatetodevice4 = l
    elif z[10]==0:
        l = silent_mailbox()
        gatetodevice4 = l

    if z[11]==1:
        cc = mailbox()
        backtogate = cc
    elif z[11]==0:
        cc = silent_mailbox()
        backtogate = cc

    #I need to create pipes for the clock sycnh algorithms
    gatetoheaterpipe, heatertogatepipe = Pipe()
    gatetothermopipe, thermotogatepipe = Pipe()
    gatetomotdetpipe, motdettogatepipe = Pipe()
    gatetolitbubpipe, litbubtogatepipe = Pipe()
    gatetouserpipe, usertogatepipe = Pipe()
    gatetodoorpipe, doortogatepipe = Pipe()
    gatetobackendpipe, backendtogatepipe = Pipe()

    gatewayclockboxes = [gatetoheaterpipe, gatetothermopipe, gatetomotdetpipe, gatetolitbubpipe, gatetouserpipe, gatetodoorpipe, gatetobackendpipe]
    backendclockboxes = [backendtogatepipe]

    envirotoheaterpipe, heatertoenviropipe = Pipe()
    envirotothermopipe, thermotoenviropipe = Pipe()
    envirotomotdetpipe, motdettoenviropipe = Pipe()
    envirotolitbubpipe, litbubtoenviropipe = Pipe()

    enviroclockboxes = [envirotoheaterpipe, envirotothermopipe, envirotomotdetpipe, envirotolitbubpipe]

    heaterclockboxes = [heatertogatepipe, heatertoenviropipe]
    thermoclockboxes = [thermotogatepipe, thermotoenviropipe]
    motdetclockboxes = [motdettogatepipe, motdettoenviropipe]
    litbubclockboxes = [litbubtogatepipe, litbubtoenviropipe]

    usertodoorpipe, doortouserpipe = Pipe()

    userclockboxes = [usertogatepipe, usertodoorpipe]
    doorclockboxes = [doortogatepipe, doortouserpipe]



#until the calls to activate_devices() and register_self() are made, the gateway and
#the different devices do not know which pipe to listen in on, and therefore they are
#not given an particular names when they are passed on to the processes.
    gatewaypipeboxes = [gatetodevice0, gatetodevice1, gatetodevice2, gatetodevice3, gatetodevice4]

#The proceding lines create the respective processes and start()s and join()s them
#if __name__ == '__main__': line prevents any other processes other than "__main__"
#from trying anything stupid.
    if __name__ == '__main__':
        p2 = Process(target=heatboy.hcome_to_life, args=(registrationbox, time_of_death, gatewaypipeboxes, heatertoenviro, heaterclockboxes))
        p1 = Process(target=thermo.tcome_to_life, args=(registrationbox, time_of_death, envirotothermo, gatewaypipeboxes, thermoclockboxes))
        p3 = Process(target=home.ecome_to_life, args=(registrationbox, time_of_death, envirotothermo , heatertoenviro, envirotomotdet, lit_bubtoenviro, enviroclockboxes))
        p0 = Process(target=gate.gcome_to_life, args=(registrationbox, time_of_death, 5, gatewaypipeboxes, usertogate, backtogate, gatewayclockboxes ))
        p4 = Process(target=motdet.mcome_to_life, args=(registrationbox, time_of_death, gatewaypipeboxes, envirotomotdet, motdetclockboxes))
        p5 = Process(target=lit_bub.lcome_to_life, args=(registrationbox, time_of_death, gatewaypipeboxes, lit_bubtoenviro, litbubclockboxes))
        p6 = Process(target=doordet.dcome_to_life, args=(registrationbox, time_of_death, gatewaypipeboxes,  usertodoor, doorclockboxes ))
        p7 = Process(target=backman.bcome_to_life, args=(registrationbox, time_of_death, backtogate, backendclockboxes))


        p0.start()
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()
        p6.start()
        p7.start()

 #Because the user proccess takes in keyboard input, the user process must be
 #identified with the "__main__" process or else some interesting EOF errors will
 #occur.
        user.ucome_to_life(registrationbox, time_of_death, usertogate, usertodoor, userclockboxes)
        p0.join()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()
        p6.join()
        p7.join()

#this line creates the universe.
create_the_universe(x, length_of_life)
