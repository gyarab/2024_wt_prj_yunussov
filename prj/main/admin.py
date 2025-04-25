from django.contrib import admin
from .models import Movie, Director

class MovieAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "year", "director", "description"]
    
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "birth_year", "description"]

# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Director, DirectorAdmin)
