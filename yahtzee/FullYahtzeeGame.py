# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 19:39:55 2020

@author: Tobi
"""
"""            
Yahtzee Regeln:
1.er = alle 1.er  
2.er = alle 2.er
3.er = alle 3.er
4.er = alle 4.er
5.er = alle 5.er
6.er = alle 6.er
Bonus(>=63P) = 35P

3 of a kind = alle Würfel
4 of a kind = alle Würfel
Full House = 25P
Small Straight = 30P
Large Straight = 40P
Yahtzee = 50P
Chance = alle Würfel

YahtzeeBonus = 100P + Joker
Joker Regeln:
1. x.er Wertung
2. beliebige untere Wertung
3. "0" in beliebiger oberen Wertung

Layout:
    
---------------------------------
|1.er :___  | 3 of a kind  :___ |
|2.er :___  | 4 of a kind  :___ |
|3.er :___  | Full House   :___ |
|4.er :___  | Sm.Straight  :___ |
|5.er :___  | Lr.Straight  :___ |
|6.er :___  | Yahtzee      :___ |
|Total:___  | Chance       :___ |
|Bonus(>=63P):___| Jokers  :___ |
---------------------------------  


"""
import random

#------------------------------------------------------------------------------
#-------------------------Überprüfung der Würfel-------------------------------
#------------------------------------------------------------------------------

"""------------------count_dice------------------------------
Input: geworfene Würfel in einer Liste
Output: 6 elementigeListe mit der Häufigkeit der Augenzahl
 
Beispiel: 
    count_dice(['1','1','1','5','2'])
    Rückgabe: [3,1,0,0,1,0] 
"""
def count_dice(dice_roll):
    dice_count=[0,0,0,0,0,0]
    
    for i, element in enumerate(dice_roll):       
        if dice_roll[i] == '1':
            dice_count[0]+= 1
            
        elif dice_roll[i] == '2':
            dice_count[1]+= 1
            
        elif dice_roll[i] == '3':
            dice_count[2]+= 1
            
        elif dice_roll[i] == '4':
            dice_count[3]+= 1
            
        elif dice_roll[i] == '5':
            dice_count[4]+= 1
            
        else: 
            dice_count[5]+= 1
    return dice_count


"""------------------check_roll------------------------------
Input: geworfene Würfel in einer Liste + Spieler Eingabe
Output: Punkte für die Würfel bei gegebener Spieler Eingabe
 
Beispiel: 
    check_roll(['1','1','1','5','2'],'3k') 
    Rückgabe: 10
"""
def check_roll(dice_roll,method):
    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    n6=0
    templist=[]
    templist= count_dice(dice_roll).copy()



#----------1.er----------------------------------------------------------------
    if method == '1':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '1':
                n1 += 1
        return 1* n1
    
#----------2.er----------------------------------------------------------------    
    if method == '2':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '2':
                n2+= 1
        return 2* n2
    
#----------3.er----------------------------------------------------------------    
    if method == '3':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '3':
                n3+= 1
        return 3* n3  
    
#----------4.er----------------------------------------------------------------        
    if method == '4':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '4':
                n4+= 1
        return 4* n4
    
#----------------------5.er----------------------------------------------------     
    if method == '5':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '5':
                n5+= 1
        return 5* n5
    
#----------------------6.er----------------------------------------------------       
    if method == '6':
        for i, element in enumerate(dice_roll):
            if dice_roll[i] == '6':
                n6+= 1
        return 6* n6
    
#----------------------3 of a kind--------------------------------------------- 
    if method == '3k' or method =='7':
        for i, element in enumerate(templist):
            if int(templist[i]) >= 3:
                for i, element in enumerate(dice_roll):
                    n1+= int(dice_roll[i]) 
            return n1
        return 0

#----------------------4 of a kind---------------------------------------------    
    if method == '4k' or method =='8':
        for i, element in enumerate(templist):
            if int(templist[i]) >= 4:
                for i, element in enumerate(dice_roll):
                    n1+= int(dice_roll[i]) 
            return n1
        return 0
    
#----------------------full house----------------------------------------------
    if method == 'fh' or method =='9':
        for i, element in enumerate(templist):
            if int(templist[i]) == 3:
                for j, element in enumerate(templist):
                    if int(templist[j]) == 1:
                        return 0
                return 25
        return 0 

#----------------------small straight------------------------------------------
    if method == 'ss' or method =='10':
        if templist[0] >= 1 and templist[1] >= 1 and  templist[2] >= 1 and  templist[3] >= 1:
            return 30
        if templist[1] >= 1 and templist[2] >= 1 and  templist[3] >= 1 and  templist[4] >= 1:
            return 30
        if templist[2] >= 1 and templist[3] >= 1 and  templist[4] >= 1 and  templist[5] >= 1:
            return 30
        return 0
    
#---------------------large straight-------------------------------------------
    if method == 'ls' or method =='11':
        if templist[0] == 1 and templist[1] == 1 and  templist[2] == 1 and  templist[3] == 1 and  templist[4] == 1:
            return 40
        if templist[1] == 1 and templist[2] == 1 and  templist[3] == 1 and  templist[4] == 1 and  templist[5] == 1:
            return 40
        return 0        

#-----------------------YAHTZEE------------------------------------------------
    if method == 'y' or method =='12':
        for i, element in enumerate(templist):
            if int(templist[i]) == 5:
                return 50
        return 0

#----------------------chance--------------------------------------------------
    if method == 'c' or method =='13':
        for i, element in enumerate(dice_roll):
                n1+= int(dice_roll[i]) 
        return n1
    
    
#------------------------------------------------------------------------------
#-----------------------------Prints-------------------------------------------
#------------------------------------------------------------------------------

"""------------------show_scoreboard------------------------------
Input: derzeitige Punkteliste
Output: print des Print Layouts

Print Layout:
---------------------------------
|1.er :___  | 3 of a kind  :___ |
|2.er :___  | 4 of a kind  :___ |
|3.er :___  | Full House   :___ |
|4.er :___  | Sm.Straight  :___ |
|5.er :___  | Lr.Straight  :___ |
|6.er :___  | Yahtzee      :___ |
|Total:___  | Chance       :___ |          
|Bonus(>=63P):___| Jokers  :___ |     
---------------------------------    
"""
def show_scoreboard(score_inputs):
    temp= []
    total= 0
    show_bonus= '_0'
    temp= list(score_inputs)
    for i in range(0,5):
        if temp[i] > '-1':
            total+= int(temp[i])
    temp.append(str(total)) 
    
    
    for i,item in enumerate(temp):
        if temp[i] == '-1':
            temp[i]= '___'
        elif int(temp[i]) < 10:
            temp[i]= '__' + str(temp[i])
        elif int(temp[i]) <100:
            temp[i]= '_'+str(temp[i])
    if total >= 63:
        show_bonus= '35'
    print('---------------------------------')
    print('|1.er :' +str(temp[0]) +'  | 3 of a kind  :' +str(temp[6]) +' |')
    print('|2.er :' +str(temp[1]) +'  | 4 of a kind  :' +str(temp[7]) +' |')
    print('|3.er :' +str(temp[2]) +'  | Full House   :' +str(temp[8]) +' |')
    print('|4.er :' +str(temp[3]) +'  | Sm.Straight  :' +str(temp[9]) +' |')
    print('|5.er :' +str(temp[4]) +'  | Lr.Straight  :' +str(temp[10]) +' |')
    print('|6.er :' +str(temp[5]) +'  | Yahtzee      :' +str(temp[11]) +' |')
    print('|Total:' +str(temp[13]) +'  | Chance       :' +str(temp[12]) +' |')          
    print('|Bonus(>=63P):_' +str(show_bonus) +'| Jokers  :___ |')     
    print('---------------------------------')
    
    
    
#------------------------------------------------------------------------------
#-------------------------MAIN-------------------------------
#------------------------------------------------------------------------------


def start():
#----------------------Setup--------------------------------------------------------
    score_inputs= []
    rounds= 0
    upper_total= 0
    total_points= 0
    
    for i in range(13):
        score_inputs.append('-1')
    
    max_rounds= int(input('Choose the amount of rounds! (Default=12) '))
    
    
#-----------------------------------Main Game Loop-----------------------------  
    while rounds <= max_rounds:
             
        dice_roll =[]
        for i in range(5):
            dice_roll.append(str(random.randint(1,6)))
              
        print('Your dice: ')
        print(*dice_roll)

#-----------------------------------Reroll 1-----------------------------------        
        safeguard1= False
        while not safeguard1:
            dice_reroll = input('Which dice do you want to reroll?\nUse 1-5, if you dont want to reroll use 0! ')
            if dice_reroll >= '6':
                print('A number between 0 and 5... ')
            else:
                safeguard1= True
            
        if dice_reroll != '0':
            dice_reroll = dice_reroll.split()
            for index, ch in enumerate(dice_reroll):
                dice_reroll[index] = int(ch) - 1
        
            for index in dice_reroll:
                dice_roll[index] = str(random.randint(1,6))
                
            print(*dice_roll)
#-----------------------------------Reroll 2-----------------------------------                 
            safeguard2= False
            while not safeguard2:
                dice_reroll2 = input('Which dice do you want to reroll?\nUse 1-5, if you dont want to reroll use 0! ')
                if dice_reroll2 >= '6':
                    print('A number between 0 and 5... ')
                else:
                    safeguard2= True
                
            if dice_reroll2 != '0':
                dice_reroll2 = dice_reroll2.split()
                for index, ch in enumerate(dice_reroll2):
                    dice_reroll2[index] = int(ch) - 1
                    
                for index in dice_reroll2:
                    dice_roll[index] = str(random.randint(1,6))                
        print()
        print(*dice_roll)
 
#-----------------------------------Auswahl der Kategorie----------------------      
        number_valid1 = False
        while not number_valid1:
            print('Where do you want to put your roll?')
            show_scoreboard(score_inputs)
            player_choice= str(input('Use: "1,2,3,4,5,6,3k,4k,fh,ss,ls,y,c" '))
            if player_choice == '1':
                if score_inputs[0] == '-1':
                    score_inputs[0] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == '2':
                if score_inputs[1] == '-1':
                    score_inputs[1] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == '3':
                if score_inputs[2] == '-1':
                    score_inputs[2] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
            elif player_choice == '4':
                if score_inputs[3] == '-1':
                    score_inputs[3] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == '5':
                if score_inputs[4] == '-1':
                    score_inputs[4] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
            
            elif player_choice == '6':
                if score_inputs[5] == '-1':
                    score_inputs[5] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
            
            elif player_choice == '3k' or player_choice =='7':
                if score_inputs[6] == '-1':
                    score_inputs[6] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == '4k' or player_choice =='8':
                if score_inputs[7] == '-1':
                    score_inputs[7] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == 'fh' or player_choice =='9':
                if score_inputs[8] == '-1':
                    score_inputs[8] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == 'ss' or player_choice =='10':
                if score_inputs[9] == '-1':
                    score_inputs[9] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == 'ls' or player_choice =='11':
                if score_inputs[10] == '-1':
                    score_inputs[10] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == 'y' or player_choice =='12':
                if score_inputs[11] == '-1':
                    score_inputs[11] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            elif player_choice == 'c' or player_choice =='13':
                if score_inputs[12] == '-1':
                    score_inputs[12] = str(check_roll(dice_roll,player_choice))
                    number_valid1 = True
                else:
                    print('You already scored points here, choose a different category.')
                    
            else: 
                print('Invalid input! Please choose one of the following: "1,2,3,4,5,6,3k,4k,ff,ss,ls,y,c"\n')
        
        
        show_scoreboard(score_inputs)
        rounds= rounds + 1
#-----------------------------------Ausgabe des Endpunktstands-----------------         
    for i, element in enumerate(score_inputs):
        total_points += int(score_inputs[i])
    for i in range(0,5):
        if score_inputs[i] > '-1':
            upper_total+= int(score_inputs[i])
    if upper_total >= 63:
        total_points += 35
    print('End of the game!\nYou have scored a total of ' + str(total_points)+ ' Points!' )
        