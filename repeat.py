# Predefined list of names or items
name_list = ["Alice", "Bob", "Charlie", "David"]


while True:
    # Taking input from the user
    user_input = input("Enter a name: ")

    # Checking if the input is in the list
    if user_input in name_list:
        print("pass")
        break
    else:
        print("fail")
