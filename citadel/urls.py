"""citadel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.generics import ListCreateAPIView

# TODO: LLevar todo este desmadre a sus respectivos archivos y tambien

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def example_view(request, format=None):
    content = {
        'status': 'Hola a todos'
    }
    return Response(content)


from haystack.query import SearchQuerySet, EmptySearchQuerySet

from haystack.utils import Highlighter
from rest_framework import mixins
from apps.biblioteca.models import Libro

class LibroSearchSerializer(serializers.ModelSerializer):
    # tipo = serializers.CharField()
    biblioteca = serializers.CharField()
    # titulo = serializers.SerializerMethodField('custom_titulo')
    # def custom_titulo(self, xfield):
    #     request = self.context['request']
    #     preg = request.query_params.get('q')
    #     highlight = Highlighter(preg)
    #     # Highlighter(my_query, html_tag='div', css_class='found', max_length=35)
    #     return highlight.highlight(xfield.titulo)
    # TODO: investigar highlight en Vue para no sobrecargar al back
    resumen = serializers.SerializerMethodField('custom_resumen')
    def custom_resumen(self, xfield):
        request = self.context['request']
        preg = request.query_params.get('q')
        highlight = Highlighter(preg, max_length=150)
        # Highlighter(my_query, html_tag='div', css_class='found', max_length=35)
        return highlight.highlight(xfield.resumen)

    #Recuperar la cantidad disponible
    # xcantidad = serializers.SerializerMethodField('custom_xcantidad')
    # def custom_xcantidad(self, xfield):
    #     pcantidad = Prestamo_invitado.objects.filter(libro=xfield.pk).filter(estado__in=['Reservado', 'Prestado']).count()
    #     return int(xfield.cantidad)-pcantidad

    class Meta:
        model = Libro
        fields = ('pk', 'titulo', 'autor', 'malaga', 'dewey', 'biblioteca', 'resumen', 'fecha_ingreso')

from rest_framework import permissions
from haystack.query import AutoQuery, SQ
from haystack.inputs import Exact

class LibroSearchView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LibroSearchSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_queryset(self, *args, **kwargs):
        request = self.request
        queryset = EmptySearchQuerySet()

        q = request.query_params.get('q')
        # form = BuscarRestForm(request.GET)
        # if form.is_valid():
        #     query = strip_tags(form.cleaned_data['q'])
        #     # tipo = strip_tags(form.cleaned_data['tipo'])
        #     # queryset = SearchQuerySet().filter(content=query).filter(tipo=tipo)
        #     queryset = SearchQuerySet().filter(content=query)
        # queryset = SearchQuerySet().filter(content=q)
        queryset = SearchQuerySet().filter(SQ(content=AutoQuery(q)) | SQ(titulo=Exact(q)))
        # queryset = SearchQuerySet().filter(SQ(content=AutoQuery(q)) | SQ(titulo=AutoQuery(q)))

        return queryset


import json

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def busqueda_view(request, format=None):
    sqs = SearchQuerySet().autocomplete(content_auto=request.query_params.get('q'))[:5]
    suggestions = [result.titulo for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    content = json.dumps({
        'results': suggestions
    })
    return Response(content)


router.register("libros/search", LibroSearchView, base_name="libro-search")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
    #url(r'^api-auth-demo/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v2/', example_view),
    url(r'^api/v3/users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list'),
    url(r'^api/v1/auto/', busqueda_view),
    # -------------------------------------------------------------------------------------------
    # JWT TOKEN
    # -------------------------------------------------------------------------------------------
    url(r'^api-auth/', obtain_jwt_token),
]
