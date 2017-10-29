from django.core.management import BaseCommand
import datetime
from haystack import indexes
from apps.biblioteca.models import Libro

def fake_libro():
    xfakes = []
    for _ in range(1,50):
        fake = Factory.create('es_ES')
        persona = fake.simple_profile()
        item = {
            # Metadatos
            'biblioteca_id': 1,
            'titulo': fake.text(max_nb_chars=200, ext_word_list=None),
            'autor': fake.name_male(),
            'editorial': fake.company(),
            'edicion': fake.company_suffix(),
            'publicacion': fake.year(),
            'resumen': fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None),
            'paginas': random.randrange(1,5000),
            # Observaciones
            'observacion': fake.paragraphs(nb=3, ext_word_list=None),
            # Almacenaje
            'cantidad': random.randrange(1,500),
            'fecha_ingreso': fake.date_time_between(start_date="-10y", end_date="now", tzinfo=None),
            # Catalogacion
            'isbn': fake.isbn13(separator="-"),
            #tags = TagField(blank=True, null=True, verbose_name='Palabras Clave', help_text='Son palabras concretas que describiran el libro Ejem: Física, Drama, Niños')
            'dewey': fake.ean8(),
            'malaga': fake.ssn(),
            # Personalizacion
            'foto': fake.image_url(width=None, height=None),
            # Libros Digitales
            'libro_digital': fake.file_path(depth=1, category=None, extension=None),
        }
        print(item)
        p = Libro(**item)
        p.save()
        # xfakes.append(item);

class Command(BaseCommand):
    help = "Citadel - Factory fake data"

    def handle(self, *args, **options):
        fake_libro()
        self.stdout.write("El proceso se ejecuto correctamente!")
