from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('product-list/', views.product_list, name='product_list'),
    path('product/<pid>/', views.product_detail, name='product_detail'),


    ####-------------------category--------------------#####
    path('category/', views.category_list, name='category_list'),  
    path('category/<cid>/', views.category_product_list_view, name='category_product_view'),
    path('category/cat5f2hb2e2bh/', views.category_product_list_view, name='best_selling'),

    #####-----------------vendor-----------------------#####
    path('vendors/', views.vendor_list_view, name='vendor_list'),
    path('vendor/<vid>/', views.vendor_detail_view, name='vendor_detail'),


    path('add-review/<str:pid>/', views.ajax_add_review, name='ajax_add_review'),

    path('search/', views.search_view, name='search'),
    


]
