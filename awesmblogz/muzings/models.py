from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class Entry(models.Model):
    STATUS_CHOICES = ((0, 'draft'),
                      (1, 'hidden'),
                      (2, 'published'),
                      )
    title = models.CharField('title', max_length=255)
    slug = models.SlugField(blank=True)
    content = models.TextField('content')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    date_created = models.DateTimeField('creation date', default=timezone.now)
    date_updated = models.DateTimeField('last update', auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super(Entry, self).save(*args, **kwargs)
