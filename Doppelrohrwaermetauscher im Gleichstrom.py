# Doppelrohr-WT-Gleichstrom.py
# https://repl.it/@Schaekermann/Doppelrohr-WT-Gleichstrom#main.py


import matplotlib.pyplot as plt
import math

# Vpunkt1 ist der kalte Stoffstrom (hier Wasser)
Vpunkt1 = 0.01 # m3/s
rho1 = 998.2 # kg/m3
cp1  = 4190  # J/(Kg*K)
thetaEintritt1 = 20 # °C

# Vpunkt2 ist der warme Stoffstrom (hier auch Wasser)
Vpunkt2 = 0.02 # m3/s
rho2 = 998.2 # kg/m3
cp2 = 4190  # J/(Kg*K)
thetaEintritt2 = 80 # °C


# Rohrwand innen
s = 0.003 # m entspricht s = 3 mm
lambdaStahl = 20 # W/(m*K)

# Innenrohr - Kaltes Fluid
eta1 = 1e-6  # Pa*s
di1  = 0.05  # m
da1  = di1+2*s # m

mpunkt1 = Vpunkt1*rho1
print("mpunkt1 [kg/s] = "+str(mpunkt1))
v1= Vpunkt1*4/(math.pi*di1**2)
#print("v1="+str(v1))
Re1 = v1*di1*rho1/eta1
#print("Re1="+str(Re1))

# alpha nach Chemietechnik Auflage 12 Seite 344
# turbulente strömendes Wasser in eiunem Rohr
# alpha = 1000 bis 15000 ich wähle den Mittelwert
alpha1 = 8000 # W/(m^2 * K)

# Aussenrohr - Warmes Fluid
#rho2 = 998.2 # kg/m3
eta2 = 1e-6  # Pa*s
#cp2 = 4190  # J/(Kg*K)
di2  = 0.1  # m
#thetaEintritt2 = 90 # °C
#Vpunkt2 = 0.01 # m3/s
mpunkt2 = Vpunkt2*rho2
print("mpunkt2 [kg/s] = "+str(mpunkt2))
v2 = Vpunkt2*4/(math.pi*(di2**2-da1**2))
#print("v2="+str(v2))
Re2 = v2*di2*rho2/eta2
#print("Re2="+str(Re2))

# alpha nach Chemietechnik Auflage 12 Seite 344
# turbulente strömendes Wasser in eiunem Rohr
# alpha = 1000 bis 15000 ich wähle den Mittelwert
alpha2 = 8000 # W/(m^2 * K)

# Wärmedurchgang
k=1/(1/alpha1 + s/lambdaStahl +1/alpha2)
print("k=",k)
# k = 3000  # W/(m2*K)
#print("k="+str(k))

deltal = 0.5 # m


deltaA = di1*deltal*math.pi
#print("deltaA="+str(deltaA))
abschnitte=400
theta_innen = [thetaEintritt1]
theta_aussen = [thetaEintritt2]


i=0
laenge = [i*deltal]
Qpunkt = [k*deltaA*(theta_aussen[0]-theta_innen[0])]

#print(i,theta_innen[i],theta_aussen[i],Qpunkt[i],sep=" ")              
for i in range(1,abschnitte+1):
   theta_innen.append((theta_innen[i-1]+ Qpunkt[i-1]/(mpunkt1*cp1)))
   theta_aussen.append((theta_aussen[i-1] - Qpunkt[i-1]/(mpunkt2*cp2)))
   Qpunkt.append(k*deltaA*(theta_aussen[i]-theta_innen[i]))
   laenge.append(i*deltal)
   #print(i,theta_innen[i],theta_aussen[i],Qpunkt[i],sep=" ")
   #print(i)

print("\nDer warme Stoffstrom:")
print("Theta-2-Eintritt [°C] =", thetaEintritt2 ,"\nTheta-2-Austritt [°C] =", theta_aussen[abschnitte])

print("\nDer kalte Stoffstrom:")
print("Theta-1-Eintritt [°C] =", thetaEintritt1 ,"\nTheta-1-Austritt [°C] =", theta_innen[abschnitte])

DeltaThetaklein=theta_aussen[abschnitte]-theta_innen[abschnitte]
DeltaThetagroß=theta_aussen[0]-theta_innen[0]
DeltaThetaMittel = (DeltaThetagroß-DeltaThetaklein)/ math.log(DeltaThetagroß/DeltaThetaklein)
# log ist in Python der natürliche Logarithmus, also die Umkehrfunktion zu e^x
#print("DeltThetaMittel [°C] =", DeltaThetaMittel)
   
plt.plot(laenge, theta_innen, "b",
         laenge, theta_aussen, "r")
plt.xlabel('Länge [m]')
plt.ylabel('Temperatur [°C]')
plt.title('Gleichstrom')
plt.xlim(0,200)
plt.ylim(0,100)
plt.show()



theta_aussen[0]=thetaEintritt2
theta_innen[0]=thetaEintritt1
Qpunkt[0]= k*deltaA*(theta_aussen[0]-theta_innen[0])


for i in range(0,abschnitte+1):
   theta_innen[i]=thetaEintritt1
for j in range(15):     
    Qpunkt[0]= k*deltaA*(theta_aussen[0]-theta_innen[0])
    for i in range(1,abschnitte+1):
       #theta_innen[i]=theta_innen[i-1] - Qpunkt[i-1]/(mpunkt1*cp1)
       theta_aussen[i]=theta_aussen[i-1] - Qpunkt[i-1]/(mpunkt2*cp2)
       Qpunkt[i]=k*deltaA*(theta_aussen[i]-theta_innen[i])
       #print(i,theta_innen[i],theta_aussen[i],Qpunkt[i],sep=" ")
       #print(i)

    for i in range(abschnitte,0,-1):
       #print(i)
       theta_innen[i-1]=theta_innen[i] + Qpunkt[i]/(mpunkt1*cp1)
       #theta_aussen[i]=theta_aussen[i-1] - Qpunkt[i-1]/(mpunkt2*cp2)
       Qpunkt[i-1]=k*deltaA*(theta_aussen[i-1]-theta_innen[i-1])
       #print(i-1,theta_innen[i-1],theta_aussen[i-1],Qpunkt[i-1],sep=" ")
       #print(i)

print("\nDer warme Stoffstrom:")
print("Theta-2-Eintritt [°C] =", thetaEintritt2 ,"\nTheta-2-Austritt [°C] =", theta_aussen[abschnitte])

print("\nDer kalte Stoffstrom:")
print("Theta-1-Eintritt [°C] =", thetaEintritt1 ,"\nTheta-1-Austritt [°C] =", theta_innen[0])

plt.plot(laenge, theta_innen, "b",
             laenge, theta_aussen, "r")
plt.xlabel('Länge [m]')
plt.ylabel('Temperatur [°C]')
plt.title('Gegenstrom ' +str(j+1) +'. Durchlauf')
plt.xlim(0, 200)
plt.ylim(0, 100)
plt.show()

''' Beispielausgaben
mpunkt1 [kg/s] = 9.982000000000001
mpunkt2 [kg/s] = 19.964000000000002
k= 2500.0


Der warme Stoffstrom:
Theta-2-Eintritt [°C] = 80 
Theta-2-Austritt [°C] = 61.18413163529428

Der kalte Stoffstrom:
Theta-1-Eintritt [°C] = 20 
Theta-1-Austritt [°C] = 57.63173672941132
DeltThetaMittel [°C] = 19.96927671528714
'''
