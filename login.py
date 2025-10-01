# Login genérico en Python (consola)

# Diccionario que simula usuarios registrados
usuarios = {
    "nacho": "nacho123",
    "lucas": "lucas123",
    "renzo": "renzo123"
}

def login():
    print("=== Sistema de Login ===")
    intentos = 3
    
    while intentos > 0:
        usuario = input("Usuario: ")
        contraseña = input("Contraseña: ")
        
        if usuario in usuarios and usuarios[usuario] == contraseña:
            print(f"\n✅ Bienvenido, {usuario}!")
            return True
        else:
            intentos -= 1
            print(f"❌ Usuario o contraseña incorrectos. Intentos restantes: {intentos}")
    
    print("\n⚠️ Demasiados intentos fallidos. Acceso bloqueado.")
    return False

# Ejecutar
if __name__ == "__main__":
    login()
