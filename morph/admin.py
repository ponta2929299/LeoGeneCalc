from django.contrib import admin
from .models import Gene,Morph,ComboMorph

@admin.register(Gene)
class GeneAdmin(admin.ModelAdmin):
    list_display = ["gene_type"]

admin.site.register(Morph)

@admin.register(ComboMorph)
class ComboMorphAdmin(admin.ModelAdmin):
    filter_horizontal = ["morphs"]