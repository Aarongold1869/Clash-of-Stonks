
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
            UserID = userload()
            continue 
        
        elif action == '3':
            end_program = True
            break
            
        
        logout = False 
        while logout == False:
            print("What would you like to do?")
            action = input("1. buy\n2. sell\n3. view portfolio\n4. view leaderboard \n5. update account info\n6. logout\n(select an option): ")
            
            if action == '1':
                portload(UserID)
                continue
        
            if action == '2':
                
                continue
            
            if action == '3':
                portview(UserID)
                continue
                
            if action == '4':
                rank()
                continue
                
            if action == '5':
                
                continue
                
            if action == '6':
                
                logout = True 
                break
            break

        
        
if __name__ == "__main__":
    main()
    
    