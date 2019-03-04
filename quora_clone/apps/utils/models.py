from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class CreationModificationDateMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('creation date and time'), auto_now_add=True)
    updated_at = models.DateTimeField(_('modification date and time'), auto_now=True)


class MetaTagsMixin(models.Model):
    class Meta:
        abstract = True

    meta_description = models.CharField(_('Description'), max_length=255, blank=True)
    meta_keywords = models.CharField(_('Keywords'),
                                     max_length=255,
                                     blank=True, help_text=_('Separate keywords by comma.'))
    meta_author = models.CharField(_('Author'), max_length=255, blank=False)
    meta_copyright = models.CharField(_('Copyright'), max_length=255, blank=True)

    @staticmethod
    def get_meta(name, content):
        tag = ''
        if name and content:
            tag = render_to_string(template_name='utils/_meta_tag.html', context={'name': name,
                                                                                  'content': content}
                                   )
        return mark_safe(tag)

    def get_meta_description(self):
        return self.get_meta('description', self.meta_description)

    def get_meta_keywords(self):
        return self.get_meta('keywords', self.meta_keywords)

    def get_meta_author(self):
        return self.get_meta('author', self.meta_author)

    def get_meta_copyright(self):
        return self.get_meta('copyright', self.meta_copyright)

    def get_meta_tags(self):
        meta_tags = (self.meta_description, self.meta_keywords, self.meta_author, self.meta_copyright)
        meta_tags_string = '\n'.join(meta_tags)
        return mark_safe(meta_tags_string)
