from postalservice import message, mailbox
import random

#The enviroment class is the virtual enviroment which is modeled as it's own seprate
#process so as to make the simulation more real. It has two probability distributions,
#one for the temperature and one for the "intruder," which are modeled as a markov process.
class enviroment:
    def __init__(self):
        self.temperature = 1
        self.intruder = "no"
        random.seed()
        self.is_heater_on = "no"
        self.is_light_on = "no"

#an hour of time is simulated by one while loop so that thetime%24 < 12 means that
#it is "daytime" and "nighttime" otherwise
    def isnight(self, thetime):
        if thetime%24 < 12:
            return 0
        else:
            return 1
#The temperature is a simple markov chain which at any time can rise, drop, or stay
#the same. The probabiltiy is affected by the time of day i.e. the function isnight() (line 17)
#and whether the heater is on. If the heater is on it is more likely that the temperature
#will rise and if it is night it is more likely that the temperature will drop
    def temperature_change(self, thetime):
        r = random.randint(0,100)
        if self.is_heater_on == "no":
            if self.isnight(thetime):
                if r < 97:
                    self.temperature = self.temperature -1
                elif r > 99:
                    self.temperature = self.temperature + 1
            else:
                if r < 32:
                    self.temperature = self.temperature -1
                elif r > 94:
                    self.temperature = self.temperature + 1
        else:
            if self.isnight(thetime):
                if r < 5:
                    self.temperature = self.temperature -1
                elif r > 49:
                    self.temperature = self.temperature + 1
            else:
                if r < 2:
                    self.temperature = self.temperature -1
                elif r > 4:
                    self.temperature = self.temperature + 1

#The probability of an "intruder" (which can be the owner walking around the living
#room or an authentic trespasser). The probabiltiy is affected by the time of day
#i.e. the function isnight() (line 17) and whether the light is on. The possible 
# outcomes are binary; either there is or isn't an intruder.
    def intruder_change(self, thetime):
        r = random.randint(0,100)
        if self.is_light_on == "off":
            if self.isnight(thetime):
                if r < 61:
                    self.intruder = "yes"
                else:
                    self.intruder = "no"
            else:
                if r < 23:
                    self.intruder = "yes"
                else:
                    self.intruder = "no"
        else:
            if self.isnight(thetime):
                if r < 47:
                    self.intruder = "yes"
                else :
                    self.intruder = "no"
            else:
                if r < 2:
                    self.intruder = "yes"
                else :
                    self.intruder = "no"

#ecome_to_life is the function that models the virtual enviroment's behavior. The
#mbox parameter is the registrationbox() that the gateway uses to signal the start of the
#simulation, life_of_universe is the duration of time for which the virtual universe
# will exist, thermobox is the mailbox used to relay information to the thermostat,
#heaterbox is the mailbox that the heater uses to affect the virtual enviroments
#probability distribution for the temperature, envirotomotdet is the mailbox used
#to relay information to the motion detecter, and lit_bubtoenviro is the mailbox
#that the lightbulb uses to affect the virtual enviroments probability distribution
#for the "intruder."
    def ecome_to_life(self, mbox, life_of_universe, thermobox, heaterbox, envirotomotdet, lit_bubtoenviro):
        mbox.wait_on_mail("enviro")
        time_until_we_all_die = 0
        while time_until_we_all_die < life_of_universe:
            self.temperature_change(time_until_we_all_die)
            temp = message("thermo","enviro", "", self.temperature, thermobox.timestamp())
            thermobox.deliver_mail(temp)
            x = heaterbox.wait_on_mail()
            if x.data == "on":
                self.is_heater_on = "yes"
            else:
                self.is_heater_on = "no"
            time_until_we_all_die = time_until_we_all_die + 1
            self.intruder_change(time_until_we_all_die)
            isthereintruder = message("mot_det","enviro", "", self.intruder, envirotomotdet.timestamp())
            envirotomotdet.deliver_mail(isthereintruder)
            x = lit_bubtoenviro.wait_on_mail()
            if x.data == "on":
                self.is_light_on = "yes"
            else:
                self.is_light_on = "no"