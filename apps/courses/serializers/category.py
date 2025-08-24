from rest_framework import serializers

from apps.courses.models import Category
from apps.courses.services.validate_alpha import alpha_validator


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            "name": {"required": False},
            "icon": {"required": False},
        }

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True, allow_blank=False, allow_null=False, validators=[alpha_validator]
    )

    def create(self, validated_data):
        try:
            category = Category.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                {"detail": f"Failed to create category: {str(e)}"}
            )
        return category
