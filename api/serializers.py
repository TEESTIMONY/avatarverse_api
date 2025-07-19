from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Avatar
from .models import Reaction

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = '__all__'
        extra_kwargs = {
            'svg_data': {'read_only': True},  # Tell DRF this is generated, not input
            'user': {'read_only': True},     # Make user read-only
            'part': {'read_only': True}
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            # Try authenticating with email
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        data['user'] = user
        return data

class CommunityAvatarSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(required=True)
    seed_text = serializers.CharField(required=True)
    reactions = serializers.SerializerMethodField()

    class Meta:
        model = Avatar
        fields = ['id', 'user', 'image', 'seed_text', 'created_at', 'reactions']
        read_only_fields = ['id', 'user', 'created_at']

    def get_reactions(self, obj):
        # Count each reaction type
        reaction_counts = {key: 0 for key, _ in Reaction.REACTION_CHOICES}
        for reaction in obj.reactions.all():
            reaction_counts[reaction.reaction] += 1
        # Get current user's reaction if authenticated
        user_reaction = None
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_reaction_obj = obj.reactions.filter(user=request.user).first()
            if user_reaction_obj:
                user_reaction = user_reaction_obj.reaction
        reaction_counts['active'] = user_reaction
        return reaction_counts

class ReactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reaction
        fields = ['id', 'user', 'avatar', 'reaction', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
