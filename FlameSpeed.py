import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import csv
#parameters
Po =ct.one_atm
#Kelwins
To = 298.0
#gas model
g = ct.Solution('gri30.cti')
#Domain width in [m]
width = 0.014
#Equivalence ratio loop
Phi0 = 0.68
Phik = 1.32
Phi = []
Su = []
f = open("Tekst.txt", "w")




while True:
    
    Phi0 += 0.02
    
    #Condition of breaking the loop
    if Phi0 >= Phik:
        break
        
    g.set_equivalence_ratio(Phi0, 'C2H4', {'O2':1.0, 'N2':3.76})
    g.TP = To, Po    
    #Output to control parameters of gas
    g() 
    #Output to control current equivalent ratio
    print ("Equivalent ratio: %f" % (Phi0))

    #Flame object for FreeFlame slover
    flame = ct.FreeFlame(g, width = width)
    #Tolerances for the FF solver
    flame.set_refine_criteria(ratio = 3, slope = 0.1, curve = 0.1)
    #Logging level
    loglevel = 1
    
    flame.solve(loglevel = loglevel, auto = True)
    Su0= flame.velocity[0]*100
    print("")
    #Output for control flame speed
    print("For ER: {:.2f} Flame Speed is: {:.2f}cm/s".format(Phi0,Su0))
    print("")
    Su.append(Su0)
    Phi.append(Phi0)


np.savetxt('Tekst.txt', np.c_[Su,Phi], header='Su (cm/s)               Phi\n')



#plot chart
plt.suptitle('Flame Speed of ethene versus equivalence ratio')
plt.plot(Phi, Su, 'o', label='Cantera')
plt.legend()
plt.ylabel('Burning Velocity [cm/s]')
plt.xlabel('Equivalence ratio')
plt.show()

