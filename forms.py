from django import forms
from models import User,Post,Like,Comment


class Signup_Form(forms.ModelForm):
    class Meta:
        model = User
        fields=['email','username','name','password']

class Login_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class Post_form(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image','caption']
class Like_form(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post']
class Comm_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment','post']

