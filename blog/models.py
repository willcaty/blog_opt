from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField("标签", max_length=20, unique=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField()
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    article = models.IntegerField('文章ID')


class Article(models.Model):
    title = models.CharField('标题', max_length=50, )
    body = models.TextField('正文')
    create_at = models.DateTimeField('创建时间', auto_now_add=True)
    abstract = models.CharField('摘要', max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_at']
