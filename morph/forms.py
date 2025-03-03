from django import forms
from .models import Morph, ComboMorph

class MorphSelectForm(forms.Form):
    #親１の遺伝子選択
    parent1_d_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["D2","D"]).exclude(morph_name__in=["エニグマ２C","ホワイト&イエロー２C"]),\
        label="顕性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    # parent1_c_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["C2","C"]),\
    #     label="共顕性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    # parent1_r_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["R2","R"]),\
    #     label="潜性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    # parent1_wild_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["-2","-"]),\
    #     label="ワイルドモルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    #親２の遺伝子選択
    parent2_d_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["D2","D"]).exclude(morph_name__in=["エニグマ２C","ホワイト&イエロー２C"]),\
        label="顕性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    # parent2_c_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["C2","C"]),\
    #     label="共顕性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}), required = False)
    
    # parent2_r_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["R2","R"]),\
    #     label="潜性モルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)
    
    # parent2_wild_morphs = forms.ModelMultipleChoiceField(queryset=Morph.objects.filter(gene_type__gene_type__in=["-2","-"]),\
    #     label="ワイルドモルフ",widget=forms.SelectMultiple(attrs={"class":"form-control"}),required = False)