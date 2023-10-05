import bcrypt

# create password

password = 'password123'.encode('utf-8')

hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)
# login

provided_password_correct = 'password123'
print(provided_password_correct)
provided_password_incorrect = 'password124'

verify_status = bcrypt.checkpw(provided_password_correct.encode('utf-8'), hashed_password)

if verify_status:
  print("True")
else:
  print("False")



