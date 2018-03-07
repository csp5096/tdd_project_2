from django.http import HttpResponse
from lists.models import List, Item
from rest_framework import routers, serializers, viewsets
from lists.forms import DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR
from rest_framework.validators import UniqueTogetherValidator

class ItemSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False,
                                 error_messages = {'blank': EMPTY_ITEM_ERROR}
                                 )

    class Meta:
        model = Item
        fields = ('id', 'list', 'text')
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=('list', 'text'),
                message=DUPLICATE_ITEM_ERROR
            )
        ]

class ListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='item_set', read_only=True)

    class Meta:
        model = List
        fields = ('id', 'items',)

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    queryset = List.objects.all()

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

router = routers.SimpleRouter()
router.register(r'lists', ListViewSet)
router.register(r'items', ItemViewSet)
