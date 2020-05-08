from django.contrib import admin
from django.urls import path
from .views import HomePageView, DricaPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('dri/', DricaPageView.as_view(), name='dri'),

]
