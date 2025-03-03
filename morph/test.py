from .models import Morph, ComboMorph

queryset = Morph.objects.filter(gene_type__in=["D2","D"]).exclude(morph_name__in=["エニグマ２C","ホワイト&イエロー２C"])

print (queryset.query)