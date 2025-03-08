from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from eapp.models import Category, Product, Review, Product, OrderItem , Cart, Order
from .serializers import CategorySerializer, ProductSerializer, ProductCreateUpdateSerializer, OrderSerializer, ReviewSerializer, CartSerializer
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admins can manage categories

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]  # Enable search functionality
    search_fields = ['name', 'description']  # Allow searching by name and description

    def get_permissions(self):
        """Define permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]  # Only admins can modify
        return [IsAuthenticated()]  # Any authenticated user can view

    def create(self, request, *args, **kwargs):
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk, is_deleted=False)
        serializer = ProductCreateUpdateSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)  # No soft delete condition
        product.delete()  # Permanently delete from DB
        return Response({"message": "Product permanently deleted"}, status=status.HTTP_204_NO_CONTENT)


# Custom permission: Only admins can modify categories
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Only admins (is_staff=True) can access

# List and create categories (Only admins)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # Restrict access to admins only

# Retrieve, update, and delete categories (Only admins)
class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]  # Restrict access to admins only


class CartListView(generics.ListCreateAPIView):
    """List all cart items for the logged-in user and allow adding new items."""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Ensure cart items are always associated with the logged-in user and update stock."""
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # Check if enough stock is available
        if product.stock < quantity:
            raise ValidationError({'error': 'Not enough stock available'})

        # Reduce stock
        product.stock -= quantity
        product.save()

        # Save cart item for the logged-in user
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Override list method to include total cart price in the response."""
        queryset = self.get_queryset()
        total_cart_price = sum(item.product.price * item.quantity for item in queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "cart_items": serializer.data,
            "cart_total_price": total_cart_price
        })


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cart item (only for the logged-in user)."""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure users can only update quantity within stock limits."""
        cart_item = self.get_object()
        new_quantity = serializer.validated_data.get('quantity', cart_item.quantity)
        product = cart_item.product

        # Calculate available stock (previously added quantity should be counted)
        stock_available = product.stock + cart_item.quantity  # Restore old quantity before checking
        if new_quantity > stock_available:
            raise ValidationError({'error': 'Not enough stock available to update quantity'})

        # Adjust stock based on the new quantity
        product.stock = stock_available - new_quantity
        product.save()

        serializer.save()


# --- User Order Management ---

class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get the current user's cart items
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items.exists():
                return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new order (status defaults to "Pending")
            order = Order.objects.create(user=request.user)

            # Create order items based on each cart item
            for cart_item in cart_items:
                if not cart_item.product:
                    raise ValueError(f"Product not found for cart item: {cart_item.id}")
                if not cart_item.product.price:
                    raise ValueError(f"Price not set for product: {cart_item.product.id}")

                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_order=cart_item.product.price
                )

            # Clear the cart after placing the order
            cart_items.delete()

            # Serialize the order and return the response
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle any unexpected errors
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

# --- Admin Order Management ---

class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()

class AdminOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Order.objects.all()

    def perform_update(self, serializer):
        # Allows admin to update order status (or cancel an order by setting status to "Cancelled")
        serializer.save()


# --- Product Reviews & Ratings ---

class LeaveReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        # Get the product
        product = get_object_or_404(Product, id=product_id)

        # Check if the user has ordered the product
        if not OrderItem.objects.filter(order__user=request.user, product=product).exists():
            return Response(
                {"detail": "You can only review products you've ordered."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if the user has already reviewed the product
        if Review.objects.filter(user=request.user, product=product).exists():
            return Response(
                {"detail": "You have already reviewed this product."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the review
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get the product ID from the URL
        product_id = self.kwargs['product_id']
        # Return all reviews for the product
        return Review.objects.filter(product_id=product_id)