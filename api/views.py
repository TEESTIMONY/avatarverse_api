from django.shortcuts import render
import cairosvg
import base64
from io import BytesIO

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Avatar
from .serializers import AvatarSerializer, UserRegistrationSerializer, UserLoginSerializer, CommunityAvatarSerializer
from multiavatar.multiavatar import multiavatar
import random
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import ReactionSerializer
from .models import Reaction
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny




class GenerateAvatarView(generics.GenericAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [AllowAny]  # Temporarily allow anonymous access for testing

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        seed_text = serializer.validated_data['seed_text']
        svg_data = multiavatar(seed_text, False, None)

        # Convert SVG to PNG
        png_buffer = BytesIO()
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_buffer)
        png_base64 = base64.b64encode(png_buffer.getvalue()).decode('utf-8')

        response_data = {
            'seed_text': seed_text,
            'svg_data': svg_data,
            'png_data': f"data:image/png;base64,{png_base64}"
        }
        # Optionally include bg_color, overlay_text if provided
        if 'bg_color' in serializer.validated_data:
            response_data['bg_color'] = serializer.validated_data['bg_color']
        if 'overlay_text' in serializer.validated_data:
            response_data['overlay_text'] = serializer.validated_data['overlay_text']
        return Response(response_data, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_200_OK)


class CommunityAvatarShareView(generics.CreateAPIView):
    serializer_class = CommunityAvatarSerializer
    permission_classes = [IsAuthenticated]
    queryset = Avatar.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommunityAvatarListView(generics.ListAPIView):
    queryset = Avatar.objects.exclude(image='').select_related('user')
    serializer_class = CommunityAvatarSerializer


class AvatarReactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, avatar_id):
        reaction_type = request.data.get('reaction')
        if reaction_type not in dict(Reaction.REACTION_CHOICES):
            raise ValidationError({'reaction': 'Invalid reaction type.'})
        avatar = Avatar.objects.get(pk=avatar_id)
        reaction, created = Reaction.objects.update_or_create(
            user=request.user, avatar=avatar,
            defaults={'reaction': reaction_type}
        )
        serializer = ReactionSerializer(reaction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAvatarListView(generics.ListAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Avatar.objects.filter(user=self.request.user)


class UserAvatarDeleteView(generics.DestroyAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Avatar.objects.filter(user=self.request.user)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Simple health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'AvatarVerse API is running'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def static_test(request):
    """Test static file serving"""
    from django.shortcuts import render
    return render(request, 'base.html')

