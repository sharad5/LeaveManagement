from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from datetime import datetime,timedelta

# Create your models here.
class Department(models.Model):
	name = models.CharField(max_length=255 ,blank= False )
	description = models.TextField()

	def __str__(self):
		return "%s Department" % (self.name)

class Employee(models.Model):
	GENDER_CHOICES = (
		('M','Male'),
		('F','Female'),
		)
	name = models.CharField(max_length=255 ,blank= False )
	gender = models.CharField(max_length=1 , choices = GENDER_CHOICES)
	date_of_birth = models.DateField()
	department = models.ForeignKey(Department,blank = False)
	leave_count = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Attendance(models.Model):
	ATTENDANCE_CHOICES = (
		('P','Present'),
		('A','Absent'),
		('L','On Leave'),
		)
	employee = models.ForeignKey(Employee,blank=False,null =False)
	status = models.CharField(max_length=10, choices = ATTENDANCE_CHOICES)
	date = models.DateField(blank=False,null=False,default= timezone.now)
	class Meta:
		unique_together = (('employee', 'date',),)
	def __str__(self):
		return "(%s , %s , %s)" % (self.employee,self.status,self.date)

class Leave(models.Model):
	employee = models.ForeignKey(Employee,blank=False,null=False)
	type= models.CharField(max_length=50)
	start_date = models.DateField()
	end_date = models.DateField()
	def __str__(self):
		return "(%s , %s)"%(self.employee,type)

def mark_on_leave(sender,instance,**kwargs):
	date=instance.start_date
	days = abs((instance.start_date-instance.end_date).days)
	for i in range(0,days):
		attendance = Attendance(employee = instance.employee,status = 'L',date=date)
		attendance.save()
		date += timedelta(days=1)

post_save.connect(mark_on_leave,sender=Leave,dispatch_uid='mark_on_leave')

def increment_leave_count(sender,instance,**kwargs):
	print(instance.status)
	if instance.status == 'A' or instance.status == 'L':
		instance.employee.leave_count += 1
		instance.employee.save()

post_save.connect(increment_leave_count,sender=Attendance,dispatch_uid='increment_leave_count')