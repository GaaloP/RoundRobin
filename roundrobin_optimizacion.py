# ¿Qué se va a optimizar?
## Se implementará la función SPF (Small Process First) con el objetivo de optimizar 
## los tiempos de espera y de retorno promedio. La lógica detrás de esta estrategia es que 
## los procesos más cortos (en términos de tiempo de servicio) se ejecuten con mayor frecuencia, 
## lo que reduce significativamente su tiempo de espera.
##
## Además, se considerará el tiempo de llegada de cada proceso. En caso de que un nuevo proceso 
## llegue mientras una ronda ya está en ejecución, este será añadido a la siguiente ronda. 
## Para lograrlo, en cada ronda se aplicará un algoritmo de ordenamiento que evaluará el 
## tiempo de servicio restante de cada proceso, los organizará de menor a mayor y comenzará 
## la ejecución en ese orden.

import pandas as pd
import matplotlib.pyplot as plt
import random

def NuevoProceso(L, Laux, R):
    print('\n______________________________\n_______Carga de datos_________\n______________________________\n')
    
    canProcesos = int(input('Ingresa la cantidad de procesos: '))
    for j in range(canProcesos):
        PID = str(input(f'Ingrese el id del proceso {j}:'))
        TS = int(input(f'Ingrese el tiempo de servicio del proceso {j}:'))
       
        L.loc[len(Laux)] = [PID, TS, 0, R, 0, 0]
        Laux.loc[len(Laux)] = [PID, TS, 0, R, 0, 0]
                
def color_random():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

Ti = 1
R = 0

L = pd.DataFrame()
L['PID'] = []
L['TS'] = []
L['TL'] = []
L['TR'] = []
L['TF'] = []
L['TE'] = []

Laux = L.copy()

NuevoProceso(L, Laux, R)



Q = int(input('Ingresa el valor Quantum: '))
 #ESte es el reloj 
Pant = pd.DataFrame()
Pant['PID'] = []
Pant['TS'] = []

# plot
ejecuciones = [] 
ronda = 1

while Laux['TS'].sum() > 0:
    
    nuevo = 0
    while nuevo != '1' and nuevo != '2':
        print('----------------------------------------')
        nuevo = input('Que deseas hacer? (ingresa el numero de la opcion)\n1.-\tAgregar un nuevo proceso.\n2.-\tContinuar ronda.\nRespusta>')
    
    if nuevo == '1':
        NuevoProceso(L, Laux, R)
        
    
    print('\n/////////////////////\n/////Nueva Ronda////\n////////////////////')
    Laux = Laux.sort_values('TS').reset_index(drop=True)
       
    for i in range(len(Laux)):  

        if Laux.loc[i, "TS"] > 0: 
            if (not Laux.iloc[i].equals(Pant)) and (not Pant.empty):
                # Si el proceso que entra es diferente al anterior, se le suma el tiempo de intercambio (final)
                R = R + Ti/2
                
            # Guardar inicio antes de ejecutar
            inicio = R 
            
            #si le quedan mas de 1 quantum
            if Laux.loc[i, "TS"] > Q:

                # Si el proceso que entra es diferente al anterior, se le suma el tiempo de intercambio (inicio)
                if not Laux.iloc[i].equals(Pant):
                    R = R + Ti/2

                Laux.loc[i, "TS"] = Laux.loc[i, "TS"] - Q
                R = R + Q
                duracion = R - inicio
                
            #si el ts restante es menor o igual a un quantum
            else:
                if not Laux.iloc[i].equals(Pant):
                    R = R + Ti/2

                R = R + Laux.loc[i, "TS"]
                
                duracion = R - inicio
                
                Laux.loc[i, "TS"] = 0
                Laux.loc[i, "TF"] = R
                #Tiempo de retorno = tiempo final - tiempo llegada (0)
                Laux.loc[i, "TR"] = Laux.loc[i, "TF"] - Laux.loc[i, "TL"]
                #Tiempo de espera = tiempo retorno - tiempo servicio
                Laux.loc[i, "TE"] = Laux.loc[i, "TR"] - L.loc[L["PID"] == Laux.loc[i, "PID"], "TS"].values[0]

                
            # Guardar ejecución
            ejecuciones.append((ronda, Laux.loc[i, "PID"], inicio, duracion))
    
        Pant = Laux.loc[i]

    print("Iteración con:\n", Laux)
    ronda += 1

print("\nTiempo de espera promedio:\n", Laux['TE'].mean())
print("\nTiempo de retorno promedio:\n", Laux['TR'].mean())
print('Fin')

# -------------------------------
# Plot
# -------------------------------
fig, ax = plt.subplots(figsize=(12,4))

colores = {}
for r, pid, inicio, dur in ejecuciones:
    if pid not in colores:
        colores[pid] = color_random()

    y = (r-1) * 10
    ax.broken_barh([(inicio, dur)], (y, 8), facecolors=colores[pid])
    ax.text(inicio + dur/2, y+4, pid, ha="center", va="center", color="white", fontsize=9)

ax.set_xlabel("Tiempo (R)")
ax.set_yticks([(r-1)*10+4 for r in range(1, ronda)])
ax.set_yticklabels([f"Ronda {r}" for r in range(1, ronda)])
ax.set_title("Ejecución de procesos con Round Robin")
ax.grid(True)

plt.show()