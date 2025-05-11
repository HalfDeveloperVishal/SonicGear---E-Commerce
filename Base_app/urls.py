from django.urls import path
from .views import homepage,register_view,login_view,logout_view,add_to_cart,cart_count,cart_view,remove_from_cart,earphone_list,headphone_list,techgadget_list_view,new_arrival_detail,featured_product_detail,headphone_detail,techgadget_detail,earphone_detail , add_address ,show_address , delete_address ,edit_address , checkout_view , new_navbar 

urlpatterns = [
    path('', homepage, name='homepage'),
    # path('base/', Base, name='Base'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path("cart/count/", cart_count, name="cart_count"),
    path('cart/', cart_view, name='cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('earphones/', earphone_list, name='earphone_list'),
    path('headphones/', headphone_list, name='headphone_list'),
    path('techgadgets/', techgadget_list_view, name='techgadget_list_view'),
    path('new-arrival/<uuid:pk>/', new_arrival_detail, name='new_arrival_detail'),
    path('featured-product/<uuid:pk>/', featured_product_detail, name='featured_product_detail'),
    path('earphone/<uuid:pk>/', earphone_detail, name='earphone_detail'),
    path('headphone/<uuid:pk>/', headphone_detail, name='headphone_detail'),
    path('tech-gadget/<uuid:pk>/', techgadget_detail, name='techgadget_detail'),
    path("add-address/", add_address, name="add_address"),
    path('show-address/', show_address, name='show_address'),
    path('delete-address/<int:address_id>/', delete_address, name='delete_address'),
    path('edit-address/<int:address_id>/', edit_address, name='edit_address'),
    path('address/<int:address_id>/select/', checkout_view, name='checkout_view'),
    path('new_navbar/', new_navbar, name='new_navbar'),
]


