from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CategoryListCreateView, CategoryRetrieveUpdateDeleteView, CartListView, CartDetailView, PlaceOrderView, OrderHistoryView,OrderDetailView, AdminOrderListView,AdminOrderDetailView,LeaveReviewView, ProductReviewsView

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    # Category API using ViewSet (Primary API)
    path('categories/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),

    # Category API using Class-Based Views (Separate Functionality)
    path('categories/cbv/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/cbv/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-detail-cbv'),

    # Product API using ViewSet
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    
    path('cart/', CartListView.as_view(), name='cart-list'),  # List and Create Cart Items
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'), 
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/history/', OrderHistoryView.as_view(), name='order-history'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('products/<int:product_id>/reviews/', LeaveReviewView.as_view(), name='leave-review'),
    path('products/<int:product_id>/reviews/list/', ProductReviewsView.as_view(), name='product-reviews'),
]

        