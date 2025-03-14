from rest_framework import serializers
from morph.models import Gene, Morph, ComboMorph

# Geneのシリアライザー
class GeneSerializer(serializers.ModelSerializer):
    gene_type_display = serializers.CharField(source='get_gene_type_display', read_only=True)

    class Meta:
        model = Gene
        fields = ['gene_type', 'gene_type_display']

# Morphのシリアライザー
class MorphSerializer(serializers.ModelSerializer):
    gene_type = GeneSerializer()  # Geneの詳細も含める

    class Meta:
        model = Morph
        fields = '__all__'

# ComboMorphのシリアライザー
class ComboMorphSerializer(serializers.ModelSerializer):
    morphs = MorphSerializer(many=True)  # 多対多のMorphのデータもJSONに含める

    class Meta:
        model = ComboMorph
        fields = '__all__'
