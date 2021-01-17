from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _ 

def upload_to(instance, filename):
    return f'posts/{filename}'

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):

    # custom model manager
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = [
        ('draft','Draft'),
        ('published','Published'),
    ]

    category = models.ForeignKey(
        Category,on_delete = models.PROTECT,default=1 )
    title = models.CharField(max_length=100)
    image = models.ImageField( _("Image"), upload_to= 'media/posts/', default='posts/default.jpg')
    excerpt = models.TextField(null=True)
    content = models.TextField()    
    slug = models.SlugField(max_length=250,unique_for_date='published') 
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='blog_posts' )
    status = models.CharField(
        max_length=10,choices=options,default='published' )

    # model managers
    #default 
    objects = models.Manager()
    # custom
    postobjects = PostObjects()

    class Meta:
        ordering = ('-published',)
    
    def __str__(self):
        return self.title

