def password_check(passwd):
      
    special_sym =['$', '@', '#', '%']
    errors = []

    if len(passwd) < 6:
        errors.append('length should be at least 6')
          
    if len(passwd) > 20:
        errors.append('length should be not be greater than 8')
          
    if not any(char.isdigit() for char in passwd):
        errors/append('Password should have at least one numeral')
          
    if not any(char.isupper() for char in passwd):
        errors.append('Password should have at least one uppercase letter')
          
    if not any(char.islower() for char in passwd):
        errors.append('Password should have at least one lowercase letter')
          
    if not any(char in special_sym for char in passwd):
        errors.append('Password should have at least one of the symbols $ @ # %')

    return errors

