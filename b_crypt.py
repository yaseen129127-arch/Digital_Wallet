import bcrypt

# def pass_bcrypt():
# password="secure_password".encode("utf-8")
password=b"secure_password"
# print(password)

# print(type(password))
salt=bcrypt.gensalt()
hashed=bcrypt.hashpw(password, salt)
# if bcrypt.checkpw(password,hashed)

# print("hashed password:", hashed)
# import bcrypt


# password = b"123456"

# salt1 = bcrypt.gensalt()
# salt2 = bcrypt.gensalt()

# hash1 = bcrypt.hashpw(password, salt1)
# hash2 = bcrypt.hashpw(password, salt2)

# print(hash1)
# print(hash2)