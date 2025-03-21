from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=300)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, default="")
    director = models.ForeignKey("Director", on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"Movie <{self.id}> {self.name}"

class Director(models.Model):
    name = models.CharField(max_length=300)
    birth_year = models.IntegerField(blank=True, default="")
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Director <{self.id}> {self.name}"
