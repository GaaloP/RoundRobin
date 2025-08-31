import pandas as pd
L = pd.DataFrame()
L['PID'] = ['A','B','C','D','E','F']
L['TS'] = [10,6,1,8,13,7]
L['TL'] = [0,0,0,0,0,0]
L['TR'] = [0,0,0,0,0,0]
L['TF'] = [0,0,0,0,0,0]
L['TE'] = [0,0,0,0,0,0]
Laux = L.copy()

Q = 4
Ti = 1
R = 0 #ESte es el reloj 
Pant = pd.DataFrame()
Pant['PID'] = []
Pant['TS'] = []

while Laux['TS'].sum() > 0:
    for i in range(len(Laux)):  

        if Laux.loc[i, "TS"] > 0: 
            if (not Laux.iloc[i].equals(Pant)) and (not Pant.empty):
                # Si el proceso que entra es diferente al anterior, se le suma el tiempo de intercambio (final)
                R = R + Ti/2
            
            #si le quedan mas de 1 quantum
            if Laux.loc[i, "TS"] > Q:

                # Si el proceso que entra es diferente al anterior, se le suma el tiempo de intercambio (inicio)
                if not Laux.iloc[i].equals(Pant):
                    R = R + Ti/2

                Laux.loc[i, "TS"] = Laux.loc[i, "TS"] - Q
                R = R + Q
            #si el ts restante es menor o igual a un quantum
            else:
                if not Laux.iloc[i].equals(Pant):
                    R = R + Ti/2

                R = R + Laux.loc[i, "TS"]
                Laux.loc[i, "TS"] = 0
                Laux.loc[i, "TF"] = R
                #Tiempo de retorno = tiempo final - tiempo llegada (0)
                Laux.loc[i, "TR"] = Laux.loc[i, "TF"] - Laux.loc[i, "TL"]
                #Tiempo de espera = tiempo retorno - tiempo servicio
                Laux.loc[i, "TE"] = Laux.loc[i, "TR"] - L.loc[i, "TS"]
            
    
    
        Pant = Laux.loc[i]

    print("Iteración con:\n", Laux)

print("\nTiempo de espera promedio:\n", Laux['TE'].mean())
print("\nTiempo de retorno promedio:\n", Laux['TR'].mean())
print('Fin')