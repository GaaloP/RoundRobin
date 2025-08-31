import pandas as pd
import matplotlib.pyplot as plt

L = pd.DataFrame()
L['PID'] = []
L['TS'] = []
L['TL'] = []
L['TR'] = []
L['TF'] = []
L['TE'] = []


canProcesos = int(input('Ingresa la cantidad de procesos: '))

for i in range(canProcesos):
    L.loc[i, 'PID'] = str(input(f'Ingrese el id del proceso {i}:'))
    L.loc[i, 'TS'] = int(input(f'Ingrese el tiempo de servicio del proceso {i}:'))
    L.loc[i, 'TL'] = [0]
    L.loc[i, 'TR'] = [0]
    L.loc[i, 'TF'] = [0]
    L.loc[i, 'TE'] = [0]
Laux = L.copy()

Q = int(input('Ingresa el valor Quantum: '))
Ti = 1
R = 0 #ESte es el reloj 
Pant = pd.DataFrame()
Pant['PID'] = []
Pant['TS'] = []

# plot
ejecuciones = [] 
ronda = 1

while Laux['TS'].sum() > 0:
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
                Laux.loc[i, "TE"] = Laux.loc[i, "TR"] - L.loc[i, "TS"]
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

colores = {"A":"skyblue", "B":"coral", "C":"blue",
           "D":"orange", "E":"green", "F":"purple"}

for r, pid, inicio, dur in ejecuciones:
    y = (r-1) * 10
    ax.broken_barh([(inicio, dur)], (y, 8), facecolors=colores.get(pid,"gray"))
    ax.text(inicio + dur/2, y+4, pid, ha="center", va="center", color="white", fontsize=9)

ax.set_xlabel("Tiempo (R)")
ax.set_yticks([(r-1)*10+4 for r in range(1, ronda)])
ax.set_yticklabels([f"Ronda {r}" for r in range(1, ronda)])
ax.set_title("Ejecución de procesos con Round Robin")
ax.grid(True)

plt.show()