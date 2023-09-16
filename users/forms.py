from django import forms
from django.contrib.auth.models import User

class UserSignUpForm(forms.ModelForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs = {"placeholder" : "Full name","class" : "input-fields"}),
	 max_length=30, required=True, label = "Full Name")
	email = forms.CharField(widget=forms.EmailInput(attrs = {"placeholder" : "Email","class" : "input-fields"}), max_length=100, required=True,label= "Email")
	password = forms.CharField(widget=forms.PasswordInput(attrs = {"placeholder" : "password","class" : "input-fields"}), label = "Password.")
	

	class Meta:

		model = User
		fields = ('username', 'email', 'password')