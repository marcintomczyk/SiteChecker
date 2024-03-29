from django.db import models


class Site(models.Model):
    # for the current project it might seem unnecessary to have urlfield as we have validation on the view
    # but for bigger projects there might be other 'site_checkers' without validation on a view layer
    original_address = models.URLField(max_length=200)
    final_address = models.URLField(max_length=200, blank=True)
    status_code = models.PositiveSmallIntegerField()
    # yes, I've found django-unixtimestampfield but didn't want to install additional dependency for something so simple
    check_date = models.IntegerField()
    error_message = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return self.original_address
