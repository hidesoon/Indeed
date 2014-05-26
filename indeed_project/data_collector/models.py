from django.db import models

class Search(models.Model):
    date = models.DateTimeField()
    term = models.CharField(max_length=100)
    def __unicode__(self):
        return self.term

class Links(models.Model):
    search = models.ForeignKey(Search)
    link = models.CharField(max_length=100)
    def __unicode__(self):
        return self.link

class Location(models.Model):
    search = models.ForeignKey(Search)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    def __unicode__(self):
        return u'%s, %s' %(self.city, self.state)

class Results(models.Model):
    search = models.ForeignKey(Search)
    # if false is bigram
    is_bigram = models.BooleanField()
    word = models.CharField(max_length=150)
    count = models.IntegerField(default=0)
    # may be empty string when search doesn't involve pos tag
    pos = models.CharField(max_length=5)
    def __unicode__(self):
        # there is a pos tag
        if self.pos != u"":
            return u'(%s, %s, %s)' %(self.word,self.count,self.pos)
        else:
            return u'(%s, %s)' %(self.word,self.count)