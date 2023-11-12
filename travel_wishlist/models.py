from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage


class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE) # name other table using string 'auth.user', on_delete=models.CASCADE will delete all data associated with a user
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True) # TextField does not have a limit, CharField does
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True) # ImageField you need to specify a path

    # add new save model, which will override django's save method
    def save(self, *arg, **kwargs):
        old_place =Place.objects.filter(pk=self.pk).first() 
        if old_place and old_place.photo: # check if there is an old place which has an old photo
            if old_place.photo != self.photo: # if old photo does not match current photo
                self.delete_photo(old_place.photo) # delete old photo

        super().save(*arg, **kwargs) # call super class to save
    
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    def delete(self, *arg, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*arg, **kwargs) # call super class to delete

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return f'{self.name} visited? {self.visited} on {self.date_visited}. Photo {photo_str}'