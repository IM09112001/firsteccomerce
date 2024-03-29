"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import StoreListView, cart, store, checkout, updateItem, proccessOrder, product_info, login_view, sign_up, sign_out
from django.conf.urls import handler404

app_name = 'store'

handler404 = 'store.views.error_404'

urlpatterns = [
    path('', store, name="store"),
    path('store/', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),

    path('login/', login_view, name='login'),
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-out/', sign_out, name='sign_out'),

    path('product/<int:product_id>/', product_info, name='product_info'),
    
	path('update_item/', updateItem, name="update_item"),
	path('process_order/', proccessOrder, name="process_order"),
]

