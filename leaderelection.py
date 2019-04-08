from postalservice import message
import time
import random

def create_edges(name, seedy,neighbors =[]):      #In order to perform "A Distributed Algorithm for
   random.seed(2**seedy)                          #Spanning Trees " by R. G. GALLAGER we need
   edges = []                                     #to give the edges weights that are equal to the
   for friend in neighbors:                       #communication delay between two processes
       timey = time.clock()                       #In order to avoid complications I added a little tiny bit
       my_first_message = message("", name, "first", "", timey) #of random noise (because random.random() \in (0,1)) 
       friend.ssssend(0,my_first_message)         #to avoid having two edges with the same weights,
       new_edge = [time,friend]                   #further we pick the larger of the two delays or else
       edges.append(new_edge)                     #we would have to implement a directed edge
   for edge in edges:                             #algorithm (which is easy but tedious)
       friends_firstmessage = edge[1].rrrrecv(0)
       edge[1].ssssend(0,friends_firstmessage)
       edge.append(friends_firstmessage.fromy)
   for edge in edges:
       my_first_message_returns = edge[1].rrrrecv(0)
       timey = time.clock()                      #I had to force the noise to have an exponential effect or
       timey = 2**( random.random()*(timey- my_first_message_returns.time))#else there is a small chance that
       edge[0] = timey                           #two edges have the same weight creating errors
       my_second_message = message("", name, "second", "", timey)
       edge[1].ssssend(0,my_second_message)
   for edge in edges:
       friends_second_message = edge[1].rrrrecv(0)
       if friends_second_message.time > edge[0]:  #We take the larger of the two comunication delays
           edge[0] = friends_second_message.time  #as the weight of the edge
   return edges

def find_min(neighborss =[]):
    min = 1000000000000          #find_min() finds the minimum edge in the edge list and
    if len(neighborss)==0:       #returns it if it exists, if it does not exist then it returns
        return [min]             #a list with one item which can be conviniently used in find_MST()
    for friend in neighborss:    #to check if both the edge and "child" list is empty
        if friend[0] < min:      #This is because if a min exists it will return length 3
            bestfriend = friend  #list of the form [minedgeweight, minedge, name of adjacent node]
            min = friend[0]
    return bestfriend

def find_MST(name, edges = []):
    original_name = name       #Find_MST employs the famous algorithm from "A Distributed Algorithm for
    my_rank = 0                #Spanning Trees " by R. G. GALLAGER to find the minimum spaaning tree
    miny = find_min(edges)     #for the network and while simaltanously electing a leader.
    status = "leader"          #The name data type keeps the name of the village or city of the node
    parent = ""                #miny is the current best minimum edge, status is whether the node is
    children = []              #currently a leader or follower, parent is the node's parent (if any)
    q = 1                      #and children is the nodes children (if any)

    love_letter = message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock())
    miny[1].send(0,love_letter)     #the algorithm begins with every node picking their min edge and wating to be picked in return
    mail = miny[1].recv(0,)
    if mail.data == my_rank:         #if they both agree that they
        if  mail.fromy < name:       #are each others minedge then
            children.append(miny)    #a friendly merge occurs
            my_rank = my_rank+1      #we compare names to break potential
        elif mail.fromy > name:      #ties in leader elections
            parent = miny
            my_rank = mail.data+1    #ties are broken with names
            name = mail.fromy
            status = "follower"
    elif mail.data > my_rank:        #if the other city/village has a higher rank then
         parent = miny               #the city is absorbed and it changes its name
         my_rank = mail.data         #and rank to the other cities name and rank
         name = mail.fromy
         status = "follower"
    if parent != "":                #the edge list must be updating by deleting edges
        for edge in edges:          #that have become children or parents
            if parent == edge:
                edges.remove(edge)
    if len(children) != 0:
        for edge in edges:
            if children[0] == edge:
                edges.remove(edge)
    finished_children = []          #this keeps track of the children that are finished and is
                                    #returned by find_MST()
    print("NEW NODE AWOKEN!!!",status,"names is   ",original_name,"city is        ",name,"            parent is ",parent,"children are",children,"edges are   ",edges)

    while len(edges)!=0 or len(children)!=0:
        q=q+1

        if status == "follower":
            orders = parent[1].recv(0,)     #a follower node awaits instructions from its parent
            my_rank = orders.data           #node and constantly updates its name and rank to
            name = orders.fromy             #that of the city it is currently part of

            if orders.command == "search":
                miny = find_min(edges)      #the search message begins a sequence of questions and answers
                did_i_find_min = "yes"      #between a parent node and a child node. Every node "searches" for its
                did_i_find_cycle = "no"     #min by looking through its edges and asking each of their children for
                j=0                         #their min. did_i_find_min is equal to yes if the min is an edge
                while j < len(children):    #and is equal to no if one of the edges is a min. did_i_find_cycle indicates
                    child = children[j]     #whether a cycle was found
                    j=j+1
                    if did_i_find_cycle == "no":
                        child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "search", my_rank, time.clock()))
                        mail = child[1].recv(0,)                #In this step a node looks through
                        if mail.command == "my_min_is":         #its children and checks if any
                            if mail.data < miny[0]:             #of them found a better edge
                                if did_i_find_min == "yes":     #if NEW MIN then we must
                                    did_i_find_min = "no"       #update any old information and
                                else:                           #inform the old min that the are not a min
                                    miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                                oldminy = miny
                                miny = [mail.data, child[1],child[2]]

                            elif mail.data == miny[0]:          #because all edges have been forced to have different
                                did_i_find_cycle = "yes"        #weights this boolean implies NEW CYCLE has been found.
                                if did_i_find_min == "no":      #we must inform any children of the cycle
                                    miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                    child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                    miny = oldminy              #we must return to the old min if a cycle was found
                                else:
                                    child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                    for edge in edges:          #if one of the min was actually found by this node
                                        if miny == edge:        #then this node must delete this edge
                                            edges.remove(edge)
                                    miny = find_min(edges)
                                for edge in edges:              #this returns the state of the found min to the
                                    if miny == edge:            #previous correct state before a cycle was found
                                        did_i_find_min = "yes"
                                if len(miny) == 1:
                                    did_i_find_min = "yes"
                            else:                               #we must inform any children if they are not min
                                child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                        if mail.command == "i_am_finished":     #one of the children has
                            finished_children.append(child)     #run out of territory to explore
                            children.remove(child)              #we place them in the finished list
                            j=j-1

                        if mail.command == "cycle":       #if one of the children found a cycle we
                            alert_min = "yes"             #must tell the parent because every phase must be
                            for edge in edges:            #synchronized so as to not create any
                                if miny == edge:          #the leader will later restart the next phase
                                    alert_min == "no"     #with a search command
                            did_i_find_cycle = "yes"
                            if len(miny) != 1:
                                if alert_min == "yes":
                                    miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                if did_i_find_cycle == "yes":          #The child alerts the parent of any cycles
                    parent[1].send(0,message(["to",parent[2],"from",original_name, "time",q], name, "cycle", miny[0], time.clock()))

                elif len(edges)!=0 or len(children)!=0:
                    parent[1].send(0,message(["to",parent[2],"from",original_name, "time",q], name, "my_min_is", miny[0], time.clock()))
                    response = parent[1].recv(0,)     #The chld now waits to update any information
                    my_rank = response.data           #about the city rank and/or name and also whats
                    name = response.fromy             #its next command is
                    if response.command == "you_are_min":
                        if did_i_find_min == "yes":        #If the parent alerts you that you are min
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock()))
                                                           #you try to merge with the city/or village by sending it a
                        elif did_i_find_min == "no":       #and waiting for a response
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock()))


                        mail = miny[1].recv(0,)            #when the other village/city responds
                        parent[1].send(0,mail)             #to the request to merge you then send the
                        response = parent[1].recv(0,)      #up to your parent(leader) who will
                        my_rank = response.data            #then inform you of the next move
                        name = response.fromy
                        if response.command == "we_lost":  #if the neighboring city is stronger
                            children.append(parent)        #then the current city of this node was
                            if did_i_find_min == "yes":    #absorbed by a larger city and therefore
                                parent = miny              #the order of communication is now reversed
                                for edge in edges:         #and therefore the parent becomes the child
                                    if parent == edge:
                                        edges.remove(edge) #the new node becomes the new parent of this node
                            elif did_i_find_min == "no":   #and this node must update other information
                                miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock()))
                                for child in children:     #such as deleting old nodes
                                    if miny[2] == child[2]:
                                        parent = child
                                        children.remove(child)


                        elif response.command == "we_won": #if the neighboring city is stronger
                            if did_i_find_min == "yes":    #then node appends the new city as one
                                children.append(miny)      #of its children and updates its edge list
                                for edge in edges:
                                    if miny == edge:
                                        edges.remove(edge)
                            elif did_i_find_min == "no":
                                miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock()))

                    elif response.command == "cycle":    #if the parent reports that the new min that this node
                        if did_i_find_min == "yes":      #found is a cycle then it must be deleted from the list
                            for edge in edges:           #or if did_i_find_min == "no" then this node will send the
                                if miny == edge:         #message down to its children and eventually by recursion a
                                    edges.remove(edge)   #solution will be found
                        elif did_i_find_min == "no":
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))


                    elif response.command == "you_are_not_min": #if the  child is not a min it then goes back to the top
                        if did_i_find_min == "no":              #of the loop and awaits a search command from its parent
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                    #the leader routine starts here. the leader commences all phases in a city by issuing a search command.
                    #the find min process is similar to a follower but eventually the leader is the only node allowed to make "decisions"
        if status == "leader":
            miny = find_min(edges)    #the search message begins a sequence of questions and answers
            did_i_find_min = "yes"    #between a parent node and a child node. Every node "searches" for its
            did_i_find_cycle = "no"   #min by looking through its edges and asking each of their children for
                                      #their min. did_i_find_min is equal to yes if the min is an edge
            j=0                       #and is equal to no if one of the edges is a min. did_i_find_cycle indicates
            while j < len(children):  #whether a cycle was found
                child = children[j]
                j=j+1

                if did_i_find_cycle == "no":
                    child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "search", my_rank, time.clock()))
                    mail = child[1].recv(0,)               #In this step a node looks through
                                                           #its children and checks if any
                    if mail.command == "my_min_is":        #of them found a better edge
                        if mail.data < miny[0]:            #if NEW MIN then we must
                            if did_i_find_min == "yes":    #update any old information and
                                did_i_find_min = "no"      #inform the old min that the are not a min
                            else:
                                miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                            oldminy = miny
                            miny = [mail.data, child[1],child[2]]
                        elif mail.data == miny[0]:         #because all edges have been forced to have different
                            did_i_find_cycle = "yes"       #weights this boolean implies NEW CYCLE has been found.
                            if did_i_find_min == "no":     #we must inform any children of the cycle
                                miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                miny = oldminy             #we must return to the old min if a cycle was found
                            else:
                                child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                for edge in edges:         #if one of the min was actually found by this node
                                    if miny == edge:       #then this node must delete this edge
                                        edges.remove(edge)
                                miny = find_min(edges)
                            for edge in edges:
                                if miny == edge:           #this returns the state of the found min to the
                                    did_i_find_min = "yes" #previous correct state before a cycle was found
                            if len(miny) == 1:
                                did_i_find_min = "yes"
                        else:
                            child[1].send(0,message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                    if mail.command == "i_am_finished":             #one of the children has
                        finished_children.append(child)             #run out of territory to explore
                        children.remove(child)                      #we place them in the finished list
                        j=j-1

                    if mail.command == "cycle":        #if one of the children found a cycle we
                        alert_min = "yes"              #must tell the parent because every phase must be
                        for edge in edges:             #synchronized so as to not create any
                            if miny == edge:           #the leader will later restart the next phase
                                alert_min == "no"      #with a search command
                        did_i_find_cycle = "yes"
                        if len(miny) != 1:
                            if alert_min == "yes":
                                miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

            if len(miny) == 1:                 #This checks if there is a miny. As stated previously find_min()
                pass                           #returns a singleton if there is no min

            elif did_i_find_cycle == "yes":    #If did_I_find cycle is true then we must restart a new phase
                pass

            elif len(edges)!=0 or len(children)!=0:  #If the leader node found the min then he/she will broadcast the desire to
                if did_i_find_min == "yes":          #merge to the adjacent node and await a response
                    miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock()))
                elif did_i_find_min == "no":         #If the leader did not find the min then he broadcasts to the min edge to merge and that broadcast
                    miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock()))
                                                     #will be recursively sent down the city-tree until it arrives at the desired node
                mail = miny[1].recv(0,)
                        #The leader then awaits a response from a min edge and then makes a decision based on the response

                if mail.data == my_rank:  #If the rank of the city/village on the adjacent edge is equal then
                                          #a merge occurs
                    if  mail.fromy < name:
                        if did_i_find_min == "yes":   #A tie is broken by lexicographic order of city names
                            children.append(miny)
                            my_rank = my_rank+1       #If a merger of two equal sized cities occurs then they must
                            for edge in edges:        #increase the rank by one
                                if edge == miny:
                                    edges.remove(edge)   #Then update the list

                        elif did_i_find_min == "no":    #If the leader did not find the min then he sends a message to the relevant nodes
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock()))
                                                        #letting them know what action to take
                    elif mail.fromy > name:
                        my_rank = mail.data+1
                        name = mail.fromy       #if the leader loses the tie he then makes the min
                        status = "follower"     #he takes the name of the min's city and then he ...

                        if did_i_find_min == "yes":   #...he then makes the min his parent if he found min
                            parent = miny             # and he updates his edge list or ...
                            for edge in edges:
                                if edge == miny:
                                    edges.remove(edge)
                                                     #... if he did not find the min then he procedes he makes the min child his parent and
                        if did_i_find_min == "no":   #sends a "we lost" broadcest to his child which propagates downward to the relevant nodes
                            miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock()))
                            for child in children:
                                if miny[2] == child[2]:
                                    parent = child
                                    children.remove(child)

                elif mail.data > my_rank:
                    my_rank = mail.data
                    name = mail.fromy
                    status = "follower"

                    if did_i_find_min == "yes":       #Similalry if a city with a larger rank is on
                        parent = miny                 #the other side of the communication then the
                        for edge in edges:            #leader makes the min his parent and broadcasts
                            if edge == miny:          #the "we lost" message down to all the relevant nodes
                                edges.remove(edge)    #but the rank is not increased this time around

                    if did_i_find_min == "no":
                        miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock()))
                        for child in children:
                            if miny[2] == child[2]:
                                parent = child
                                children.remove(child)

                elif  mail.data < my_rank:               #If the rank is smaller then we absorb the
                    if did_i_find_min == "yes":          #smaller city and very little updates need to
                        children.append(miny)            #made. The rank stays the same and we just delete
                        for edge in edges:               #the edge and turn into a chlid edge
                            if edge == miny:
                                edges.remove(edge)

                    elif did_i_find_min == "no":
                        miny[1].send(0,message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock()))

                              #finally if a follower finishes he alerts his parent and when everyone is finsihed they return with the
    if status == "follower":  #updated child paretn structure of minimum spanning tree with a unique leader which has a small amount of communication overhead
        letter_of_resignation = message(["to",parent[2],"from",original_name, "time",q], name, "i_am_finished", my_rank, time.clock())
        parent[1].send(0,letter_of_resignation)


    print("I AM FINISHED",parent, finished_children, status)
    return parent, finished_children, status
