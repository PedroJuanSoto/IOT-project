from postalservice import message
import time

def create_edges(name, neighbors =[]):
   edges = []
   for friend in neighbors:
       timey = time.clock()
       my_first_message = message("", name, "first", "", timey)
       friend.ssssend(my_first_message)
       new_edge = [time,friend]
       edges.append(new_edge)
   for edge in edges:
       friends_firstmessage = edge[1].rrrrecv()
       edge[1].ssssend(friends_firstmessage)
       edge.append(friends_firstmessage.fromy)
   for edge in edges:
       my_first_message_returns = edge[1].rrrrecv()
       timey = time.clock()
       timey = timey- my_first_message_returns.time
       edge[0] = timey
       my_second_message = message("", name, "second", "", timey)
       edge[1].ssssend(my_second_message)
   for edge in edges:
       friends_second_message = edge[1].rrrrecv()
       if friends_second_message.time < edge[0]:
           edge[0] = friends_second_message.time
   return edges

def find_min(neighborss =[]):
    min = 1000000000000
    if len(neighborss)==0:
        return [min]
    for friend in neighborss:
        if friend[0] < min:
            bestfriend = friend
            min = friend[0]
    return bestfriend

def find_MST(name, edges = []):
    original_name = name
    #print(name,edges)
    my_rank = 0
    miny = find_min(edges)
    #print(name,miny)
    status = "leader"
    parent = ""
    children = []
    q = 1

    love_letter = message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock())
    miny[1].ssssend(love_letter)
    mail = miny[1].rrrrecv()
    if mail.data == my_rank:         #if they both agree that they
        if  mail.fromy < name:       #are each others minedge then
            children.append(miny)    #a friendly merge occurs
            my_rank = my_rank+1      #we compare names to break potential
        elif mail.fromy > name:      #ties in leader elections
            parent = miny
            my_rank = mail.data+1
            name = mail.fromy
            status = "follower"
    elif mail.data > my_rank:
         parent = miny
         my_rank = mail.data
         name = mail.fromy
         status = "follower"
    if parent != "":
        for edge in edges:
            if parent == edge:
                #print("childish")
                edges.remove(edge)
    if len(children) != 0:
        #print("parenty", original_name)
        for edge in edges:
            if children[0] == edge:
                #print("parenty", original_name)
                edges.remove(edge)
    finished_children = []

    print("")
    print("SSSSSSSSSSSSSSSSSSS",status,"names is   ",original_name,"city is        ",name,"            parent is ",parent,"children are",children,"edges are   ",edges)
    print("")

    while len(edges)!=0 or len(children)!=0:
        q=q+1

        if status == "follower":
            orders = parent[1].recv()
            my_rank = orders.data
            name = orders.fromy
            if orders.command == "search":
                miny = find_min(edges)
                did_i_find_min = "yes"
                did_i_find_cycle_min = "no"
                did_i_find_child_cycle_min = "no"
                for child in children:                               #In this step a node looks through
                    child[1].send(message(["to",child[2],"from",original_name, "time",q], name, "search", my_rank, time.clock()))
                    mail = child[1].recv()                           #its children and checks if any

                    if mail.command == "my_min_is":                  #of them found a better edge
                        if mail.data < miny[0]:
                            if did_i_find_min == "yes":              #if NEW MIN then we must alert any
                                did_i_find_min = "no"                #update any old information
                                if did_i_find_cycle_min == "yes":    #Alert old cycle not min
                                    maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                                    did_i_find_cycle_min = "no"
                            elif did_i_find_child_cycle_min == "yes":      #Alert two child cycles not min
                                miny[1].send(cmessage(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                                did_i_find_child_cycle_min = "no"
                            else:
                                miny[1].send(message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                            miny = [mail.data, child[1],child[2]]

                        elif mail.data == miny[0]:                      #NEW CYCLE has been found. we must update
                            maybeminy = [mail.data, child[1],child[2]]  #because there is the possibilty
                            if did_i_find_min == "no":                  #of a tie and the tie can
                                did_i_find_child_cycle_min = "yes"      #be between two children
                            else:                                       #or one of the edges
                                did_i_find_cycle_min = "yes"

                        else:
                            child[1].send(message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                    if mail.command == "i_am_finished":             #one of the children could have
                        finished_children.append(child)             #run out of territory to explore
                        children.remove(child)

                if len(edges)!=0 or len(children)!=0:
                    parent[1].send(message(["to",parent[2],"from",original_name, "time",q], name, "my_min_is", miny[0], time.clock()))
                    response = parent[1].recv()
                    my_rank = response.data
                    name = response.fromy
                    if response.command == "you_are_min":
                        if did_i_find_min == "yes":
                            miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock()))
                            if did_i_find_cycle_min == "yes":
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock()))
                        elif did_i_find_min == "no":
                            miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock()))
                            if did_i_find_child_cycle_min == "yes":
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock()))

                        mail = miny[1].recv()
                        if did_i_find_cycle_min == "yes" or did_i_find_child_cycle_min == "yes":
                            mail = maybeminy[1].recv()
                        parent[1].send(mail)
                        response = parent[1].recv()
                        my_rank = response.data
                        name = response.fromy
                        if response.command == "we_lost":
                            children.append(parent)
                            if did_i_find_min == "yes":
                                parent = miny
                                for edge in edges:
                                    if parent == edge:
                                        edges.remove(edge)
                            elif did_i_find_min == "no":
                                miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock()))
                                for child in children:
                                    if miny[1] == edge[1]:
                                        parent = child
                                        children.remove(child)

                        elif response.command == "we_won":
                            if did_i_find_min == "yes":
                                children.append(miny)
                                for edge in edges:
                                    if miny == edge:
                                        edges.remove(edge)
                            elif did_i_find_min == "no":
                                miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock()))

                        elif response.command == "cycle":
                            if did_i_find_cycle_min == "yes":
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                for edge in edges:
                                    if miny == edge:
                                        edges.remove(edge)
                            elif did_i_find_child_cycle_min == "yes":
                                miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                            else:
                                miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))

                    elif response.command == "you_are_not_min":
                        if did_i_find_min == "no":
                            miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                        if did_i_find_cycle_min == "yes" or did_i_find_child_cycle_min == "yes":
                            maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))



        if status == "leader":
            miny = find_min(edges)
            did_i_find_min = "yes"
            did_i_find_cycle_min = "no"
            did_i_find_child_cycle_min = "no"
            for child in children:                                   #In this step a node looks through
                child[1].send(message(["to",child[2],"from",original_name, "time",q], name, "search", my_rank, time.clock()))
                mail = child[1].recv()                               #its children and checks if any

                if mail.command == "my_min_is":                      #of them found a better edge
                    if mail.data < miny[0]:
                        if did_i_find_min == "yes":                  #if NEW MIN then we must alert any
                            did_i_find_min = "no"                    #update any old information
                            if did_i_find_cycle_min == "yes":        #Alert old cycle not min
                                maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                                did_i_find_cycle_min = "no"

                        elif did_i_find_child_cycle_min == "yes":    #Alert two child cycles not min
                            miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                            maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                            did_i_find_child_cycle_min = "no"

                        else:
                            miny[1].send(message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))
                        miny = [mail.data, child[1],child[2]]

                    elif mail.data == miny[0]:                      #NEW CYCLE has been found. we must update
                        maybeminy = [mail.data, child[1],child[2]]  #because there is the possibilty
                        if did_i_find_min == "no":                  #of a tie and the tie can
                            did_i_find_child_cycle_min = "yes"      #be between two children
                        else:                                       #or one of the edges
                            did_i_find_cycle_min = "yes"
                    else:
                        child[1].send(message(["to",child[2],"from",original_name, "time",q], name, "you_are_not_min", my_rank, time.clock()))

                if mail.command == "i_am_finished":                 #one of the children could have
                    finished_children.append(child)                 #run out of territory to explore
                    children.remove(child)

            if len(edges)!=0 or len(children)!=0:
                if did_i_find_min == "yes":
                    love_letter = message(["to",miny[2],"from",original_name, "time",q], name, "i_choose_you", my_rank, time.clock())
                    miny[1].send(love_letter)
                    if did_i_find_cycle_min == "yes":
                        command = message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock())
                        maybeminy[1].send(command)
                elif did_i_find_min == "no":
                    command = message(["to",miny[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock())
                    miny[1].send(command)
                    if did_i_find_child_cycle_min == "yes":
                        command = message(["to",maybeminy[2],"from",original_name, "time",q], name, "you_are_min", my_rank, time.clock())
                        maybeminy[1].send(command)

                mail = miny[1].recv()
                if did_i_find_cycle_min == "yes" or did_i_find_child_cycle_min == "yes":
                    mail = maybeminy[1].recv()

                if mail.fromy == name:
                    if did_i_find_cycle_min == "yes":
                        maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                        for edge in edges:
                            if miny == edge:
                                edges.remove(edge)
                    elif did_i_find_child_cycle_min == "yes":
                        miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                        maybeminy[1].send(message(["to",maybeminy[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))
                    else:
                        miny[1].send(message(["to",miny[2],"from",original_name, "time",q], name, "cycle", my_rank, time.clock()))


                elif mail.data == my_rank:
                    if  mail.fromy < name:
                        if did_i_find_min == "yes":
                            children.append(miny)
                            my_rank = my_rank+1
                            for edge in edges:
                                if edge == miny:
                                    edges.remove(edge)
                        elif did_i_find_min == "no":
                            command = message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock())
                            miny[1].send(command)
                    elif mail.fromy > name:
                        parent = miny
                        my_rank = mail.data+1
                        name = mail.fromy
                        status = "follower"
                        if did_i_find_min == "yes":
                            for edge in edges:
                                if edge == miny:
                                    edges.remove(edge)
                        if did_i_find_min == "no":
                            command = message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock())
                            miny[1].send(command)
                elif mail.data > my_rank:
                    parent = miny
                    my_rank = mail.data+1
                    name = mail.fromy
                    status = "follower"
                    if did_i_find_min == "yes":
                        for edge in edges:
                            if edge == miny:
                                edges.remove(edge)
                    if did_i_find_min == "no":
                        command = message(["to",miny[2],"from",original_name, "time",q], name, "we_lost", my_rank, time.clock())
                        miny[1].send(command)
                elif  mail.data < my_rank:
                    if did_i_find_min == "yes":
                        children.append(miny)
                        for edge in edges:
                            if edge == miny:
                                edges.remove(edge)
                    elif did_i_find_min == "no":
                        command = message(["to",miny[2],"from",original_name, "time",q], name, "we_won", my_rank, time.clock())
                        miny[1].send(command)
                if parent != "":
                    for edge in edges:
                        if parent == edge:
                            edges.remove(edge)
                    for child in children:
                        if parent == child:
                            children.remove(child)

    if status == "follower":
        letter_of_resignation = message(["to",parent[2],"from",original_name, "time",q], name, "i_am_finished", my_rank, time.clock())
        parent[1].send(letter_of_resignation)






    # while len(edges)!=0:
    #     miny = find_min(edges)
    #     love_letter = message("", name, "i_choose_you", my_rank, time.clock())
    #     miny[1].send(love_letter)
    #     edges.remove(miny)
    # # print("names is   ",original_name,"parent is",name,"  ",parent,"children are   ",children,"edges are   ",edges)
    # return [parent,children]
