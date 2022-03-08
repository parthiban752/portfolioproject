from random import choices
from django.db import models
from users.models import Profile

# Create your models here.
class Project(models.Model):
    projectlist=[('static','static application'),
                    ('dynamic','dynamic application'),
            ]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='photos/',default='photos/website.jpg',null=True,blank=True)
    demo_link = models.CharField(max_length=2000,null=True,blank=True)
    source_link = models.CharField(max_length=2000,null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    created=models.DateTimeField(auto_now_add=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    type = models.CharField(max_length=20,choices=projectlist,null=True,blank=True)

    def __str__(self):
        return self.title

    @property
    def getvotecount(self):
        reviews = self.review_set.all()
        upvotes = reviews.filter(value='up').count()
        totalcount = reviews.count()
        voteratio = (upvotes/totalcount)*100

        self.vote_total = totalcount
        self.vote_ratio = voteratio
        self.save()

    @property
    def reviewers(self):
        reviewers = self.review_set.all().values_list('owner__id',flat=True)
        return reviewers

class Review(models.Model):
    values=[('up','like'),('down','unlike')]
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=20,choices=values,default='up')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner','project']]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name










