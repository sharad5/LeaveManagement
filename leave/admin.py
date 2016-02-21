from django.contrib import admin
from leave.models import *
from django.contrib.auth.models import User
# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
	list_display=('employee','date','status','is_approved')
	list_filter = ['date','employee__department']
	search_fields = ('employee__name',)

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','department','leave_count','gender')
	list_filter = ['department']
	search_fields = ('name',)

	def generate_username(self,firstname, lastname):
		firstname = '-'.join(firstname.split(" "))
		lastname = '-'.join(lastname.split(" "))
		username = "{0}-{1}".format(firstname, lastname).lower()
		x=0
		#print(settings.AUTH_USER_MODEL)
		while True:
			if x==0 and User.objects.filter(username=username).count() == 0:
				return username
			else:
				new_username = "{0}{1}".format(username, x)
				if User.objects.filter(username=new_username).count() == 0:
					return new_username
			x += 1
			if x > 1000000:
				raise Exception("Wow! Amazingly popular name")

	def save_model(self, request, obj, form, change):
		if obj.user is None:
			user = User.objects.create(first_name = obj.first_name, last_name = obj.last_name, email = obj.email, username = self.generate_username(obj.first_name,obj.last_name))
			user.set_password(obj.email)
			user.save()
			obj.user = user
		obj.save()

class LeaveAdmin(admin.ModelAdmin):
	list_display = ('employee','type','start_date','end_date')
	search_fields = ('employee__name','type')

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Department)
admin.site.register(Leave,LeaveAdmin)