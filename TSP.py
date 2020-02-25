import math
import matplotlib.pyplot as plt
import chardet
import pandas as pd

with open(r"C:\Users\Ankit\Desktop\tour17.csv", 'rb') as f: #change path accordingly
    result = chardet.detect(f.read()) #to detect the encoding of csv file
#change path accordingly
df=pd.read_csv(r"C:\Users\Ankit\Desktop\tour17.csv",encoding=result['encoding'],error_bad_lines=False,sep=';', header=None)#the file is stored in veriable df
def csv_to_list():# function to convert csv to list
    cities = [[0 for x in range(3)] for y in range(len(df[0]))]
    for i in range(len(df[0])):
        cities[i][0] = df[0][i]
    for i in range(len(df[1])):
        cities[i][1] = df[1][i]
    for i in range(len(df[2])):
        cities[i][2] = df[2][i]
    return cities#returs a list with name,x,y coordinates of cities
cities = csv_to_list() # comment this line if csv file not present
#######if file is not there use the below list of cities just uncomment the lines below - this data is from tour 17########

#cities = [['Albany', 43, 25], ['Athens', 23, 3], ['Chicago', 16, 22],
          #['Cincinnati', 22, 19], ['Huntsville',9, 21],['Indianapolis',19,19],['Jackson',5,9],
          #['Louisville',20,16],['Madison',19,9],['Nashville',18,13],['New York',42,20],
          #['Ocean city',17,40],['Ottawa',40,30],['Quebec, CA',44,31],['Richmond',36,15],
          #['Syracuse',41,27],['Worcester',45,23]]



def getdistance(x1, y1, x2, y2): #getting the distance between cities - input xy coordinates of 2cities output - distance
    a = math.sqrt(((abs(y2 - y1)) ** 2) + ((abs(x2 - x1)) ** 2))
    a = round(a,2)
    return a

def distmat(cities): #creates a distance matrix nxn of cities as nodes
    no_of_cities = len(cities)
    k = [[0 for x in range(no_of_cities)] for y in range(no_of_cities)]#zero nxn matrix
    for i in range(no_of_cities):
        for j in range(no_of_cities):
            p = getdistance(cities[i][1], cities[i][2], cities[j][1], cities[j][2])
            k[i][j] = p
    return k#distance matrix
print("The distance matrix between cities is ")
print(distmat(cities))

def greedyTSP(dmat,sourcenode):#this is the function which takes the distance matrix dmat and the source node and outputs the next nodes as a list, the end node
    #and the distance travelled between the nodes
    sol = []# list to add for visited cities
    temp_dist = dmat#matrix of distances
    tot_dist = 0 #distance travelled
    x = sourcenode#initial node
    for j in temp_dist:
        j[x] = 0#source node coloumn values 0
    sol.append(x)#adding source node to visited
    h = len(temp_dist)
    for e in range(h, 1, -1):
        #print(temp_dist)
        m = min(l for l in temp_dist[x] if l > 0)#finding minimum distance to nextnode other than 0
        tot_dist = tot_dist + m #adding the distance
        #print(m)
        s = temp_dist[x].index(m)
        #print(s)
        if s not in sol:#if nexxt node not visited add to visited
            sol.append(s)
        for w in temp_dist:#next node coloumn distances 0 so that they are not visited again
            w[s] = 0
        #print(temp_dist)
        x = s#next node as the starting node for loop
    return ([sol,tot_dist,s])
def print_cityname(sol):#taking the solution in form of nodes and printing corresponding cities
    cityname_sol = []
    for cityname in sol:
        cityname_sol.append(cities[cityname][0])
    return  cityname_sol

def plotting_cities(ans):#plotting the cities as points and arrows
    ax = plt.subplot()
    for city in cities:
        ax.plot(city[1],city[2],'ro')
        ax.text(city[1],city[2],city[0]+'('+str(city[1])+','+str(city[2])+')',ha='left', va='bottom')
    for v in range(0,len(ans)-1):
        node = ans[v]
        next_node = ans[v+1]
        #print(node,next_node)
        #print(cities[node][1],cities[node][2],cities[next_node][1],cities[next_node][2])
        plt.annotate(s='', xy=(cities[node][1],cities[node][2]), xytext=(cities[next_node][1],cities[next_node][2]), arrowprops=dict(arrowstyle='<-'))

    last_node = ans[len(ans)-1]
    start_node = ans[0]
    circle = plt.Circle((cities[start_node][1], cities[start_node][2]),1, color='blue') #source node is circled in blue
    #print(last_node,start_node)
    ax.add_artist(circle)
    plt.annotate(s='', xy=(cities[last_node][1], cities[last_node][2]), xytext=(cities[start_node][1], cities[start_node][2]),
                 arrowprops=dict(arrowstyle='<-'))#joining last node to first node

    plt.show()

start_city = 'Worcester' # start city
res = any(start_city in sublist for sublist in cities)#checking if start city exists in cities matrix
if res:
    print('Running the algorithm - hang tight')
    for city in cities:
        if start_city == city[0]:
            source = cities.index(city)
            break

    temp_distmat = distmat(cities)  # getting distance matrix - this will get changed when we run the greedy algo
    k = greedyTSP(temp_distmat,source)  # k will be a list with sol(list),distance excluding the end node to source , and the end node
    org_distmat = distmat(cities)  # calling the distance matrix to get the distance from end to source
    tot_dist = k[1] + org_distmat[k[2]][source]  # adding the distance of end node to source
    print('The solution is', k[0])
    print(print_cityname(k[0]))
    print('The total distance of loop is', tot_dist)
    plotting_cities(k[0])

else:
    print('invalid city')






