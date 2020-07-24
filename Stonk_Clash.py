
from Clash_Functions import *

def main():
    
    end_program = False
    while end_program == False:
        
        print("\nWelcome to Clash of Stonks!")
        action = input("1. Login\n2. Create Account\n3. Exit\n(Type 1, 2, or 3): ")
        
        if action == "1":
            UserID = login()
            
            if UserID == "false":
                
                continue
            
        elif action == "2":
            UserID = user_info()
        
        elif action == '3':
            end_program = True
            
            break
        
        else:
            
            continue
        
        logout = False 
        while logout == False:
           
            print("What would you like to do?")
            action = input("1. buy\n2. sell\n3. view portfolio\n4. view leaderboard \n5. Awards \n6. update account info\n7. logout\n(select an option): ")
            
            if action == '1':
                show_table(UserID)
                purchase_order(UserID)
                
                continue
        
            if action == '2':
                show_table(UserID)
                sale_order(UserID)
                
                continue
            
            if action == '3':
                view_portfolio(UserID)
                
                continue
                
            if action == '4':
                rank_display()
                
                continue
                
            if action == '5':
                awards_menu(UserID)
                
                continue
               
            if action == '6':
                update_user_menu(UserID)
                
                continue
                
            if action == '7':
                logout = True 
                break
            
            else: 
                continue

        
if __name__ == "__main__":
    main()
    
    