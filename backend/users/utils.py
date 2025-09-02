
from django.utils.text import slugify
from .models import PerfilUser
import random



def generar_username(nombre: str, apellido: str) -> str:
    base_username = slugify(f"{nombre}_{apellido}")
    numero = ''.join(str(random.randint(0, 9)) for _ in range(4))
    username = f"{base_username}_{numero}"
    
    contador = 1
    while PerfilUser.objects.filter(username=username).exists():
        username = f"{base_username}_{numero}_{contador}"
        contador += 1

    return username