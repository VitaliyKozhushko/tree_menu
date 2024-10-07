from django.test import TestCase
from django.urls import reverse
from ..models import Menu, MenuItem


class MenuTestCase(TestCase):
    """
    Проверка правильности отображения меню на странице
    """

    def setUp(self):
        """
        Создание меню и его элементов
        """
        self.menu = Menu.objects.create(title="main_menu", url='main')
        self.item_1 = MenuItem.objects.create(menu=self.menu, title="Home", url="1")
        self.item_2 = MenuItem.objects.create(menu=self.menu, title="About", url="/about")
        self.item_3 = MenuItem.objects.create(menu=self.menu, title="Contact", url="/contact/", parent=self.item_2)

        assert Menu.objects.count() > 0

    def test_main_page_menu_list(self):
        """
        Отображение списка меню на главной странице
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'main_menu')
        self.assertNotContains(response, 'Home')

    def test_tree_menu_dynamic(self):
        """
        Отображение меню с пунктами на динамической странице
        """
        response = self.client.get(reverse('tree_menu', kwargs={'item_url': 'contact'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'main_menu')
        self.assertContains(response, 'Home')
        self.assertContains(response, 'Contact')
        self.assertContains(response, 'About')
