import random
import time

def year_2023(conocimiento=0):
    rendirse = False
    estado = [
        "Que bueno que soy! <3 ",
        "Burnout :v ",
        "La IA es mejor que yo :'v ",
        "Sindrome del impostor ;v ",
        "No se nada -.- ",
        "Quiero dejarlo ;v",
        "Tengo que intentarlo :)"
    ]

    for dia in range(1, 366):
        print(f"Dia {dia} de 2024 ")
        print(random.choice(estado))

        # Este codigo nunca va a ejecutarse
        if rendirse:
            raise Exception()

        if dia == 365:
            print("No subir a produccion ")

        time.sleep(60 * 60 * 24)

        conocimiento += 1

    # Mueve estas líneas fuera del bucle
    print(f"Eres un {conocimiento}% mejor <3 ")
    print("Feliz 2024, Developers!")

# Llama a la función para ejecutar el código
year_2023()
