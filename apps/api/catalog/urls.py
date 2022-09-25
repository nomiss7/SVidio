from django.urls import path
from apps.api.catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ImageViewSet, ProductDeleteView, CategoryViewSet, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, \
    CategoryDetailView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('product/', ProductListView.as_view()),
    path('product/create/', ProductCreateView.as_view()),
    path('product/update/<int:pk>/', ProductUpdateView.as_view()),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view()),
    path('product/<int:pk>/', ProductDetailView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view()),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view()),
    path('category/<int:pk>/', CategoryDetailView.as_view()),
]

router = DefaultRouter()
router.register('product/image', ImageViewSet, basename='product_image')
router.register('category', CategoryViewSet, basename='category')

urlpatterns += router.urls
