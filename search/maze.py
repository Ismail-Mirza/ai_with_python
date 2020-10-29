import sys
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
class StackFrontier():
    def __init__(self):
        self.frontier=[]

    #add explored node to the frontier
    def add(self,node):
        self.frontier.append(node)
    #justify that any state already in the frontier
    def contains_state(self,state):
        return any(node.state==state for node in self.frontier) #return true of state alredy in frontier
    def empty(self):
        return  len(self.frontier) == 0
    #remove node from frontier if the node is not the goal
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        #as stack is first in last out database it remove nodes from the last of list

        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
#make maze from the input file
class maze(object):
    """docstring fo maze."""

    def __init__(self, filename):
        with open(filename) as inp:
            contents=inp.read()
        #Validate start and Goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents=contents.splitlines()
        #get the height and width of Maze
        self.height=len(contents)
        self.width=max(len(line) for line in contents) #get the max line as the width of Maze
        #keep track of walls in maze ,goal and start
        self.walls=[]
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j]=='A':
                        self.start=(i,j)
                    elif contents[i][j]=="B":
                        self.end=(i,j)
                    elif contents[i][j] !=" ":
                        row.append(True)
                        continue
                    row.append(False)
                except IndexError:
                    row.append(False)
                    break
            self.walls.append(row)
        #append intial solution
        self.solution=None
    def print(self):
        solution= self.solution[1] if self.solution is not None else None
        for i , row in enumerate(self.walls):
            for j,block in enumerate(row):
                if block:
                    print("█",end="")
                elif (i,j) == self.start:
                    print("A",end="")
                elif (i,j) == self.end:
                    print("B",end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ",end="")

            print()
    def neighbors(self,state):
        x,y=state
        candidates=[
            ('up',(x-1,y)),
            ('down',(x+1,y)),
            ('right',(x,y+1)),
            ('left',(x,y-1))
        ]
        result=[]
        for action,(r,c) in candidates:
            if 0 <= r <self.height and 0 <=c<self.width and not self.walls[r][c]:
                result.append((action,(r,c)))
        return result

    #solve maze
    def solve(self):
        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()
        while True:
            if frontier.empty():
                raise Exception("No solution")
            #than remove a node from the frontier
            node =frontier.remove()
            #already explored is the removed node
            self.num_explored += 1
            if node.state == self.end:
                #if we find the goal we we have to find the action and the path that has needed to reached the Goal
                actions=[]
                path=[]
                #if child not parent node thake than looping continue hobe
                while node.parent is not None:
                    actions.append(node.action)
                    path.append(node.state)
                    node=node.parent
                actions.reverse()
                path.reverse()
                self.solution=(actions,path)
                return

            self.explored.add(node.state)
            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                #if new state already in frontier or in the explored set than we did not to add new state in the frontier
                #if not than the loop will be infinite bcz
                if  not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
    def print_explored(self):
        solution= self.solution[1] if self.solution is not None else None
        for i , row in enumerate(self.walls):
            for j,block in enumerate(row):
                if block:
                    print("█",end="")
                elif (i,j) == self.start:
                    print("A",end="")
                elif (i,j) == self.end:
                    print("B",end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                elif (i,j) in self.explored:
                    print("-",end="")
                else:
                    print(" ",end="")

            print()


m = maze('maze2.txt')
print("Maze:")
m.print()
print("Solving...\n\n")
m.solve()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
print("Explored:")
m.print_explored()
