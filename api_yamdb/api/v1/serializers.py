import re

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author', 'pub_date', 'title')

    def validate(self, data):
        request = self.context.get('request')
        author = request.user
        title = get_object_or_404(
            Title,
            pk=self.context.get('view').kwargs.get('title_id')
        )
        is_review_exists = (
            Review.objects.filter(title=title, author=author).exists()
        )
        if request.method == 'POST' and is_review_exists:
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв на каждое произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category',)


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role')

    def validate_username(self, username):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username.'})
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(get_user_model(), username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data

    def validate_token(self, username):
        user = get_object_or_404(User, username=username)
        token = AccessToken.for_user(user)
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"token": "Invalid token"})

    def validate_username(self, username):
        regex = re.compile(r'^[\w.@+-]+$')
        if not re.fullmatch(regex, username):
            raise serializers.ValidationError('Проверьте username!')
        return username
