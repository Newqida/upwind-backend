from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    is_active = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        attrs['email'] = attrs.get('email').lower()
        validated_data = super().validate(attrs)
        validated_data['access_token'] = validated_data.pop('access')
        validated_data['refresh_token'] = validated_data.pop('refresh')

        return validated_data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField()
    access_token = serializers.ReadOnlyField()
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token")
        validated_data = super().validate(attrs)
        validated_data["access_token"] = validated_data.pop("access")
        validated_data["refresh_token"] = attrs["refresh"]
        return validated_data
