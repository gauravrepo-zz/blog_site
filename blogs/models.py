from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

def upload_location(instance, filename):
    file_path = 'blogs/{username}/{title}-image.jpg'.format(
        username=str(instance.author.username), title=str(instance.title)
    )
    return file_path

# Blog model
class Blog(models.Model):
    
    title           = models.CharField(verbose_name="Blog Title", max_length=60)
    body            = models.CharField(verbose_name="Blog body", max_length=3000)
    image           = models.ImageField(upload_to=upload_location, null=True, blank=True)
    is_draft        = models.BooleanField(verbose_name="Draft mode", default=True)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE)
    date_posted     = models.DateTimeField(verbose_name="Date posted", auto_now=False, auto_now_add=True)
    date_updated    = models.DateTimeField(verbose_name="Date updated", auto_now=True, auto_now_add=False)
    slug            = models.SlugField(blank=True, unique=True)
    main_image      = ImageSpecField(source="image", processors=[ResizeToFill(960, 540)], format='JPEG')
    thumb_image     = ImageSpecField(source="image", processors=[ResizeToFill(410, 240)], format='JPEG', options={'quality': 80})


    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("Post_detail", kwargs={"pk": self.pk})

@receiver(post_delete, sender= Blog)
def delete_post_image(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(pre_save, sender=Blog)
def pre_post_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)
pre_save.connect(pre_post_save, sender=Blog)

