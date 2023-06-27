#Takes in CSV, positionEstLong, positionEstShort, takeProf, stopLoss 
#run calculation on "simple" trading algorithm


def simple_analysis(CSV_file_name, pEstLong, pEstShort, takeProf, stopLoss):

    import numpy as np
    from IPython.display import clear_output
    import matplotlib.pyplot as plt
    from numpy import genfromtxt

    my_data = genfromtxt(CSV_file_name, delimiter=',')

    time = np.array([])
    openPrice = np.array([])

    for i in my_data: 
        time = np.append(time, i[0]) #spits out unix time stamp array
        openPrice = np.append(openPrice, i[1]) #opening price

    openPrice = openPrice.astype(np.float) 
    time = time.astype(np.float)

    iteration = np.linspace(0,len(time)-1,len(time))
    iteration = iteration.astype(int)
    dfx = np.array([])
    dfy = np.array([])

    for i in iteration: 
        dfy = np.append(dfy, openPrice[i])
        dfx = np.append(dfx, time[i]) 

    df = np.column_stack((dfx, dfy)) 
    PA = df[:,1]

    LNG = pEstLong
    SHT = pEstShort
    PRT_LNG = takeProf
    PRT_SHT = takeProf
    STOP_LOSS = stopLoss
    Stake = 1E6
    Accum_profit = 0 
    Accum_loss = 0
    Fund = np.array([1E6])
    loss_keep = np.array([])
    profit_keep = np.array([])

    for i in range(len(df)-1): # Calculating Function
        clear_output(wait = True)
    
        P0 = PA[i] 
        P1 = PA[i+1]

        if np.round((P1 - P0)/P0,5) >= LNG: #Long Position Condition (buying at P1, P1 is more than LNG% of P1)
        
            for j in range(len(df[i:,:])-1): #iterating from P1 to P_end 
            
                Pn = df[i+1+j, 1] #Pn is the price of sell
                
                if np.round((Pn - P1)/P1,5) >= PRT_LNG: #Take profit condition
                    
                    profit = Stake*(Pn-P1)/P1
                    Accum_profit = Accum_profit + profit 
                    Fund = np.append(Fund, Fund[-1]+profit)
                    profit_keep = np.append(profit_keep, profit)
                    break
                    
                elif np.round((P1 - Pn)/P1,5) >= STOP_LOSS: #Stoploss condition 
                    
                    loss = Stake*(Pn-P1)/P1
                    Accum_loss = Accum_loss + loss
                    Fund = np.append(Fund, Fund[-1]+loss)
                    loss_keep = np.append(loss_keep, loss)
                    
                    break
                
                else: 
                    continue
                    
        print('Current Progress', np.round(100*i/(len(df)-1), 2),"%")
        continue

        if np.round((P1 - P0)/P0, 5) <= SHT: #Short Position Condition (margin sell at P1, P0 is less than SHT% P1)
        
            for j in range(len(df[i:,:])-1):
                Pn = df[i+1+j, 1]
                
                if np.round((P1 - Pn)/P1, 5) >= PRT_SHT: #Take profit condition (Pn is 0.5% more than P1)
                    
                    profit = Stake*(Pn-P1)/P1
                    Accum_profit = Accum_profit + profit 
                    Fund = np.append(Fund, Fund[-1]+profit)
                    profit_keep = np.append(profit_keep, profit)
                    
                    break
                    
                elif  np.round((Pn - P1)/P1, 5) >= STOP_LOSS: #Stoploss condition 
                    
                    loss = Stake*(Pn-P1)/P1
                    Accum_loss = Accum_loss + loss
                    Fund = np.append(Fund, Fund[-1]+loss)
                    loss_keep = np.append(loss_keep, loss)
                    
                    break
                    
                else: 
                    continue
        
        print('Current Progress', np.round(100*i/(len(df)-1), 2),"%")
                
        continue
            
    
    
    X = range(len(Fund))
    plt.plot(X, Fund,'k', label ='stock price' )
    plt.xlabel('Number of Trade Executed')
    plt.ylabel('Portfolio Value')
    plt.show()
