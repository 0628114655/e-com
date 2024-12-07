from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('electronics/', views.electronics, name = 'electronics'),
    path('clothing/', views.clothing, name = 'clothing'),
    path('shoes/', views.shoes, name = 'shoes'),
    path('palestine/', views.palestine, name = 'palestine'),
    path('cart/', views.cart, name = 'cart'),
    path('product/<int:product_id>', views.product, name = 'product'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_items/', views.updateItems, name = 'update_items'),
    path('processOrder/', views.processOrder, name = 'processOrder'),
    path('signin/', views.signIn, name = 'signin'),
    path('signup/', views.signUp, name = 'signup'),
    path('signout/', views.signOut, name = 'signout'),
    path('required/', views.required, name = 'required'),
]
