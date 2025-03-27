import jwt

# The JWT token you received
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNDY4MjY5NSwiaWF0IjoxNzI0NTk2Mjk1LCJqdGkiOiJlMTA3MzIzZTE4YTg0YWM0YmRhODU0ZGUzMjc4NjJlMSIsInVzZXJfaWQiOjUsImlzX29yZ2FuaXplciI6dHJ1ZX0.NTigIAdN_tbbmaOofNYGiDYqs9SL0uODoiSsKsZD8_4"

# Secret key used to sign the token, the same one used in your Django settings
SECRET_KEY = 'django-insecure-ipna81hl(abfsk=(a=y5p0=)hf3cbt-k@shg=x2fk=iog96g19'

# Decode the token
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

# Check the claims
print(decoded)
print("Is Organizer:", decoded.get("is_organizer"))