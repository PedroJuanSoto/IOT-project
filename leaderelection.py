from postalservice import message
import time

def create_edges(name, neighbors =[]):
   edges = []
   for friend in neighbors:
       timey = time.clock()
       my_first_message = message("", name, "first", "", timey)
       friend.send(my_first_message)
       new_edge = [time,friend]
       edges.append(new_edge)
   for edge in edges:
       friends_firstmessage = edge[1].recv()
       edge[1].send(friends_firstmessage)
   for edge in edges:
       my_first_message_returns = edge[1].recv()
       timey = time.clock()
       timey = timey- my_first_message_returns.time
       edge[0] = timey
       my_second_message = message("", name, "second", "", timey)
       edge[1].send(my_second_message)
   for edge in edges:
       friends_second_message = edge[1].recv()
       if friends_second_message.time < edge[0]:
           edge[0] = friends_second_message.time
   return edges

def find_min(neighborss =[]):
    min = 100000000000
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
    love_letter = message("", name, "i_choose_you", my_rank, time.clock())
    miny[1].send(love_letter)
    mail = miny[1].recv()
    if mail.data == my_rank:         #if they both agree that they
        if  mail.fromy < name:       #are each others minedge then
            children.append(miny)    #a friendly merge occurs
            my_rank = my_rank+1      #we compare names to break potential
        elif mail.fromy > name:      #ties in leader elections
            parent = miny
            my_rank = mail.data+1
            name = mail.fromy
            status == "follower"
    elif mail.data > my_rank:
         parent = miny
         my_rank = mail.data
         name = mail.fromy
         status == "follower"
    if parent != "":
        for edge in edges:
            if parent == edge:
                edges.remove(edge)
    if len(children) != 0:
        for edge in edges:
            if children[0] == edge:
                edges.remove(edge)
    # finished_children = []
    # print("names is   ",original_name,"parent is",name,"  ",parent,"children are   ",children,"edges are   ",edges)
    # while len(edges)!=0 or len(children)!=0:
    #     miny = find_min(edges)
    #     did_i_find_min = "yes"
    #     for child in children:                 #In this step a node looks through
    #         mail = child[1].recv()             #its children and checks if any
    #         if mail.command == "my_min_is":    #of them found a better edge
    #             if mail.data < miny[0]:
    #                 miny = [mail.data, child[1]]
    #                 did_i_find_min = "no"      #the node lets the child no if they
    #             else:                          #found a poor solution
    #                 command = message("", name, "you_are_not_min", my_rank, time.clock())
    #                 miny[1].send(command)
    #         if mail.command == "i_am_finished":     #one of the children could have
    #             finished_children.append(child)     #run out of territory to explore
    #             children.remove(child)
    #     if status == "follower":
    #         my_min_is = message("", name, "my_min_is", miny[0], time.clock())
    #         parent[1].send(my_min_is)
    #         response = parent[1].recv()
    #         if response.command == "you_are_min":
    #             my_rank = response.data
    #             name = response.fromy
    #             if did_i_find_min == "yes":
    #                 love_letter = message("", name, "i_choose_you", my_rank, time.clock())
    #                 miny[1].send(love_letter)
    #             elif did_i_find_min == "no":
    #                 command = message("", name, "you_are_min", my_rank, time.clock())
    #                 miny[1].send(command)
    #             mail = miny[1].recv()
    #             if mail.fromy!=name:
    #                 if mail.data == my_rank:
    #                     if  mail.fromy < name:       #We now repeat the same merger
    #                         children.append(miny)    #process from the first
    #                         my_rank = my_rank+1      #part of find_MST
    #                         parent[1].send(mail)     #With the exception that the node
    #                     elif mail.fromy > name:      #must now notify its respective
    #                         parent[1].send(mail)     #parent about what is happening
    #                         parent = miny
    #                         my_rank = mail.data+1
    #                         name = mail.fromy
    #                         status == "follower"
    #                     if did_i_find_min == "yes":  #We must also update our edge
    #                         edges.remove(miny)       #and children list
    #                     elif did_i_find_min == "no":
    #                         for child in children:
    #                             if child[1] == miny[1]:
    #                                 children.remove(child)
    #                 elif mail.data < my_rank:
    #                      children.append(miny)
    #                 elif mail.data > my_rank:
    #                      parent = miny
    #                      my_rank = mail.data+1
    #                      name = mail.fromy
    #                      status == "follower"
    #             if mail.fromy==name and mail.command == "i_choose_you":
    #                 parent[1].send(mail)            #This if branch takes care of
    #                 if did_i_find_min == "yes":     #the case where we have created
    #                     edges.remove(miny)          #a cycle. We know this happend if the
    #                 elif did_i_find_min == "no":    #if they have the same because
    #                     for child in children:      #we created two paths to the
    #                         if child[1] == miny[1]: #same node
    #                             children.remove(child)
    #         if response.command == "you_are_not_min":
    #             my_rank = response.data
    #             name = response.fromy
    #             if did_i_find_min == "yes":
    #                 pass
    #             elif did_i_find_min == "no":
    #                 command = message("", name, "you_are_not_min", my_rank, time.clock())
    #                 miny[1].send(command)
    #     elif status == "leader":
    #         if did_i_find_min == "yes":
    #             love_letter = message("", name, "i_choose_you", my_rank, time.clock())
    #             miny[1].send(love_letter)
    #         elif did_i_find_min == "no":
    #             command = message("", name, "you_are_min", my_rank, time.clock())
    #             miny[1].send(command)
    #         mail = miny[1].recv()
    #         if mail.data == my_rank:
    #             if  mail.fromy < name:       #We now repeat the same merger
    #                 children.append(miny)    #process from follower merger
    #                 my_rank = my_rank+1      #With the exception that the node
    #             elif mail.fromy > name:      #does not have to notify its parent
    #                 parent = miny            #about what is happening
    #                 my_rank = mail.data+1    #beacause a leader has no perent
    #                 name = mail.fromy
    #                 status == "follower"
    #             if did_i_find_min == "yes":
    #                 edges.remove(miny)
    #             elif did_i_find_min == "no":
    #                 for child in children:
    #                     if child[1] == miny[1]:
    #                         children.remove(child)
    # print(original_name,parent,finished_children)
    # return [parent,finished_children]
    while len(edges)!=0:
        miny = find_min(edges)
        love_letter = message("", name, "i_choose_you", my_rank, time.clock())
        miny[1].send(love_letter)
        edges.remove(miny)
    print("names is   ",original_name,"parent is",name,"  ",parent,"children are   ",children,"edges are   ",edges)
    return [parent,children]
