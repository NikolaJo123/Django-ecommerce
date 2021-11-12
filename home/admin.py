from django.contrib import admin
from home.models import Setting, ContactMessage, ContactForm, MessageAlert, AlertCat, FAQ, Language, SettingLang




# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'updated_at', 'created_at', 'status']


class TheMessage(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email', 'subject', 'created_at', 'updated_at', 'status']
    readonly_fields = ('name', 'surname', 'email', 'address', 'city', 'country', 'zipcode', 'telephone', 'subject', 'message', 'ip')
    list_filter = ['status']


class AlertView(admin.ModelAdmin):
    list_display = ['name']


class CatAlertView(admin.ModelAdmin):
    list_display = ['title', 'description', 'create_at', 'update_at']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'lang', 'status', 'created_at', 'updated_at']
    list_filter= ['status']


class LanguagesAdmin(admin.ModelAdmin):
    list_display = ['name', 'code','status', 'created_at', 'updated_at']
    list_filter = ['status']


class SettingLangAdmin(admin.ModelAdmin):
    list_display = ['title', 'keywords','description','lang']
    list_filter = ['lang']




admin.site.register(FAQ, FAQAdmin)
admin.site.register(Language, LanguagesAdmin)
admin.site.register(SettingLang, SettingLangAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, TheMessage)
admin.site.register(MessageAlert, AlertView)
admin.site.register(AlertCat, CatAlertView)
