from multiprocessing import Queue, Pipe
import time

#The "message" data type is the main object that is communicated between the
#processes. It has 5 parameters:

class clockbox:
    def __init__(self, pipe):
        self.pipey = pipe

    def send(self, offset, inmessage):      #This function delivers the message "inmessage"
        self.pipey.send(inmessage)
        inmessage.printmessage(offset,"sender")

    def recv(self,offset):
        x =  self.pipey.recv()
        x.printmessage(offset,"reader")
        return x

    def ssssend(self, offset,inmessage):      #This function delivers the message "inmessage"
        self.pipey.send(inmessage)
        #inmessage.printmessage("sender")

    def rrrrecv(self,offset):
        x =  self.pipey.recv()
        #x.printmessage("reader")
        return x

class message:
    def __init__(self, to, fromy, command, data, time):
        self.to = to                  #"to" is who the message is intedned for
        self.fromy = fromy            #"fromy" is who the message is fromy
        self.command = command  #"command" is the main intention of the communication, i.e. report, query, etc ..
        self.data = data     #"data" is any important information that needs to be communicated
        self.time = time     #"time" is a timestamp that is made upon the message's creation which is used to
                             #keep track some of the measures desired, because different processes are
                             #usually on different processors, chips, etc ... they will often have different
                             #clocks or time (especially the gateway which spends much more time active)

    #The function printmessage does exactly what it is called
    def printmessage(self,offset, sender_or_reader):
        if sender_or_reader == "sender":
            l = []
            l.append("SENT:     to=")
            l.append(self.to)
            l.append(" from=")
            l.append(self.fromy)
            l.append(" command=")
            l.append(self.command)
            l.append(" data=")
            l.append(self.data)
            l.append(" time_stamp=")
            l.append(self.time)
            l.append("      ##AT_TIME:")
            l.append(time.clock()+offset)
            print("".join(str(x) for x in l))
        elif sender_or_reader == "reader":
            l = []
            l.append("RECIEVED: to=")
            l.append(self.to)
            l.append(" from=")
            l.append(self.fromy)
            l.append(" command=")
            l.append(self.command)
            l.append(" data=")
            l.append(self.data)
            l.append(" time_stamp=")
            l.append(self.time)
            l.append("      ##AT_TIME:")
            l.append(time.clock()+offset)
            print("".join(str(x) for x in l))

#The mailbox class is the main "connection" object used to communicate between
#processes. It is a wrapper for a multiprocessing.Queue() (which is itself a
# "Connection" object with some extra locks/semaphores)

class mailbox:
    def __init__(self):
        self.messages = Queue()


    def wait_on_query(offset,self, id):     #the difference between the wait_on_mail and the
        z=-1                         #wait_on_query function is that the wait_on_mail
        while z ==-1:                #function is only safe to use in a one-sided communication
            x =  self.messages.get() #procedure; basically wait_on_query puts back any
            if x.to == id:           #mail that was not inteded for the process opening the mail
                x.printmessage(offset,"reader")
                return x
            else:
                self.messages.put(x)

    def deliver_mail(self, offset, inmessage):      #This function delivers the message "inmessage"
        try:
            self.messages.put_nowait(inmessage)
        except:
            print("An exception was thrown while SENDING the mail")
            return -1
            pass
        else:
            inmessage.printmessage(offset,"sender")

    def wait_on_mail(self,offset):
        x =  self.messages.get()
        x.printmessage("reader")
        return x

    def timestamp(self,offset):
        return time.clock()+offset

    def check_mail(self):
        try:
            x =  self.messages.get_nowait()
        except:
            return -1
            pass
        else:
            x.printmessage("reader")
            return x


#the registrationbox is almost the same as a mailbox except the functions check_mail()
#and wait_on_mail() are different because the registration box is used between
#ALL of the processes which can create new concurrency issues
class registration_box:
    def __init__(self):
        self.messages = Queue()

    def check_mail(self, id): #In order to speed up the registration process while
        try:                  #simaltanously resolving any deadlock issues or exceptions that will be thrown
            x =  self.messages.get_nowait() #the get_nowait() function was used instead
        except:                             #of the get()
            return -1
            pass
        else:
            if x.to == id:
                x.printmessage("reader")
                return x
            else:
                self.messages.put(x)
                return -1

    def deliver_mail(self, inmessage):
        x = inmessage
        self.messages.put(x)
        x.printmessage("sender")

    def wait_on_mail(self, id): #Because the registration box is used by all of
        z = -1                  #processes we must also pass the id parameter
        while z == -1:          #to make sure that the process has not left wothout
            z = self.check_mail(id)     #the message that it was wating for
        return z

    def timestamp(self,offset):
        return time.clock()+offset

#The silent mailbox is identical to the mailbox except for the fact that it does
#not have print() statements
class silent_mailbox:
    def __init__(self):
        self.messages = Queue()

    def wait_on_query(self, offset, id):
        z=-1
        while z ==-1:
            x =  self.messages.get()
            if x.to == id:
                return x
            else:
                self.messages.put(x)

    def deliver_mail(self, offset, inmessage):
        try:
            self.messages.put_nowait(inmessage)
        except:
            print("An exception was thrown while SENDING the mail")
            return -1
            pass

    def wait_on_mail(self,offset):
        x =  self.messages.get()
        return x

    def timestamp(self,offset):
        return time.clock()+offset

    def check_mail(self):
        try:
            x =  self.messages.get_nowait()
        except:
            return -1
            pass
        else:
            return x

class silent_registration_box:
    def __init__(self):
        self.messages = Queue()

    def check_mail(self, id): #In order to speed up the registration process while
        try:                  #simaltanously resolving any deadlock issues or exceptions that will be thrown
            x =  self.messages.get_nowait() #the get_nowait() function was used instead
        except:                             #of the get()
            return -1
            pass
        else:
            if x.to == id:
                return x
            else:
                self.messages.put(x)
                return -1

    def deliver_mail(self, inmessage):
        x = inmessage
        self.messages.put(x)

    def wait_on_mail(self, id): #Because the registration box is used by all of
        z = -1                  #processes we must also pass the id parameter
        while z == -1:          #to make sure that the process has not left wothout
            z = self.check_mail(id)     #the message that it was wating for
        return z

    def timestamp(self,offset):
        return time.clock()+offset
