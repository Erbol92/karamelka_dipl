from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from diplom.settings import MEDIA_ROOT
from main.models import Cart, Products
from datetime import datetime, timedelta
from diplom.settings import days_after, days_before
# Create your models here.

class UserProxy(User):
    class Meta:
        proxy = True

    def check_discount(self, days_before=days_before, days_after=days_after):
        profile = self.profile
        if profile.b_date:
            today = datetime.now().date()
            dm_date = profile.b_date.replace(year=today.year)
            start_date = dm_date - timedelta(days=days_before)
            end_date = dm_date + timedelta(days=days_after)
            print(start_date,today,end_date)
            return start_date <= today <= end_date
        return False

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
    
    def sum_cart(self):
        summary = 0
        for cart in self.carts.all():
            summary +=cart.get_pos_sum()
        for cart in self.carts_constr.all():
            summary +=cart.get_sum()
        return summary
    
class Profile(models.Model):
    def image_path(self, instance):
        return f'{MEDIA_ROOT}/profile/{self.prof}/{self.photo.name}'
    prof = models.OneToOneField(
        User, verbose_name='пользователь', on_delete=models.CASCADE, null=False, related_name='profile')
    b_date = models.DateField('дата рождения', null=True, blank=True)
    phone = models.CharField('№ тел.', max_length=16, null=True)
    address = models.CharField('адрес', max_length=120, null=True)
    photo = models.ImageField('фото', upload_to=image_path, null=True, blank=True)
    b_date_last_change = models.DateField('дата изменения д.р.', null=True, blank=True)

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