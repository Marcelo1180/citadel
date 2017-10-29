from django.db import models
#from tagging.fields import TagField

class Biblioteca(models.Model):
    biblioteca = models.CharField(max_length=50)
    direccion = models.CharField(max_length=250)

    def __str__(self):
        return self.biblioteca

    def __unicode__(self):
        return self.biblioteca

class Libro(models.Model):
    biblioteca = models.ForeignKey(Biblioteca)
    # tipo = models.ForeignKey(Tipo, related_name="tipo_libro")
    # Metadatos
    titulo = models.CharField(max_length=150) #old 70
    autor = models.CharField(max_length=100) #old 50
    editorial = models.CharField(max_length=100, blank=True, null=True) #old 50
    edicion = models.CharField(max_length=20, blank=True, null=True) #old 10
    publicacion = models.IntegerField(blank=True, null=True, verbose_name='Año de publicacion') #old 4 digits
    resumen = models.TextField(blank=True, null=True)
    paginas = models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Páginas') #old 10 char
    # Observaciones
    observacion = models.TextField(blank=True, null=True) #old estado 10 char
    # Almacenaje
    cantidad = models.IntegerField()
    fecha_ingreso = models.DateTimeField(verbose_name='Fecha de Ingreso', help_text='Fecha de ingreso a Biblioteca')
    # Catalogacion
    isbn = models.CharField(max_length=25, blank=True, null=True, verbose_name='ISBN', help_text='International Standard Book Number') #old 16
    #tags = TagField(blank=True, null=True, verbose_name='Palabras Clave', help_text='Son palabras concretas que describiran el libro Ejem: Física, Drama, Niños')
    dewey = models.CharField(null=True, max_length=20)
    malaga = models.CharField(null=True, max_length=20)
    # Personalizacion
    foto = models.ImageField(blank=True, null=True, upload_to='uploads/tapa', verbose_name='Tapa de Libro')
    # Libros Digitales
    libro_digital = models.FileField(blank=True, null=True, upload_to='uploads/libros', verbose_name='Libro digital', help_text='Opcion para colocar el libro digital al sistema')

    def __str__(self):
        return self.titulo

    def __unicode__(self):
        return self.titulo
