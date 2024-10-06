"""
Модуль, фильтрующий отображение родительских пунктов текущего меню при редактировании пункта
"""
from django import forms
from .models import MenuItem

class MenuItemAdminForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance']:
            menu = kwargs['instance'].menu
            if menu:
                self.fields['parent'].queryset = MenuItem.objects.filter(menu=menu)
            else:
                self.fields['parent'].queryset = MenuItem.objects.none()
