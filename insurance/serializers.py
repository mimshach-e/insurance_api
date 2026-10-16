from rest_framework import serializers
from .models import Customer, PolicyProduct, CustomerPolicy


# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "name", "email", "phone", "address", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value.strip()


    # def validate_email(self, value):
    #     if not value.endswith("@email.com"):
    #         raise serializers.ValidationError("Must be an @email.com address.")
    #     return value


# Policy Product Serializer
class PolicyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyProduct
        fields = ["id", "name", "policy_type", "base_premium", "description", "is_available", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_base_premium(self, value):
        if value <= 0:
            raise serializers.ValidationError("Base premium must be positive.")
        return value


# Customer Policy Serializers

# Read Serializer for reading 
class CustomerPolicyReadSerializer(serializers.ModelSerializer):
    """Nested object serializer for GET requests"""
    customer = CustomerSerializer(read_only=True)
    product = PolicyProductSerializer(read_only=True)


    class Meta:
        model = CustomerPolicy
        fields = ["id", "policy_number", "customer", "product", "actual_premium", "status", "start_date", "end_date", "created_at"]


# Write Serializer for writing
class CustomerPolicyWriteSerializer(serializers.ModelSerializer):
    """Serializer for handling POST/PUT/PATCH (with just IDS for FKs)"""
    class Meta:
        model = CustomerPolicy
        fields = ["id", "policy_number", "customer", "product", "actual_premium", "status", "start_date", "end_date", "created_at"]
        read_only_fields = ["id"]

    def validate(self, data):
        start = data.get("start_date")
        end = data.get("end_date")

        if start and end and start >= end:
            raise serializers.ValidationError("End date must be greater than start date")
        return data


    def validate_actual_premium(self, value):
        if value <= 0:
            raise serializers.ValidationError("Actual premium must be positive")
        return value



# Policy Status Serializer
class CustomerPolicyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPolicy
        fields = ["status"]

          