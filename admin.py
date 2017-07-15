from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserCreationForm, UserChangeForm
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from .models import CUser

# Register your models here.

class CAdmin(admin.AdminSite):
    site_header = 'Your Site Header'
    site_title = 'Your Site Title'
    site_url = '/'

    # This is a sample of Custom Admin test page.
    # You should create admin/test.hml or delete this method
    @never_cache
    def test(self, request, extra_content=None):
        return render(request, 'admin/test.html')

    def get_urls(self):
        from django.conf.urls import url

        urls = super(CAdmin, self).get_urls()
        # Delete this if method test() above deleted
        # here you can add urls for custom pages in admin panel
        urls += [
            url(r'^test', self.admin_view(self.test))
        ]
        return urls

site_admin = CAdmin(name='Site Admin')


class CUserCreationForm(UserCreationForm):
    class Meta:
        model = CUser
        fields = ('email',)


class CUserChangeForm(UserChangeForm):
    class Meta:
        model = CUser
        fields = ('email', 'password', 'is_active', 'is_admin')


class CUserAdmin(UserAdmin):
    form = CUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



# register models
site_admin.register(CUser, CUserAdmin)