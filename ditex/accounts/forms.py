from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *arg, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		"""
		Here we are checking user and password , we can also check 
		other way like query set 
		qs = User.object.filter(username=username)
		"""
		if username and password:
			user = authenticate(username=username, password= password)

			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("User no loger active")

		return super(UserLoginForm,self).clean(*arg,**kwargs)

class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label="Email address")
	email2 = forms.EmailField(label = "Confirm Email address")
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',
		]
		# oder is valuabel (email and email2)
	def clean_email2(self):
		email = self.cleaned_data.get("email")
		confirm_email = self.cleaned_data.get("email2")

		if email != confirm_email:
			raise forms.ValidationError("Email addess should be same")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email alredy has been register")
		return email