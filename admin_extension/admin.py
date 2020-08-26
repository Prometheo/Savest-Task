from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, re_path,reverse
from django.utils.html import format_html
from django.shortcuts import render, redirect, HttpResponseRedirect
# Register your models here.

#def deactivat_user(modeladmin, request, queryset):
    #queryset.update(is_active=False)

#deactivat_user.short_description="Deactivate user"

#ef activate_user(modeladmin, request, queryset):
    #queryset.update(is_active=True)

#activate_user.short_description="Activate user"
class UserAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_list.html'
    list_display = [
        'username', 'email', 'is_active', 'is_superuser','action_buttins',
        
        ]
    #actions = [deactivat_user, activate_user]

    def deactivate_user(self, request, user_id,):
        specific_user = User.objects.get(id = user_id)
        specific_user.is_active = False
        specific_user.save()
        self.message_user(request, "you've successfully deactivated {}".format(specific_user.username), level='warning')
        return redirect('../')
    
    def activate_user(self, request, user_id):
        specific_user = User.objects.get(id=user_id)
        specific_user.is_active = True
        specific_user.save()
        self.message_user(request, "you've successfully activated {}".format(specific_user.username))
        return redirect('../') 

    # def mail_view(self, request):
    #     return render(request, 'admin/mail_page.html')


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^deactivate/(?P<user_id>\d+)$',
                self.admin_site.admin_view(self.deactivate_user),
                name='deactivation-button',
            ),
             re_path(
                r'^activate/(?P<user_id>\d+)$',
                self.admin_site.admin_view(self.activate_user),
                name='activation-button',
            ),
        ]
        return custom_urls + urls

    def action_buttins(self, obj):
        usr = User.objects.get(id=obj.id)
        if usr.is_active:
            return format_html(
            '<a class="button" href="{}">Deactivate user</a>&nbsp;',
            reverse('admin:deactivation-button', args=[obj.id])
        )
        else:
            return format_html(
            '<a class="button" href="{}">Activate user</a>&nbsp;',
            reverse('admin:activation-button', args=[obj.id]),
        )
            

    action_buttins.short_description = 'Admin Actions'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)