from rest_framework import routers
from item.api_v1 import views

router = routers.SimpleRouter()
router.register("item", views.ItemViewSet)


app_name = "item"
urlpatterns = router.urls + [
]
