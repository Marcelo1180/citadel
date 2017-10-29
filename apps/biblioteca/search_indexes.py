import datetime
from haystack import indexes
from apps.biblioteca.models import Libro

class LibroIndex (indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # agregando relevancia
    titulo = indexes.CharField(model_attr='titulo', boost=2.5)
    autor = indexes.CharField(model_attr='autor', boost=1)
    # tipo = indexes.CharField(model_attr='tipo')
    # biblioteca = indexes.CharField(model_attr='biblioteca')
    malaga = indexes.CharField(model_attr='malaga', boost=1)
    dewey = indexes.CharField(model_attr='dewey', boost=1)
    resumen = indexes.CharField(model_attr='resumen', boost=0.3)
    # cantidad = indexes.CharField(model_attr='cantidad')
    # fecha_ingreso = indexes.CharField(model_attr='fecha_ingreso')

    # content_auto = indexes.EdgeNgramField(model_attr='titulo')
    content_auto = indexes.EdgeNgramField(model_attr='titulo')
    # autocomplete = indexes.EdgeNgramField()
    #
    # @staticmethod
    # def prepare_autocomplete(obj):
    #     return " ".join((
    #         obj.titulo, obj.autor
    #     ))

    def get_model(self):
        return Libro

    # def index_queryset(self, using=None):
        # """Used when the entire index for model is updated."""
        # return Libro.objects.filter(fecha_ingreso=datetime.datetime.now())
        # return self.get_model().objects.filter(fecha_ingreso__lte=datetime.datetime.now())
        # return self.get_model().objects
