from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import http
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.db.models.query import QuerySet, EmptyQuerySet
from django.core import serializers
from django.db.models import Q
import itertools
import json
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import requires_csrf_token
from django.template import Context, RequestContext, loader
from django.db.models.query import QuerySet, EmptyQuerySet
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
import cgi
import simplejson
import urllib
import datetime
import os, sys, Image


def xhr_search(request):
	req = {}
	if request.is_ajax():
		query = request.POST['query']
		choice = request.POST['choice']
		if choice == '1':
			entry_list = Entry.objects.filter(title__icontains=query, status=1)
			words = query.split()
			count = len(words)
			for L in range(1, count+1):
				for subset in itertools.permutations(words, L):
					count1=1
					print(subset)
					query1=subset[0]
					while count1!=len(subset):
						query1=query1+" "+subset[count1]
						count1+=1
					entry_list = entry_list | Entry.objects.filter(title__icontains=query1, status=1)
		
		
			entry_list = entry_list.distinct()
			req ['name'] =''
			for e in entry_list[0:8]:
				req ['name']+="""<div class="searchdropdowndiv"><a href='"""
				req ['name']+=e.get_absolute_url()
				req ['name']+="""' style="text-decoration:none;"><table style="width:100%;"><tr><td valign="center" style="text-align:left;"><img class="entrymainpic" id="entrymainpic" width="40" height="40" src='""" 
				req ['name']+=e.img_url
				req ['name']+="""' /></td><td valign="top" style="padding-left:10px;"><span id="profiledetailinfousernamelink" style="font-size:13px; color:#4d90fe;"href='"""
				req ['name']+=e.get_absolute_url()
				req ['name']+="""'>"""
				req ['name']+=(e.title[:40] + '..') if len(e.title) > 75 else e.title
				req ['name']+="""</span><p style="font-size:10px; color:#b8b8b8">"""
				req ['name']+="""by &nbsp """
				if e.isanon:
					req ['name']+="Anonymous"
				else:
					req ['name']+=e.author.penname
				req ['name']+=""" &nbsp """
				req ['name']+=str(e.followers.all().count())
				req ['name']+=""" followers &nbsp&nbsp """
				req ['name']+=str(e.numcomments)
				req ['name']+=""" comments</p></td></tr></table></a></div>"""
			if entry_list.count()>8:
				req ['name']+="""<div class="searchdropdowndiv" style="border-top:1px solid #e8e8e8;"><a href='/search/?q="""
				req ['name']+=query
				req ['name']+="""&choice="""
				req ['name']+=str(choice)
				req ['name']+="""' style="text-decoration:none;"><table style="width:100%;"><tr><td valign="center" style="text-align:center;"><p style="font-size:14px; color:#a2a2a2;">See all results</p></td></tr></table></a></div>""" 
			
			
		if choice == '2':
			user_list = User.objects.filter(penname__icontains=query)
			words = query.split()
			count = len(words)
			for L in range(1, count+1):
				for subset in itertools.permutations(words, L):
					count1=1
					query1=subset[0]
					while count1!=len(subset):
						query1=query1+" "+subset[count1]
						count1+=1
					user_list = user_list | User.objects.filter(Q(penname__icontains=query1) | Q(first_name__icontains=query1) | Q(last_name__icontains=query1))
			user_list.distinct().order_by('-numfollowers')	
			req ['name'] =''
			for u in user_list[0:8]:
				req ['name']+="""<div class="searchdropdowndiv"><a href="/"""
				req ['name']+=u.username
				req ['name']+="""/" style="text-decoration:none;"><table style="width:100%;"><tr><td valign="center" style="text-align:left;"><img class="entrymainpic" id="entrymainpic" src='""" 
				req ['name']+=u.get_profile().thumb_url4040
				req ['name']+="""' /></td><td valign="top" style="padding-left:10px;"><span id="profiledetailinfousernamelink" style="font-size:13px;"href='/"""
				req ['name']+=u.username
				req ['name']+="""/'>"""
				req ['name']+=u.penname
				req ['name']+="""</span>"""
				if u.first_name or u.last_name:
					req ['name']+=""" &nbsp <span style="font-size:11px; color:#b8b8b8">(%s %s)""" %(u.first_name, u.last_name)
				req ['name']+="""</span><p style="font-size:10px; color:#b8b8b8">"""
				req ['name']+=str(u.get_profile().followers.count())
				req ['name']+=""" followers &nbsp&nbsp """
				req ['name']+=str(u.get_profile().following.count())
				req ['name']+=""" following &nbsp&nbsp """
				req ['name']+=str(u.get_profile().articles.count())
				req ['name']+=""" articles</p></td></tr></table></a></div>"""
			if user_list.count()>8:
				req ['name']+="""<div class="searchdropdowndiv" style="border-top:1px solid #e8e8e8;"><a href='/search/?q="""
				req ['name']+=query
				req ['name']+="""&choice="""
				req ['name']+=str(choice)
				req ['name']+="""' style="text-decoration:none;"><table style="width:100%;"><tr><td valign="center" style="text-align:center;"><p style="font-size:14px; color:#a2a2a2;">See all results</p></td></tr></table></a></div>""" 
			
	else:
		req ['name'] = ""
	response=simplejson.dumps(req)
#	return HttpResponse(message)
	return HttpResponse(response, mimetype="application/json")	
