from rest_framework.serializers import ModelSerializer
from .models import UserPost, PostMedia,PostLikes,PostComments
from users.serializers import UserProfileViewSerializer
from rest_framework import serializers

class UserPostCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']

        return UserPost.objects.create(**validated_data)


    class Meta:
        model = UserPost
        fields = ('caption_text', 'location', )


class PostMediaCreateSerializer(ModelSerializer):

    class Meta:
        model = PostMedia
        fields = ('media_file', 'sequence_index', 'post')

class PostMediaViewSerializer(ModelSerializer):
    class Meta:
        model= PostMedia
        exclude = ('post', )

class PostFeedSerializer(ModelSerializer):

    class Meta:
        model = UserPost
        fields = '__all__'
        include = ('media')

class PostLikeCreateSerializer():

    def create(self, validated_data):
        
        validated_data['liked_by'] = self.context['current_user']

        return PostLikes.objects.create(**validated_data)

    class Meta:
        model = PostLikes
        fields = ('post', 'liked_by')

class UserPostCommentSerializer():

    def create(self, validated_data):
        validated_data['author'] = self.context['current_user']

        return PostComments.objects.create(**validated_data)

    class Meta:
        model = PostComments
        fields = ('id', 'text', 'post')

       
    