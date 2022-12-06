from django.db import models


# Create your models here.

class Poll(models.Model):
    description = models.CharField(max_length=200)
    isActive = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Choice(models.Model):
    choice = models.CharField(max_length=50)
    votes = models.IntegerField(default=0)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return f'{self.choice} {self.poll}'


class Site(models.Model):
    site_name = models.CharField(max_length=50)

    def __str__(self):
        return self.site_name


class SiteAdmin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    site = models.OneToOneField(Site, related_name='admin', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.site}'


class Admin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Voter(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    choices = models.ManyToManyField(Choice, related_name='voters', blank=True)
    answered = models.ManyToManyField(Poll, related_name='answered_by', blank=True)
    site = models.ForeignKey(Site, related_name='voter', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
