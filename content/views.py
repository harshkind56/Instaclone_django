from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserPostCreateSerializer,PostMediaCreateSerializer,PostFeedSerializer,PostMediaViewSerializer,PostLikeCreateSerializer,UserPostCommentSerializer
from rest_framework import mixins
from rest_framework import generics
from .models import UserPost, PostMedia,PostLikes,PostComments
from .filter import CurrentUserFollowingFilterBackend
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from datetime import datetime


class UserPostCreateFeed(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer
    filter_backends = [CurrentUserFollowingFilterBackend ]


   

    def get_serializer_context(self):
        return {'current_user' : self.request.user.profile}
    
    def get_serializer_class(self):
       
        if self.request.method == 'GET':

            return PostFeedSerializer
        
        return self.serializer_class

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class UserPostMediaView(mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes=[IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = PostMediaCreateSerializer


    def put(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class UserPostDetailUpdateView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = UserPost.objects.all()
    serializer_class = UserPostCreateSerializer

    def get_serializer_class(self):
       
        if self.request.method == 'GET':

            return PostFeedSerializer
        
        return self.serializer_class

    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def get(self,request,*args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
from rest_framework.response import Response

class PostLikeViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin,  viewsets.GenericViewSet):

    queryset = PostLikes.objects.all()
    serializer_class = PostLikeCreateSerializer

    def get_serializer_class(self):
        return {'current_user' : self.request.user.profile}
        
    
   
    #TODO IMPLIMENET GET_SERIALIZER CLASS METHOD AND APPROPIATE SERIALIZER FOR THE LIKE POST
    def list(self,request):
        post_likes = self.queryset.filter(post_id = request.query_params['post_id'])
        page = self.paginate_queryset(post_likes)
        if page:
            serializer = self.get_serializer(page, many = True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_likes, many = True)# if the page is not much 

        return Response(serializer.data)
 
class PostCommentViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    queryset = PostComments.objects.all()
    serializer_class = UserPostCommentSerializer

    def get_serializer_class(self):
        return {'current_user' : self.request.user.profile}
    
    def list(self, request):
        post_comments =self.queryset.filter(post_id = request.query_params['post_id'])

        page = self.paginate_queryset(post_comments)

        if page:
            serializer = self.get_serializer(page, many = True)

            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(post_comments, many = True)# if the page is not much 
        #implement get_serializer_class to have an appropiate response
        #update post listing serializer to cary on the count.
        #update post listing /feed serializer to show username.
        #update post feed serializers.
        #user signup  -> email.
        #challenges - increases a response time for an additional.
        #you have potential risk of api call failing.
        #Asychrnous manner
        #review the comment for foul /bad language.
        



    
    



    


