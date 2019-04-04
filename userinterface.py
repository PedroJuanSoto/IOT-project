from postalservice import message, mailbox
from leaderelection import create_edges, find_MST
from berkeley import berkeley_clock_synch

#the user process is the simplest process. It interacts with the user by asking whether
#or not they wish to stay home (and holding down the enter key simulates staying
#in the same place). If the user leaves home (i.e. self.name =="away") and the
#gateway notifies the user process that there is an intruder then the user process
#notifies the user with a hard to miss "ALERT" notification.
class user_interface:
    def __init__(self):
        self.name = "HaibinandPedro"
        self.offset = 0

    def ucome_to_life(self, mbox, life_of_universe, usertogate, usertodoor, clockboxes):
        neighbors = create_edges("user",4,clockboxes)
        parent, children, status = find_MST("user", neighbors)
        self.time=berkeley_clock_synch("user", self.offset, parent, children, status)
        mbox.wait_on_mail("user")
        time_until_we_all_die = 0
        self.name = "home"
        while time_until_we_all_die < life_of_universe:
            x = usertogate.wait_on_query(self.offset,"user")
            time_until_we_all_die = time_until_we_all_die + 1
            if x.data == "yes" and self.name=="away":
                print("      A        L            EEEEEEEEEEE    RRRRRRRR    TTTTTTTTTTTTT")
                print("     A A       L            E              R       R         T     ")
                print("    A   A      L            E              R       R         T     ")
                print("   AAAAAAA     L            EEEEEEEEEEE    R RRRRRR          T     ")
                print("  A       A    L            E              R       R         T     ")
                print(" A         A   L            E              R        R        T     ")
                print("A           A  LLLLLLLLLLL  EEEEEEEEEEE    R         R       T     ")
            else:
                pass
            prevstate = self.name
            home_or_not = input('')
            if home_or_not == "away":
                self.name= "away"
            elif home_or_not == "home":
                self.name= "home"
            report = message("gate", "user", "", self.name, usertogate.timestamp(self.offset))
            usertogate.deliver_mail(self.offset,report)
            if self.name != prevstate:
                door = message("door", "user", "statechange", self.name, usertodoor.timestamp(self.offset))
                usertodoor.deliver_mail(self.offset,door)
            else:
                door = message("door", "user", "nochange", "", usertodoor.timestamp(self.offset))
                usertodoor.deliver_mail(self.offset,door)
            self.time=berkeley_clock_synch("user", self.offset, parent, children, status)
