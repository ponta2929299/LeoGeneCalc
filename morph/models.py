from django.db import models
import json

#遺伝子タイプ
class Gene(models.Model):
    TYPE_CHOICES=[
        ("D","顕性het"),
        ("D2","顕性homo"),
        ("C","共顕性het"),
        ("C2","共顕性homo"),
        ("R2","潜性homo"),
        ("R","潜性het"),
        ("-2","ワイルドhomo"),
        ("-","ワイルドhet"),
        ("N","no_name"),
    ]
    gene_type = models.CharField(max_length = 10,choices = TYPE_CHOICES) 
    
    def __str__(self):
        return self.get_gene_type_display()
    #日本語ラベルを表示
    
    
#単一モルフ
class Morph(models.Model):
    id = models.AutoField(primary_key=True)
    morph_name = models.CharField(max_length = 100)
    gene_type = models.ForeignKey(Gene, on_delete=models.PROTECT)
    morph_detail = models.TextField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.morph_name == "end":
            max_id = Morph.objects.aggregate(models.Max('id'))['id__max']
            self.id = max_id + 1 if max_id else 1
        super(Morph, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.morph_name
    
    
    
    
#コンボモルフ
class ComboMorph(models.Model):
    combo_morph_name = models.CharField(max_length = 100,primary_key=True)
    morphs = models.ManyToManyField(Morph)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.combo_morph_name
    
    #計算結果が既存のコンボモルフと一致するか確認する
    def check_and_return_existing_combo(self):
        calculated_morph = set(self.morphs.all())
        
        existing_combos = ComboMorph.objects.all()
        for combo in existing_combos:
            if calculated_morph == set(combo.morphs.all()):
                return combo
        return None