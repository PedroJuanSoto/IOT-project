from postalservice import message, mailbox
from leaderelection import create_edges, find_MST

#the user process is the simplest process. It interacts with the user by asking whether
#or not they wish to stay home (and holding down the enter key simulates staying
#in the same place). If the user leaves home (i.e. self.name =="away") and the
#gateway notifies the user process that there is an intruder then the user process
#notifies the user with a hard to miss "ALERT" notification.
class user_interface:
    def __init__(self):
        self.name = "HaibinandPedro"

    def ucome_to_life(self, mbox, life_of_universe, usertogate, usertodoor, clockboxes):
        mbox.wait_on_mail("user")
        time_until_we_all_die = 0
        self.name = "home"
        neighbors = create_edges("user",4,clockboxes)
        find_MST("user", neighbors)
        while time_until_we_all_die < life_of_universe:
            x = usertogate.wait_on_query("user")
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
            report = message("gate", "user", "", self.name, usertogate.timestamp())
            usertogate.deliver_mail(report)
            if self.name != prevstate:
                door = message("door", "user", "statechange", self.name, usertodoor.timestamp())
                usertodoor.deliver_mail(door)
            else:
                door = message("door", "user", "nochange", "", usertodoor.timestamp())
                usertodoor.deliver_mail(door)
