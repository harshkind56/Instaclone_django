from django.shortcuts import render,redirect
from users.forms import UserSignUpForm
from django.contrib import messages
from rest_framework.decorators import api_view,authentication_classes, permission_classes

from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer,UserProfileViewSerializer,UserProfileUpdateSerializer,NetworkEdgeCreationSerializer,NetworkEdgeViewSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile, NetworkEdge
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework import mixins



def index(request):


    return render(request, 'users/index.html',)

#working as django not DRF.
def Signup(request):
	form = UserSignUpForm()
	
	errors = []
    
	
	if request.method == 'POST':
		form = UserSignUpForm(request.POST)

		if form.is_valid():
			user = form.save(commit = False)
			username = form.cleaned_data.get('username')
			messages.success(request, f'account created{username}')
			user.save()
			return redirect('home')
			
	else:
		error = form.errors

		form = UserSignUpForm()


	
	context = {
		'form':form,
		'errors': errors
		
	}

	return render(request, 'users/sign_up.html', context)


@api_view(['POST'])
def create_user(request):
	

	serializer = UserCreateSerializer(data = request.data) # mapp the data 
	response_data = {
		"errors" : None,
		"data" : None
	}
	if serializer.is_valid(): # validate the data.
		
		user = serializer.save() # save the data.
		

		refresh = RefreshToken.for_user(user)

		response_data["data"] ={
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
		response_status = status.HTTP_201_CREATED
	else:
		response_data['errors'] = serializer.errors
		response_status = status.HTTP_400_BAD_REQUEST
	return Response(response_data, status= response_status)

@api_view(['GET'])
@authentication_classes([JWTAuthentication]) # request.user will specify the particular user
@permission_classes([IsAuthenticated])  # authenication should be there
def user_list(request):
	

	
	#protect this field
	#better presentation of user object.
	users = UserProfile.objects.all()
	

	serialized_data = UserProfileViewSerializer(instance = users, many = True) #multiple user back)#
	
	return Response(serialized_data.data, status= status.HTTP_200_OK)

# PUT- Imdeptont.
# retry policy.



class UserProfileDetail(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [JWTAuthentication]

	def get(self, request, pk):
		user = UserProfile.objects.filter(id=pk).first()

		if user:
			serializer = UserProfileViewSerializer(instance=user)
			response_data = {
				"data" : serializer.data,
				"error" : None
			}
			response_status = status.HTTP_200_OK
		else:
			response_data = {
				"data" : None,
				"error" :  "User does not exist"
			}
			response_status = status.HTTP_404_NOT_FOUND

		return Response(response_data, status= response_status)
		


	def post(self,request, pk):

		user_profile_serializer = UserProfileUpdateSerializer(instance = request.user.profile, data = request.data) 

		response_data = {
			"data" : None,
			"errors":None
			}

		if user_profile_serializer.is_valid():

			user_profile = user_profile_serializer.save()

			response_data['data'] = UserProfileViewSerializer(instance=user_profile).data

			response_status = status.HTTP_200_OK

		else:
			response_data['errors'] = user_profile.serializer.errors
			response_status = status.HTTP_400_BAD_REQUEST

		return Response(response_data, status= response_status)
	
	def delete(self, request, pk):
		user = request.user

		user.delete()

		response_data = {
			"data" : None,
			"message" : "User object was successfully deleted."
		}

		return Response(response_data, status= status.HTTP_200_OK)


# default behaviour of the mixings.
#override the default behaviour of the mixings. - overriding the methods such as query_set
class UserNetworkEdgeView(mixins.CreateModelMixin, mixins.ListModelMixin,  generics.GenericAPIView ):# child class of class based views.


	queryset = NetworkEdge.objects.all()
	serializer_class = NetworkEdgeCreationSerializer
	permission_classes = [IsAuthenticated, ]
	authentication_classes = [JWTAuthentication, ]

	def get_serializer(self):#get a lost of followers and following.
		if self.request.method == 'GET':
			return NetworkEdgeViewSerializer
		return self.serializer_class
	
	def get_queryset(self):
		edge_direction = self.request.query_params['direction']
		#NetworkEdge.objects.all().filter(to_user = self.request.user.profile)
		if edge_direction == 'followers':
			return self.queryset.filter(to_user = self.request.user.profile)
		elif edge_direction == 'following':
			return self.queryset.filter(from_user = self.request.user.profile)
	

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)
		


	def post(self, request, *args, **kwargs): #follow
		#request.user.profile.id
		#implement by serializer context object.
		request.data['from_user'] = request.user.profile.id
	
		return self.create(request, *args, **kwargs)  

	def delete(self, request, *args, **kwargs):#unfollow

		#token will give identity who is trying to unfollow.
		#implement it bu network edge primary key.
		network_edge = NetworkEdge.objects.filter(from_user = request.user.profile, to_user = request.data['to_user'])

		if network_edge.exists():
			network_edge.delete()
			message = "succeess"
		else:
			message = "No edge found"
		return Response({"data":None, "message" : message}, status=status.HTTP_200_OK)
		
  


	
	
