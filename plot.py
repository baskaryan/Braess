from __future__ import division

import matplotlib.pyplot as plt
from math import sqrt
from simulation import simulate
import numpy as np
from paths import find_paths
from equilibrium import eq_fxn


#The equilibrium C(theta) function for canonical graph
def eq_fun_six(theta):
    if theta>=23:
        return(83)
    return (1286-9*theta)/(13)

#Obtaining the values we will work with:
min_theta, max_theta, step_theta = 0, 60, 1
n_value_list = [6]
res_list = [5]
theta_value_list = list(range(min_theta, max_theta, step_theta))


list_plots = []
list_labels = []


#Types of search available 'u', 'gm', 'g'
name_of_search = {'u': 'Uniform Cost Search', 'gm': 'Google Maps', 'g': 'Greedy Search'}
chosen_searches = ['gm', 'u', 'g']


for type_of_search in chosen_searches:
    
    #We will do the following for all the resoltuion values:
    for index_res in range(len(res_list)):
        total_list = []
    
        #For each different number of people
        for n in n_value_list:
            last_person_cost = []
            per_person_cost = []
            for theta in range(min_theta, max_theta, step_theta):
                
                last_cost, avg_cost = simulate(theta, n, res_list[index_res], type_of_search)
                last_person_cost.append(  last_cost )
                per_person_cost.append( avg_cost)
            total_list.append(per_person_cost)
        
        #Plotting the points
        index_n = 0
        for n in total_list:    
            list_labels.append("{}, {} people, res: {}, ".format(name_of_search[type_of_search], n_value_list[index_n], res_list[index_res]))            
            index_n+=1
            list_plots.append(plt.scatter(theta_value_list, n, label='cur', s = 5))

plt.legend(list_plots, list_labels, fontsize=8)



#Just the equilibrium plots
plt.plot(theta_value_list, map(eq_fun_six, theta_value_list)   )
eq_graph = lambda t: [[(0,1, 10, 0), (0,2, 1, 50)], [(1,3, 1, 50), (1,2, 1, t)], [(2,3, 10, 0)], []]
paths = find_paths(eq_graph(0))
c_list={}
for n in n_value_list:
    if n!= 6:
        c_list[n] = eq_fxn(eq_graph, paths, n, theta_value_list)

for key in c_list:
    plt.plot(theta_value_list, c_list[key])

plt.ylabel('Average cost per agent')
plt.xlabel('Theta')
plt.title('Plot of Cost for all the approaches')


plt.savefig('C:/Users/Calan/Desktop/CS136 FINAL PROJECT/File '  + str(chosen_searches)+ '.png', dpi=300)
plt.show()