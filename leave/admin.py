from django.contrib import admin
from leave.models import *
# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
	list_display=('employee','date','status')
	list_filter = ['date','employee__department']
	search_fields = ('employee__name',)

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('name','department','leave_count','gender')
	list_filter = ['department']
	search_fields = ('name',)

class LeaveAdmin(admin.ModelAdmin):
	list_display = ('employee','type','start_date','end_date')
	search_fields = ('employee__name','type')

admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Department)
admin.site.register(Leave,LeaveAdmin)