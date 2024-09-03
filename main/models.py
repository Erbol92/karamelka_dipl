from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from diplom.settings import MEDIA_ROOT
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
    protein = models.FloatField('белки', default=0)
    fat = models.FloatField('жиры', default=0)
    carbohydrate = models.FloatField('углеводы', default=0)
    calories = models.FloatField('каллории', default=0)

    def __str__(self):
        return f'{self.product.name_product}'

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Cart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False)
    product = models.ForeignKey(
        Products, verbose_name='товар', on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField('кол-во в корзине', default=0)

    def __str__(self):
        return f'{self.user} {self.product.name_product} - {self.quantity} шт.'

    # def __init__(self,user,product,quantity):
    #    pass

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
