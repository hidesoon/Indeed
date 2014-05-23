from django.db import models



class Search(models.Model):
    date = models.DateField()
    term = models.CharField(max_length=100)

class Links(models.Model):
    search = models.ForeignKey(Search)
    link = models.CharField(max_length=100)

class Location(models.Model):
    search = models.ForeignKey(Search)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)

class Results(models.Model):
    search = models.ForeignKey(Search)
    is_unigram = models.BooleanField()
    is_bigram = models.BooleanField()
    word = models.CharField(max_length=150)
    count = models.IntegerField(default=0)




