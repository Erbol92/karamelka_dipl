from django.db import models
from django.db.models.functions import Cast
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from diplom.settings import MEDIA_ROOT
from django.shortcuts import reverse
from math import prod
from diplom.settings import coefficient
import json
from datetime import datetime
# Create your models here.


class CategoryProduct(models.Model):
    name_category = models.CharField('тип', max_length=50)
    slug = models.SlugField(max_length=50, unique=True,
                            db_index=True, verbose_name="URL", null=True)

    def __str__(self):
        return self.name_category

    class Meta:
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'


class Products(models.Model):
    def image_path(self, instance):
        return f'{MEDIA_ROOT}/products/{self.name_product}/{self.image.name}'
    category = models.ForeignKey(
        CategoryProduct, verbose_name='категория', on_delete=models.CASCADE, null=False, related_name='prod_cat')
    name_product = models.CharField('Название продукта', max_length=50)
    description = models.TextField('Описание')
    price = models.FloatField('Цена товара', default=0)
    quantity = models.IntegerField('Кол-во', default=0)
    image = models.ImageField('фото', upload_to=image_path)

    def compress_logo(self, image):
        im = Image.open(image)
        width, height = im.size[0], int(im.size[0] * 1.5)
        x, y = 0, int((im.size[1] - height) // 2)
        area = (x, y, x+width, y+height)
        im = im.crop((area))
        im = im.resize((200, 300))
        im_bytes = BytesIO()
        im.save(fp=im_bytes, format="WEBP", quality=100)
        image_content_file = ContentFile(content=im_bytes.getvalue())
        name = image.name.split('.')[0] + '.WEBP'
        new_image = File(image_content_file, name=name)
        return new_image

    def save(self, *args, **kwargs):
        try:
            this = Products.objects.filter(id=self.id).first()
            if this and this.image != self.image:
                self.image = self.compress_logo(self.image)
                this.image.delete(save=False)
        except ValueError:
            pass
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name_product
    
    def get_absolute_url(self,*args,**kwargs):
        return reverse('product_detail', kwargs={'pk': self.id, 'name': self.name_product})
    
    def get_ingridients(self):
        return ProductIngredients.objects.filter(product=self)

    def get_pfc(self):
        nutricions = self.get_ingridients().aggregate(
        total_protein=Cast(models.Sum(models.F('protein') * models.F('amount') / 1000), models.IntegerField()),
        total_fat=Cast(models.Sum(models.F('fat') * models.F('amount') / 1000), models.IntegerField()),
        total_carbohydrate=Cast(models.Sum(models.F('carbohydrate') * models.F('amount') / 1000), models.IntegerField()),
    )
        nutricions['kcal'] = nutricions['total_protein']*4+nutricions['total_fat']*9+nutricions['total_carbohydrate']*4
        return nutricions
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Ingridients(models.Model):
    name_ingridient = models.CharField(
        'название ингридиента', max_length=50, null=False, blank=False)

    def __str__(self):
        return f'{self.name_ingridient}'

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class ProductIngredients(models.Model):
    product = models.ForeignKey(
        Products, verbose_name='продукт', on_delete=models.CASCADE)
    ingridient = models.ForeignKey(
        Ingridients, verbose_name='название', on_delete=models.CASCADE, null=True, blank=False)
    amount = models.FloatField('кол-во', default=0)
    choice = (
        ('things', 'шт.'),
        ('gram', 'грамм'),
        ('tsn', 'ч.л.'),
        ('tbsn', 'ст.л.'),
    )
    unit = models.CharField('ед. изм.', max_length=10, choices=choice)
    protein = models.IntegerField('белки', default=0)
    fat = models.IntegerField('жиры', default=0)
    carbohydrate = models.IntegerField('углеводы', default=0)
    calories = models.FloatField('каллории', default=0)

    def __str__(self):
        return f'{self.product.name_product}'

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Cart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False, related_name='carts')
    product = models.ForeignKey(
        Products, verbose_name='товар', on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField('кол-во в корзине', default=1)

    def __str__(self):
        return f'{self.user} {self.product.name_product} - {self.quantity} шт.'

    def get_pos_sum(self):
        print(self.product.price,self.quantity)
        return self.product.price*self.quantity
    
    def remove_from_cart(self):
        self.quantity -=1
        self.save()
        return f'{self.product} удален из корзины'
    
    def add_quant_to_cart(self):
        self.quantity +=1
        self.save()
        return f'{self.product} добавлен в корзину'
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Bisquit(models.Model):
    title = models.CharField('Название', max_length=30)
    descrition = models.TextField('Описание')
    calorie = models.IntegerField('Ккал/100гр', default=0)
    weight = models.IntegerField('Вес кг/м3', default=0)
    price = models.FloatField('цена за кг', default=0)

    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name = 'Бисквит'
        verbose_name_plural = 'Бисквиты'

class Filling(models.Model):
    title = models.CharField('Название', max_length=30)
    descrition = models.TextField('Описание')
    calorie = models.IntegerField('Ккал/100гр', default=0)
    weight = models.IntegerField('Вес кг/м3', default=0)
    price = models.FloatField('цена за кг', default=0)

    def __str__(self):
        return f'{self.title}'
    class Meta:
        verbose_name = 'Начинка'
        verbose_name_plural = 'Начинки'

class CartConstructor(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False, related_name='carts_constr')
    uniq_id = models.CharField('хекс', max_length=100)
    data = models.JSONField()  # Поле для хранения JSON-данных
    quantity = models.IntegerField('количество',default=1)
    price = models.IntegerField('Цена',default = 0)

    def get_data(self):
        return present_data(self)
        

    def get_sum(self):
        return self.price*self.quantity
    
    def remove_from_cart(self):
        self.quantity -=1
        self.save()
        return f'удалено из корзины'
    
    def add_quant_to_cart(self):
        self.quantity +=1
        self.save()
        return f'добавлено в корзину'
    
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        verbose_name = 'Конструктор корзина'
        verbose_name_plural = 'Конструктор корзина'

class Order(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False, related_name='orders')
    product = models.ForeignKey(Products,verbose_name='товар', on_delete=models.CASCADE,null=True,blank=True)
    consrt = models.JSONField('Заказ из конструктора',null=True,blank=True)  # Поле для хранения JSON-данных
    quantity = models.PositiveIntegerField('Количество',default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    place =  models.JSONField('доставка/адрес',null=False)
    payment =  models.JSONField('оплата',null=False)
    CHOICE = {'in_job': 'в работе',
              'ready':'готов',}
    state = models.CharField('состояние',max_length=6, choices=CHOICE,default = 'in_job')
    status = models.BooleanField('отработан',default=False)
    status_at = models.DateTimeField('время готовности',null=True,blank=True)
    def __str__(self):
        return f'заказ {self.user} {self.quantity} x {self.product or self.consrt}'
    
    def get_data(self):
        return present_data(self)
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def json_place(self):
        if not self.place:  # Проверяем, что поле не пустое
            return {}  # Возвращаем пустой словарь, если поле пустое
        try:
            return json.loads(self.place)  # Преобразуем JSON-строку обратно в словарь
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}  # Возвращаем пустой словарь в случае ошибки
    def json_payment(self):
        if not self.payment:  # Проверяем, что поле не пустое
            return {}  # Возвращаем пустой словарь, если поле пустое

        try:
            return json.loads(self.payment)  # Преобразуем JSON-строку обратно в словарь
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        return {}  # Возвращаем пустой словарь в случае ошибки

def present_data(obj):
        def replace_keys(original_dict, replacement_dict):
            return {replacement_dict.get(key, key): value for key, value in original_dict.items()}
        replacement_size = {
            'a': 'длина',
            'b': 'ширина',
            'c': 'высота',
            'r': 'радиус',
            'h': 'высота'
        }
        replacement_form = {
            'circle': 'круг',
            'square': 'квадрат',
            'rectangle': 'прямоугольник',
        }
        data = obj.data if hasattr(obj,'data') else obj.consrt 

        price = 0
        present = {}
        present['layers_size'] = len(data)-2
        present['layers']=[]
        for step, dat in data.items():
                if int(step) == 1:
                    present['guest'] = dat.get('guest')
                if int(step) > 1 and  int(step) < len(data):
                    bisquit = Bisquit.objects.get(id=dat.get('bisquit'))
                    present['layers'].append({
                        'form':replacement_form.get(dat.get('form'), dat.get('form')),
                        'bisquit':bisquit,
                        'size':replace_keys(dat.get('size'), replacement_size),
                        'step':int(step)-1
                        }
                        )
                if int(step) == len(data):
                    filling = Filling.objects.get(id=dat.get('filling'))
                    present['filling'] = filling

        full_weight,ful_calorie = 0, 0
        for layer in present['layers']:
            val = 0
            match layer['form']:
                case 'круг':
                    val = 3.14*layer['size']['радиус']
                case 'квадрат':
                    val = 1
                case 'прямоугольник':
                    val = 1
            v = f'{val*prod(layer['size'].values()):.2f}'
            
            layer['weight'] = float(v)*layer['bisquit'].weight/1000000
            price += layer['weight']*layer['bisquit'].price
            layer['calorie'] = layer['weight']*10*layer['bisquit'].calorie
            full_weight += layer['weight']
            ful_calorie += layer['calorie']
        present['full_weight'] = f'{full_weight:.2f}'
        filling_ccal,filling_weight = 0, 0
        if present.get('filling'):
            filling_weight = float(present['full_weight'])*0.2
            price += present['filling'].price*filling_weight
            filling_ccal = filling_weight*present['filling'].calorie*10
        obj.price = int(price*coefficient)
        obj.save()
        present['ful_calorie'] = f'{ful_calorie + filling_ccal:.2f}'
        present['full_weight'] = f'{full_weight+filling_weight:.2f}'

        return present


class Comment(models.Model):
    product = models.ForeignKey(Products, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    moderated = models.BooleanField('проверено модератором',default=False)

    def __str__(self):
        return f'Комменатрий {self.user.username} на {self.product.name_product}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'