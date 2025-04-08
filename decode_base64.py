import base64

# String codificada em Base64 do comando curl
encoded = "YXBpQ25uOjdlYjE2MDA2MjY1YWE1MzUxNmIxMTU5NTAzY2MyNmViNzM4NTI5ZDM0NDgwOTE0MTZhYmE3Yzc3ODRlNWY2ODE="

# Decodifica a string
decoded = base64.b64decode(encoded).decode('utf-8')

print("String decodificada:", decoded)

# Separa o username e a senha
if ":" in decoded:
    username, password = decoded.split(":", 1)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Comprimento da senha: {len(password)}")
