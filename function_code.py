import pandas as pd

#get the pricelist and converet it into a data frame
Vendopath = 'F:\\Radwania\\1-Technical\\Vendorname\\Price_List_Vendor.xlsx' 
df_aqua = pd.read_excel(aquapath)  
df_aqua['priceegp']= df_aqua['Prices']* USD TO EGP*  Discount * Tax 
df_aqua['salesprice']= df_aqua['priceegp']/Value
replacement_dict = {'INJECTED SAND FILTERS ': '', 'VALVE DIA': '', 'AT 50M3/HR/M2 VELOCITY': '', 'WITH TOP 6 WAY VALVE 1.5"': 'Tvalve 1.5"', 'SIDE 6 WAY VALVE 2"': 'Svalve 2"', 'SIDE 6 WAY VALVE 2"': 'Svalve 2"'}
df_aqua['DESCRIPTION'].replace(replacement_dict, regex=True, inplace=True) 

#main design iteams
desiredpumptype_filtration  = 'EUROSWIM'
desiredpumptype_display  = 'EUROSWIM'
volume = 600
turnover = 10   
head = 12

# Boq DataFrame List of columns
description = []
quantity = []
unitprice = []
heads = [10, 12, 14, 16, 18]
qpumpvalues = []
filtervalues = []
qpumplist = []

# Equipment lists
q_value_filter = [6, 10, 14, 22, 30, 35, 36, 44.8]
filter_values = ['450MM', '530MM', '620MM', '790MM', '900MM', '950MM', '1000MM', '1200MM']

# EUROSWIM PUMPS DISCHARGELISTS
pumpEUROSWIM1 = [18, 15, 9, 0, 0, 0]
pumpEUROSWIM1_5 = [23, 20, 14, 7, 0, 0]
pumpEUROSWIM2 = [29, 26, 21, 14, 4, 0]
pumpEUROSWIM3 = [40, 38, 33, 30, 24, 16]
EUROSWIM_pumps_discharge = [pumpEUROSWIM1, pumpEUROSWIM1_5, pumpEUROSWIM2, pumpEUROSWIM3]

# WINNER PUMPS DISCHARGELISTS
pumpOptima1 = [13, 10.5, 7.6, 4,0 ]
pumpWINNER1_5 = [21, 19, 17, 14, 10]
pumpWINNER2 = [24, 21, 18, 14, 12]
pumpWINNER3 = [29, 27, 23, 20, 15]
WINNER_pumps_discharge = [pumpOptima1, pumpWINNER1_5, pumpWINNER2, pumpWINNER3]

#MAGNUS PUMPS DISCHARGELISTS
pumpmagnus3HP = [43, 26, 10, 0, 0]    
pumpmagnus4HP = [56, 42, 29, 14, 0]
pumpmagnus5_5HP = [84, 57, 30, 0, 0]
pumpmagnus7_5HP = [107, 85, 57, 12, 0]
pumpmagnus10HP = [126, 107, 80, 48, 14]
pumpmagnus12_5HP = [152, 136, 118, 99, 80]
pumpmagnus15HP = [177, 162, 146, 130, 112]
MAGNUS_pumps_discharge = [pumpmagnus3HP,pumpmagnus4HP,pumpmagnus5_5HP,pumpmagnus7_5HP,pumpmagnus10HP, pumpmagnus12_5HP, pumpmagnus15HP]  

#pump discharge selector with respect to given head

def pump_model_discharge_at_head_finder(head, desiredpumptype_filtration, desiredpumptype_display):
    # Initialize qlist and pumpslist outside the loop
    qlist = []
    pumpslist = []
    desiredpumptype_list = [desiredpumptype_filtration]
    pumps_qlist = [] 
    pumps_pumpslist = [] 
    if  desiredpumptype_display != 0:
          desiredpumptype_list.append(desiredpumptype_display)
    for desiredpumptype in desiredpumptype_list: 
    # Check desiredpumptype Model
        if desiredpumptype == 'EUROSWIM':
            pumps_discharg_elist = EUROSWIM_pumps_discharge
            pumpslist = ['1HP', '1.5HP', '2HP', '3HP']
        elif desiredpumptype == 'WINNER':
            pumps_discharg_elist = WINNER_pumps_discharge
            pumpslist = ['1HP', '1.5HP', '2HP', '3HP']
        elif desiredpumptype == 'MAGNUS':
            pumps_discharg_elist = MAGNUS_pumps_discharge
            pumpslist = ['3HP', '4HP', '5.5HP', '7.5HP', '10HP', '12.5HP', '15HP']

        # Get the pump discharge based on the head
        for i in heads:
            if head == i:
                index_of_i = heads.index(i)
                qlist = [pumps_discharg_elist[j][index_of_i] for j in range(len(pumpslist))]

        # Additional number of pumps for MAGNUS PUMP MODEL
        if desiredpumptype == 'MAGNUS':
            add_to_pumplist = [pumps_discharg_elist[j][index_of_i] for j in range(4, len(pumpslist))]
            qlist.extend(add_to_pumplist)
        pumps_pumpslist.append(pumpslist)
        pumps_qlist.append(qlist) 



    return(pumps_qlist, pumps_pumpslist)
pump_model_discharge_at_head_finder(head, desiredpumptype_filtration , desiredpumptype_display)

#pump selection function

def pump_selector_at_discharge_q(q, qnozzels, pumps_qlist, pumps_pumpslist):
    fountain_pumps_list = [] 
    number_pumps_list = []  
    discharge_pumps_list = []
    qfountainlist = [q]

    if qnozzels != 0:
        qfountainlist.append(qnozzels)

    for discharge in qfountainlist:
        pump_found = False
        # Determine qlist and pumpslist based on discharge
        if discharge == q:
            qlist = pumps_qlist[0]
            pumpslist = pumps_pumpslist[0]
        elif len(pumps_qlist) > 1 and len(pumps_pumpslist) > 1:
            qlist = pumps_qlist[1]
            pumpslist = pumps_pumpslist[1]

        for i in range(len(qlist)):
            if discharge <= qlist[i]: 
                selected_pump = pumpslist[i]
                qpump = qlist[i]
                number_of_pumps = 1
                break
            elif discharge > qlist[i]:
                for k in range(2, 9):
                    for j in range(len(qlist)):
                        if discharge <= qlist[j] * k:
                            selected_pump = pumpslist[j]
                            qpump = qlist[j]
                            number_of_pumps = k
                            pump_found = True
                            fountain_pumps_list.append(selected_pump) 
                            number_pumps_list.append(number_of_pumps) 
                            discharge_pumps_list.append(qpump)
                            break
                    if pump_found: break
                if pump_found: break
    return fountain_pumps_list, discharge_pumps_list, number_pumps_list
pumps_qlist, pumps_pumpslist = pump_model_discharge_at_head_finder(head, desiredpumptype_filtration, desiredpumptype_display)
pump_selector_at_discharge_q(90, 200, pumps_qlist, pumps_pumpslist)

#Filter selector function 

q_value_filter = [6, 10, 14, 22, 30, 35, 36, 44.8]
filter_values = ['450MM', '530MM', '620MM', '790MM', '900MM', '950MM', '1000MM', '1200MM']
def filter_selector(q_value_filter, filter_values, q):
    filter_found = False
    for i in range(len(q_value_filter)):
        if q <= q_value_filter[i]:
            filter = filter_values[i]
            qfilter = q_value_filter[i]
            numbe_of_filters = 1
            break
        elif q > q_value_filter[i]:
            for k in range(2,9):
                for j in range(len(q_value_filter)):
                    if q <= q_value_filter[j]*k:
                       filter = filter_values[j]
                       qfilter = q_value_filter[j]
                       numbe_of_filters = k
                       filter_found = True
                       break
                    if filter_found: break
                if filter_found: break 
             
              
    return(filter, numbe_of_filters, qfilter) 
filter_selector(q_value_filter, filter_values, 120)

#BOQ lists Appending function(description, price and quantity) 

pumps_qlist, pumps_pumpslist = pump_model_discharge_at_head_finder(head, desiredpumptype_filtration , desiredpumptype_display)

fountain_pumps_list, discharge_pumps_list, number_pumps_list = pump_selector_at_discharge_q ( 90, 200, pumps_qlist, pumps_pumpslist)

filter, numbe_of_filters, qfilter= filter_selector(q_value_filter, filter_values, 120)

def pricing_and_boq_creation(filter, numbe_of_filters, qfilter,fountain_pumps_list, discharge_pumps_list, number_pumps_list, desiredpumptype_filtration, desiredpumptype_display ):
    filter_description = f'Supply and Installation and Commissionning of {numbe_of_filters} Sand Filter/s {filter} with discharge= {qfilter} m3 per hour'
    filtration_pump_description = f'Supply and Installation and Commissionning of Pump/s Model {desiredpumptype_filtration} {fountain_pumps_list[0]} ({number_pumps_list[0]} working + 1 alternating) with discharge = {discharge_pumps_list[0]} m3 per hour @head = {head} Aqua Made or Equal'
    filter_salesprice  = df_aqua.loc[df_aqua['DESCRIPTION'].str.contains(filter, na=False) , 'salesprice'].iloc[0]
    filtrationpump_salesprice  = df_aqua.loc[df_aqua['DESCRIPTION'].str.contains(fountain_pumps_list[0], na=False) & df_aqua['DESCRIPTION'].str.contains(desiredpumptype_filtration, case=False), 'salesprice'].iloc[0]
    description_list = [filter_description,filtration_pump_description] 
    salesprice_list = [filter_salesprice, filtrationpump_salesprice]
    quantity_list = [numbe_of_filters,number_pumps_list[0]]
    description.extend(description_list) 
    unitprice.extend(salesprice_list) 
    quantity.extend(quantity_list) 
    if len(fountain_pumps_list) == 2:
        Display_pump_description = f'Supply and Installation and Commissionning of Pump/s Model {desiredpumptype_display} {fountain_pumps_list[1]} ({number_pumps_list[1]} working + 1 alternating) with discharge = {discharge_pumps_list[1]} m3 per hour @head = {head} Aqua Made or Equal' 
        displaypump_salesprice = df_aqua.loc[df_aqua['DESCRIPTION'].str.contains(fountain_pumps_list[1], na=False) & df_aqua['DESCRIPTION'].str.contains(desiredpumptype_filtration, case=False), 'salesprice'].iloc[0]
        description.append(Display_pump_description) 
        unitprice.append(displaypump_salesprice) 
        quantity.append(number_pumps_list[1]) 
    accessories_list= ['ABS FRAME AND GRATE ABS CONCRETE 300 X 300MM', 'ABS MAIN DRAIN GRILLE LUXE ROUND', 'ABS BOTTOM INLET FOR CONCRETE 2" OUTSIDE THREAD, 50MM INSIDE SOLVENT', 'ABS SUCTION NOZZEL FOR CONCRETE, 2" GLUE','ABS OVERFLOW CHANNEL DRAIN FOR CONCRETE 2" OUTSIDE THREAD, 50MM INSIDE SOLVENT',]
    for desired_iteam_name in accessories_list: 
        selected_row = df_aqua[df_aqua['DESCRIPTION'].str.contains(desired_iteam_name, na=False)] 
        selected_iteam_price = selected_row['salesprice'].values.round().item() 
        description.append(desired_iteam_name) 
        unitprice.append(selected_iteam_price) 
    for i in range(len(accessories_list)):
        quantity.append(1)   
    print(unitprice , quantity, description)   

pricing_and_boq_creation(filter, numbe_of_filters, qfilter,fountain_pumps_list, discharge_pumps_list, number_pumps_list, desiredpumptype_filtration, desiredpumptype_display )

#BOQ data frame 

boq = pd.DataFrame() 
boq['Iteam'], boq['Description'], boq['Quantity'], boq['Unit Price'] = range(len(description)),  description,quantity, unitprice
boq['Total Price'] = boq['Quantity'] *  boq['Unit Price']
boq 

#DAta Frame to excel 

boq.to_excel('F:\\Radwania\\baneswief fountain\\BOQ.xlsx', index=False) 




