def validar_as():
    try:
        as_num = int(input("Ingrese el número de AS de BGP: "))

        if (64512 <= as_num <= 65534) or (4200000000 <= as_num <= 4294967294):
            print(f"El número de AS {as_num} corresponde a un AS PRIVADO.")
        
        elif (1 <= as_num <= 64511) or (65536 <= as_num <= 4199999999):
            print(f"El número de AS {as_num} corresponde a un AS PÚBLICO.")
            
        else:
            print("El número ingresado está reservado o fuera del rango estándar de asignación.")

    except ValueError:
        print("Error: Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    validar_as()
