# import hashlib
# import secrets
# import hmac


# def hash_password(password):
#     salt = secrets.token_bytes(16)
#     n=2**14
#     r=8
#     p=5
#     hashed = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p)
#     return hashed, salt, n, r, p

# def verify_password(password, hashed, salt, n, r, p):
#     new_hash = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p)
#     return hmac.compare_digest(hashed, new_hash)

# N=2^17 (128 MiB), r=8 (1024 bytes), p=1
# N=2^16 (64 MiB), r=8 (1024 bytes), p=2
# N=2^15 (32 MiB), r=8 (1024 bytes), p=3
# N=2^14 (16 MiB), r=8 (1024 bytes), p=5
# N=2^13 (8 MiB), r=8 (1024 bytes), p=10
#  hashlib.scrypt(password, *, salt, n, r, p, maxmem=0, dklen=64)
# https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html?utm_source=chatgpt.com