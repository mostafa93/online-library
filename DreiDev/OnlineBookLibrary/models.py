from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class Library(models.Model):
    library_owner = models.OneToOneField(User)
    library_name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.library_name)
        super(Library, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.library_name

    def get_absolute_url(self):
        return reverse("library-detail", kwargs={"slug": self.slug})


class Book(models.Model):
    library = models.ForeignKey(Library)
    book_title = models.CharField(max_length=128, unique=True)
    book_author = models.CharField(max_length=64, unique=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.book_title)
        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.book_title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"slug": self.slug})
