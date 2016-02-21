from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import *
import datetime

# Create your views here.
def login_init(request):
	return render(request,'leave/login.html',{})

def login_auth(request):
	print request.POST
	username = request.POST.get('username')
	password = request.POST.get('password')
	print username
	print password
	user=authenticate(username=username,password=password)
	print user
	if user is None:
		return render(request,'leave/login.html',{'error':True})
	if user.is_active:
		login(request,user)
	return HttpResponseRedirect('/mark_attendance')

def mark_attendance_init(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	print request.user
	try:
		employee = Employee.objects.get(user = request.user)
		att = Attendance.objects.get(employee = employee, date = datetime.date.today())
		status = att.status
		approved = att.is_approved
		marked = True
	except Attendance.DoesNotExist:
		marked = False
		status = None
	return render(request,'leave/mark_attendance.html',{'user':request.user,'today':str(timezone.now())[:10],'marked':marked,'status':status,'approved':approved})

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def mark_attendance(request):
	attendance = request.POST.get('attendance')
	employee = Employee.objects.get(user = request.user)
	status = attendance
	try:
		att = Attendance.objects.get(status = status, date = datetime.date.today())
	except Attendance.DoesNotExist:
		att = Attendance.objects.create(employee = employee, status = status, date = datetime.date.today())
	return render(request,'leave/mark_attendance.html',{'user':request.user,'today':str(timezone.now())[:10],'marked':True,'status':att.status})

def change_password_init(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	return render(request, 'leave/change_password.html', {'user':request.user,'error':False})

def change_password(request):
	password = request.POST.get('pass1')
	password2 = request.POST.get('pass2')
	if password != password2:
		return render(request, 'leave/change_password.html', {'user':request.user,'error':True})
	user = request.user
	user.set_password(password)
	user.save()
	return HttpResponseRedirect('/mark_attendance/')