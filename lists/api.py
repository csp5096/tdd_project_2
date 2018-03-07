from django.http import HttpResponse
from lists.models import List, Item
from rest_framework import routers, serializers, viewsets

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'text')

class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='item_set')

    class Meta:
        model = List
        fields = ('id', 'items',)

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

router = routers.SimpleRouter()
router.register(r'lists', ListViewSet)
