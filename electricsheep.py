from postalservice import message, mailbox


def create_edges(name, neighbors =[]):
   edges = []
   for friend in neighbors:
       time = friend.timestamp()
       sending = message("", name, "sending1", "", time)
       friend.deliver_mail(sending)
       new_edge = [time,friend]
       edges.append(new_edge)
   tasks = 0
   while tasks < len(neighbors):
       for j,friend in enumerate(neighbors):
           mail = friend.check_mail()
           if mail!=-1:
               if mail.fromy==name:
                   friend.deliver_mail(mail)
               elif mail.command=="sending1":
                   sending = message("", name, "sending2", "", time)
                   friend.deliver_mail(sending)
               elif mail.command=="sending2":
                   newtime = friend.timestamp()
                   edges[j][0]=newtime-edges[j][0]
   return edges

def create_edges(name, neighborss =[]):
    edges = []
    for k,friend in enumerate(neighborss):
        heythere = [1,friend]
        edges.append(heythere)
    return edges

def find_min(neighborss =[]):
    min = 100000000000
    for j,friend in enumerate(neighborss):
        if friend[0] < min:
            bestfriend = friend
            min = friend[0]
    return bestfriend

def ffind_MST(name, edges = []):
    miny = find_min(edges)
    return miny

def find_MST(name, edges = []):
    my_rank = [0, len(edges)]
    miny = find_min(edges)
    status = "leader"
    parent = ""
    children = []
    for z in range(10):
        #while status == "leader" and my_rank==0:
            love_letter = message("", name, "i_choose_you", my_rank, miny[1].timestamp())
            miny[1].deliver_mail(love_letter)
            mailbag = []
            for edge in edges:
                mail =edge[1].check_mail()
                if mail!=-1:
                    if edge[1] == miny[1] and  mail.command == "i_choose_you":
                        if mail.data[0] == my_rank:         #if they both agree that they
                            if  mail.data[1] < my_rank[1]:     #are each others minedge then
                                children.append(edge)             #a friendly merge occurs
                                my_rank = my_rank+1
                            elif mail.data[1] > my_rank[1]:
                                parent = edge
                                my_rank = mail.data[0]+1 #most of these if elif statements
                                name = mail.fromy           #are a way of breaking a tie in
                                status == "follower"        #leader selection
                            else:
                                if  mail.fromy < name:
                                    children.append(edge)
                                    my_rank = my_rank+1
                                elif mail.fromy > name:
                                    parent = edge
                                    my_rank = mail.data[0]+1
                                    name = mail.fromy
                                    status == "follower"
                        elif mail.data[0] < my_rank:
                             children.append(edge)
                             my_rank = my_rank+1
                        elif mail.data[0] > my_rank:
                             parent = edge
                             my_rank = mail.data[0]+1
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
    while len(edges)!=0:
        cycles = []
        for edge in edges:
            mail =edge[1].check_mail()
            if mail!=-1:
                if mail.command == "i_choose_you" and mail.data[0] < my_rank:
                    if mail.name != name:
                        children.append(edge)             #an absorbtion occurs if they the
                        my_rank = my_rank+1         #other city is smaller
                        love_letter = message("", name, "i_choose_you", my_rank, miny[1].timestamp())
                        miny[1].deliver_mail(love_letter)
                    else:
                        cycles.append(edge)
                        love_letter = message("", name, "i_choose_you", my_rank, miny[1].timestamp())
                        miny[1].deliver_mail(love_letter)
        for w in cycles:
            edges.remove(w)
        miny = find_min(edges)
        did_i_find_min = "yes"
        for child in children:
            mail =child[1].check_mail()
            if mail!=-1:
                if mail.command == "my_min_is" and mail.data < miny[0]:
                    miny = [mail.data, child[1]]
                    did_i_find_min = "no"
        if status == "follower":
            love_letter = message("", name, "my_min_is", miny[0], miny[1].timestamp())
            parent[1].deliver_mail(love_letter)
            response = parent[1].wait_on_mail()
            if response.command == "you_are_min":
                my_rank = response.data
                name = response.fromy
                if did_i_find_min == "yes":
                    love_letter = message("", name, "i_choose_you", my_rank, miny[1].timestamp())
                    miny[1].deliver_mail(love_letter)
                elif did_i_find_min == "no":
                    command = message("", name, "you_are_min", my_rank, miny[1].timestamp())
                    miny[1].deliver_mail(command)
            if response.command == "you_are_not_min":
                my_rank = response.data
                name = response.fromy
                if did_i_find_min == "yes":
                    pass
                elif did_i_find_min == "no":
                    command = message("", name, "you_are_not_min", my_rank, miny[1].timestamp())
                    miny[1].deliver_mail(command)
        elif status == "leader":
            if did_i_find_min == "yes":
                love_letter = message("", name, "i_choose_you", my_rank, miny[1].timestamp())
                miny[1].deliver_mail(love_letter)
            elif did_i_find_min == "no":
                command = message("", name, "you_are_min", my_rank, miny[1].timestamp())
                miny[1].deliver_mail(command)
        for child in children:
            if miny[1] != child[1]:
                command = message("", name, "you_are_not_min", my_rank, miny[1].timestamp())
                miny[1].deliver_mail(command)
