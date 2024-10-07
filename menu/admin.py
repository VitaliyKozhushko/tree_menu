from django.contrib import admin
from .models import Menu, MenuItem
from .forms import MenuItemAdminForm


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    form = MenuItemAdminForm
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        """
        Отображение родительских пунктов текущего меню при создании нового пункта
        """
        formset = super().get_formset(request, obj, **kwargs)

        class FilteredFormset(formset):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for form in self.forms:
                    menu = obj if obj else form.instance.menu
                    if menu:
                        form.fields['parent'].queryset = MenuItem.objects.filter(menu=menu)
                    else:
                        form.fields['parent'].queryset = MenuItem.objects.none()

        return FilteredFormset


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
