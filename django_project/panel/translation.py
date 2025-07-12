from modeltranslation.translator import translator, TranslationOptions
from django.contrib.auth.models import Permission

class PermissionTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Permission, PermissionTranslationOptions)
