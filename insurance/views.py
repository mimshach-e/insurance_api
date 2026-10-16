from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Customer, PolicyProduct, CustomerPolicy
from .serializers import (
    CustomerSerializer,
    PolicyProductSerializer,
    CustomerPolicyReadSerializer,
    CustomerPolicyWriteSerializer,
    CustomerPolicyStatusSerializer,
)

# Customer Viewset
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ["is_active", "created_at"]
    search_fields = ["name", "email", "phone", "address"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]     # default ordering


    @extend_schema(responses=CustomerPolicyReadSerializer(many=True))
    @action(detail=True, methods=["get"])
    def policies(self, request, pk=None):
        customer = self.get_object()
        policies = customer.policies.all()
        serializer = CustomerPolicyReadSerializer(policies, many=True)
        return Response(serializer.data)


# Policy Product ViewSet
class PolicyProductViewSet(viewsets.ModelViewSet):
    queryset = PolicyProduct.objects.all()
    serializer_class = PolicyProductSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ["policy_type", "is_available"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "base_premium", "created_at"]
    ordering = ["policy_type", "name"]     # default ordering


    @extend_schema(responses=CustomerPolicyReadSerializer(many=True))
    @action(detail=True, methods=["get"])
    def policies(self, request, pk=None):
        product = self.get_object()
        policies = product.policies.all()
        serializer = CustomerPolicyReadSerializer(policies, many=True)
        return Response(serializer.data)



# Customer Policy ViewSet
class CustomerPolicyViewSet(viewsets.ModelViewSet):
    queryset = CustomerPolicy.objects.select_related("customer", "product")

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "customer", "product", "product__policy_type"]
    search_fields = ["policy_number", "customer__name", "product__name"]
    ordering_fields = ["created_at", "start_date", "end_date", "actual_premium"]
    ordering = ["-created_at"]


    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CustomerPolicyReadSerializer
        if self.action == "update_status":
            return CustomerPolicyStatusSerializer
        return CustomerPolicyWriteSerializer

    @extend_schema(
        request=CustomerPolicyStatusSerializer,
        responses=CustomerPolicyReadSerializer,
    )
    @action(detail=True, methods=["patch", "post"], url_path="status")
    def update_status(self, request, pk=None):
        """for updating only the status"""
        policy = self.get_object()
        serializer = self.get_serializer(policy, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CustomerPolicyReadSerializer(policy).data)

    @extend_schema(
        request=None,
        responses=CustomerPolicyReadSerializer,
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """shortcut for canceling policy"""
        policy = self.get_object()
        policy.status = "canceled"
        policy.save()
        return Response(CustomerPolicyReadSerializer(policy).data)