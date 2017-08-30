# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
class User(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=15)
	username = models.CharField(max_length=15)
	password = models.CharField(max_length=6)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)


class SessionToken(models.Model):
	user = models.ForeignKey(User)
	session_token = models.CharField(max_length=255)
	last_request_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	is_valid = models.BooleanField(default=True)

	def create_token(self):
		self.session_token = uuid.uuid4()

class Post(models.Model):
    user = models.ForeignKey(User)
    image = models.FileField(upload_to='user_photos/%Y/%m/%d')
    image_url = models.URLField(max_length=200)
    caption = models.CharField(max_length=250)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_liked = False
    tags = models.CharField(max_length=800)
    @property
    def like_count(self):
        return len(Like.objects.filter(post=self))
    @property
    def comment(self):
        return Comment.objects.filter(post=self).order_by('comment_on')


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    liked_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment = models.CharField(max_length=200)
    comment_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)