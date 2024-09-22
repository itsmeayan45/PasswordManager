mas_pwd=input("What is the master password? ")

def view():
    pass
view()
def add():
    name=input("Account Name: ")
    pwd=input("Password: ")
    with open("password.txt","w") as f:
        f.write(name+"|"+pwd+"\n")
        

while True:
    mode=input("Would you like to add a new password or view existing ones(view,add)? press q to quite ").lower()






    if mode=="q":
        break



    if mode=="view":
        view()
    elif mode=="add":
       add()
    else:
        print("Invalid mode")
        continue
