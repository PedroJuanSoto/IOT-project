from postalservice import message
import time

def berkeley_clock_synch(name, offset, parent, children, status):

    if status == "leader":                   #This is a modified Berkeley algorithm which exploits the tree
        communication_delays = []            #tree structure from leaderelect.py in order to reduce the
        times_and_weight = []                #complexity of the algorithm from O(n) to O(blog_b(n)+wlog_b(n))
        for child in children:               #the proof of this is given in the write up
            send_time = my_time(offset)
            child[1].send(offset,message(child[2], name, "lets_see_how_fast_you_are", "", my_time(offset)))
            child[1].recv(0,)
            child_delay = my_time(offset)-send_time
            communication_delays.append(child_delay)    #the algorithm begins by the checking the current communication
        for child in children:                          #latency bewteen a parent and his children. As proven in the
            child[1].send(offset,message(child[2], name, "give_me_your_time", "", my_time(offset)))
            child_time_and_weight = child[1].recv(0,).data #write up the parent only needs to know the latency between him and
            times_and_weight.append(child_time_and_weight) #his direct children and only keep a count of the number of ancestors
        average_time = 0
        total_weight = 1
        for times in times_and_weight:
            average_time = average_time + (times[0]*times[1]) #he then computes a weighted average and sends the average along with
            total_weight = total_weight + times[1]            #the appropriate offset to his children who then recursively do the same
        old_time = my_time(offset)
        average_time = (average_time+old_time)/total_weight
        for j,child in enumerate(children):
            child[1].send(offset,message(child[2], name, "your_time_is", average_time + communication_delays[j], my_time(offset)))
        return old_time - average_time + offset


    if status == "follower":
        orders = parent[1].recv(0,)         #the followers algorithm is essentially the same as the parents algorithm with the exception
        if orders.command == "lets_see_how_fast_you_are": #that the child must clear the pipe of any old messages in order to avoid
            parent[1].send(offset,message(parent[2], name, "this_is_how_fast_i_am", "", my_time(offset))) #undefined behavior 
        elif orders.command == "search":
            orders = parent[1].recv(0,)
            parent[1].send(offset,message(parent[2], name, "this_is_how_fast_i_am", "", my_time(offset)))
        communication_delays = []
        times_and_weight = []
        for child in children:                        #the algorithm begins by the checking the current communication
            send_time = my_time(offset)               #latency bewteen a parent and his children. As proven in the
            child[1].send(offset,message(child[2], name, "lets_see_how_fast_you_are", "", my_time(offset)))
            child[1].recv(0,)                         #write up the parent only needs to know the latency between him and
            child_delay = my_time(offset)-send_time   #his direct children and only keep a count of the number of ancestors
            communication_delays.append(child_delay)
        for child in children:
            child[1].send(offset,message(child[2], name, "give_me_your_time", "", my_time(offset)))
            child_time_and_weight = child[1].recv(0,).data
            times_and_weight.append(child_time_and_weight)
        average_time = 0
        total_weight = 1
        for times in times_and_weight:
            average_time = average_time + (times[0]*times[1])  #he then computes a weighted average and sends the average along with
            total_weight = total_weight + times[1]             #the appropriate offset to his children who then recursively do the same
        old_time = my_time(offset)
        average_time = (average_time + old_time)/total_weight
        orders = parent[1].recv(0,)
        if orders.command == "give_me_your_time":
            parent[1].send(offset,message(parent[2], name, "my_time_is", [average_time,total_weight], my_time(offset)))
        orders = parent[1].recv(0,)
        if orders.command == "your_time_is":
            new_offset=orders.data-old_time
        for j,child in enumerate(children):
            child[1].send(offset,message(child[2], name, "your_time_is", orders.data + new_offset + communication_delays[j], my_time(offset)))
        return new_offset + offset







def my_time(offset):
    return time.clock()+offset
