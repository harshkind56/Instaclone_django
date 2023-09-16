from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import UserProfile, NetworkEdge



class UserCreateSerializer(ModelSerializer):
    

    def create(self, validate_data):
        validate_data['password'] = make_password(validate_data['password'])

        user = User.objects.create(**validate_data)##passing the dictionory.

        UserProfile.objects.create(user = user) # it has one to one relations does it have to be automatically created when we have crea
        
       

        return user

    
    class Meta:
        model = User
        fields = ('username', 'password', 'email', )

class UserViewSerializer():
    model = User
    fields = ('first_name', 'last_name', 'username') # for viewing purpose. 


# nested serializer.
class UserProfileViewSerializer(ModelSerializer):
   
    

    user = UserViewSerializer()  # variabe name should be same as attribut.
    
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic_url', 'user')

    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_following_count(self,obj):
        return obj.following.count()


class UserProfileUpdateSerializer(ModelSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    
    def update(self, instance, validated_data):

        user = instance.user

        user.first_name = validated_data.pop('first_name', None)
        user.last_name = validated_data.pop('last_name', None)

        user.save()
        
        instance.bio = validated_data.get('bio', None)

        instance.save()

        return instance

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio',)

class NetworkEdgeCreationSerializer(ModelSerializer):

    



    class Meta:
        model= NetworkEdge
        fields = ('from_user', 'to_user')


class NetworkEdgeViewSerializer(ModelSerializer):

    from_user = UserProfileViewSerializer()
    to_user = UserProfileViewSerializer()

    class Meta:
        model = NetworkEdge
        fields = ('from_user', 'to_user')



