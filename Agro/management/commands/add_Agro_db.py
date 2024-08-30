import json
from django.core.management.base import BaseCommand
from Agro.models import Agro  # Asegúrate de que este import sea correcto

class Command(BaseCommand):
    help = 'Load data from Frutas.json into Agro model'

    def handle(self, *args, **kwargs):
        json_file_path = r'C:\Users\Usuario\Documents\Personal\EAFIT\Semestres\QuintoSemestre\PI1\Taller 1\AgroMerc\Agro\management\commands\Frutas.json'

        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if not isinstance(data, list):
            self.stdout.write(self.style.ERROR('El archivo JSON no contiene una lista.'))
            return

        for i, agro in enumerate(data):
            try:
                Agro.objects.create(
                    title=agro['Nombre'],
                    category=agro['Categoria'],  # Asegúrate de que este campo existe en el modelo
                    price=agro['Precio (COP)'],
                    max_quantity = agro['Cantidad Disponible'],
                    min_quantity = 1
                )
                self.stdout.write(self.style.SUCCESS(f'Se ha añadido correctamente el ítem {i + 1}'))
            except KeyError as e:
                self.stdout.write(self.style.ERROR(f'Falta la clave {e} en el ítem {i + 1}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al añadir el ítem {i + 1}: {e}'))
