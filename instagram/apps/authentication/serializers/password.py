""" Recover password serializer classes """

# Django REST Framework
from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    """ Password reset serializer class

    Verify the new password to reset the old or forgot password.
    """

    password = serializers.CharField(min_length=8, max_length=100)
    password_confirmation = serializers.CharField(min_length=8, max_length=100)

    def validate(self, validated_data):
        password = validated_data['password']
        passwd_conf = validated_data['password_confirmation']

        if password != passwd_conf:
            raise serializers.ValidationError('Password didn\'t match')

        return validated_data