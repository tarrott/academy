from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=240)
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name_plural = "feedback"


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField(default='profile.jpg', upload_to='resource_logos')
    email = models.EmailField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        width, height = img.size
        if height < width:
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))
        elif width < height:
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))
        if height > 500 and width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
        img.save(self.image.path)


class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=240, null=True, blank=True,
        help_text="Text shown on homepage under the name and image."
    )
    content = models.TextField(null=True, blank=True,
        help_text="Text shown on the individual resource page to describe the resource in depth."
    )
    image = models.ImageField(default='resource_default.jpg', upload_to='resource_logos')
    order = models.SmallIntegerField(unique=True, null=True, blank=True,
        help_text="Order that the resource is displayed on the homepage. Must be unique."
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resource_detail', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 600 or img.width > 1000:
            output_size = (1000, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Session(models.Model):
    name = models.CharField(max_length=240)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)    
    url = models.URLField(null=True, blank=True)
    capacity = models.SmallIntegerField(null=True, blank=True,
        help_text="If speicifed, the number will be shown along with the session title on the homepage and account page."
    )
    full = models.BooleanField(default=False,
        help_text="If checked, then then users can no longer register for the session and it will be greyed out on the homepage."
    )

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True)
    content = models.CharField(max_length=240)

    def __str__(self):
        return self.content
