from django.contrib import admin
from leave.models import *
# Register your models here.

class AttendanceAdmin(admin.ModelAdmin):
	list_display=('employee','date','status')
	list_filter = ['date','employee__department']
	search_fields = ('employee__name',)

admin.site.register(Employee)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Department)
admin.site.register(Leave)