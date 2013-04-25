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

from django.conf import settings

c=settings.AJAX_SEARCH_FUNCTION
m= __import__(c)

def xhr_search(request):
	req = {}
	if request.is_ajax():
		query = request.POST['query']
		try:
			choice = request.POST['choice']
		except:
			choice = '1'
		if choice == '1':
			words = query.split()
			count = len(words)
			model_list = Entry.objects.filter(title__icontains=query, status=1)
			for L in range(1, count+1):
				for subset in itertools.permutations(words, L):
					count1=1
					query1=subset[0]
					while count1!=len(subset):
						query1=query1+" "+subset[count1]
						count1+=1
					model_list = model_list | Entry.objects.filter(title__icontains=query1, status=1)
			model_list = model_list.distinct()
			req ['name'] =''
			for e in model_list[0:8]:
				req ['name']+="""<div class="searchdropdowndiv"><a href='"""
				req ['name']+=e.get_absolute_url()
				req ['name']+="""' style="text-decoration:none;"><p style="font-size:14px; color:#000000;">""" 
				req ['name']+=e
				req ['name']+="""</p></a></div>"""
			if model_list.count()>8:
				req ['name']+="""<div class="searchdropdowndiv" style="border-top:1px solid #e8e8e8;"><a href='/search/?q="""
				req ['name']+=query
				req ['name']+="""&choice="""
				req ['name']+=str(choice)
				req ['name']+="""' style="text-decoration:none;"><p style="font-size:14px; color:#a2a2a2;">See all results</p></a></div>""" 
			
			
		if choice == '2':
#					user_list = user_list | User.objects.filter(Q(penname__icontains=query1) | Q(first_name__icontains=query1) | Q(last_name__icontains=query1))
#			user_list.distinct().order_by('-numfollowers')	
			
			#Your code here
			
	else:
		req ['name'] = ""
	response=simplejson.dumps(req)
	return HttpResponse(response, mimetype="application/json")	
