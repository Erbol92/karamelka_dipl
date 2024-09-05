from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from diplom.settings import MEDIA_ROOT
from main.models import Cart, Products
# Create your models here.

class UserProxy(User):
    class Meta:
        proxy = True

    def add_cart(self, product):
        update_values = {
            'user':self,
            'product':product,
            # 'quantity':1,
        }
        obj, created = Cart.objects.update_or_create(user=self, product=product, defaults=update_values)
        if not created:
            obj.quantity +=1
            obj.save()
        return f'{product} добавлен, в корзине {obj.quantity} шт.'
    
class Profile(models.Model):
    def image_path(self, instance):
        return f'{MEDIA_ROOT}/profile/{self.prof}/{self.photo.name}'
    prof = models.OneToOneField(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False)
    phone = models.CharField('№ тел.', max_length=15, null=True)
    address = models.CharField('адрес', max_length=120, null=True)
    photo = models.ImageField('фото', upload_to=image_path, null=True)

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
            this = Profile.objects.filter(id=self.id).first()
            if this and this.photo != self.photo:
                self.photo = self.compress_logo(self.photo)
                this.photo.delete(save=False)
        except ValueError:
            pass
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'профиль {self.prof}'

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиля"