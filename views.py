# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import Signup_Form,Login_Form,Post_form,Like_form,Comm_form
from models import User, SessionToken,Post,Like,Comment
from imgurpython import ImgurClient
from smartblog.settings import BASE_DIR
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.utils import timezone


# Create your views here.



def signup_view(request):
    if request.method == "POST":
        form = Signup_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #saving data to DB
            user = User(name=name, password=password, email=email, username=username)
            user.save()
            return render(request, 'success.html')
            #return redirect('login/')
    else:
        form = Signup_Form()

    return render(request, 'index.html', {'form' : form})


def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = Login_Form(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                if password==user.password:
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = Login_Form()

    response_data['form'] = form
    return render(request, 'login.html', response_data)

def session_validator(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            return session.user
    else:
        return None

def feed_view(request):
    from clarifai.rest import ClarifaiApp
    app = ClarifaiApp(api_key='a18d01b5adca4eca9413d7f9b228a391')

    model = app.models.get(model_id='aaa03c23b3724a16a56b629203edc62c')

    user = session_validator(request)
    if user:
        posts = Post.objects.all().order_by('posted_on')
        for post in posts:
            act_usr = Like.objects.filter(user=user,post_id=post.id).first()
            if act_usr:
                post.has_liked = True

            response = model.predict_by_url("%s" % post.image_url)
            i=1
            tag_list = []
            for temp in response['outputs'][0]['data']['concepts']:
                if i>10:
                    break
                tag_list.append(temp['name'])
            post.tags = tag_list
        return render(request,'feed.html',{'Post':posts})
    else:
        return redirect('/login/')


def post_view(request):
    session = session_validator(request)
    if session:
        if request.method == "GET":
            form = Post_form()
        elif request.method == "POST":
            form = Post_form(request.POST,request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                new = Post(user=session,image=image,caption=caption)
                path = str(BASE_DIR + '/' + new.image.url)
                client = ImgurClient("8c813c6eb842fd6","75593ee8ddf35b24f24ae6649cf51bbcc52d1e2e")
                new.image_url=client.upload_from_path(path,anon=True)['link']
                new.save()
                return redirect('/feed/')

        return render(request,'post.html',{'form':form})
    else:
        return redirect('/login/')

def like_view(request):
    user = session_validator(request)
    if user and request.method == 'POST':
        form = Like_form(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            active_usr = Like.objects.filter(user=user,post_id=post_id).first()
            if active_usr:
                active_usr.delete()
            else:
                Like.objects.create(post_id=post_id,user=user)
            return redirect('/feed/')
    else:
        return redirect('/login/')
def comment_view(request):
    user = session_validator(request)
    if user and request.method=='POST':
        form = Comm_form(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get('comment')
            post_id = form.cleaned_data.get('post').id
            comment = Comment.objects.create(user=user, post_id=post_id, comment=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login/')
def logout_view(request):
    if request.COOKIES.get('session_token'):
        usr = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        usr.delete()
        return render(request,'logout.html')
    else:
        redirect('/login/')