class ObjectsData:
    def __init__(self, result_d, parent1_d, parent2_d_selected, wild_morph, wild_gene,\
        morph_match, gene_match, morph_exclude_match, gene_exclude_match):
        self.result_d = result_d
        self.parent1_d = parent1_d
        self.parent2_d_selected = parent2_d_selected
        self.wild_morph = wild_morph
        self.wild_gene = wild_gene
        self.morph_match = morph_match
        self.gene_match = gene_match
        self.morph_exclude_match = morph_exclude_match
        self.gene_exclude_match = gene_exclude_match
        
        





# [{morph_name:parent1のmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる。
# gene_type:D2
# probability:0.25}
# morph_name:parent1のmorph_nameとまったく一致。
# gene_type:D
# probability:0.5}
# {morph_name:gene_typeに紐づくmorph_nameを表示。
# gene_type:-2
# probability:0.25}]

def result_pattern1(result_d, morph_match, gene_match, parent1_d, wild_morph,wild_gene):
    result_d.append([
                {"morph_name":morph_match,
                "gene_type":gene_match,
                "probability":0.25},
                {"morph_name":parent1_d.morph_name,
                "gene_type":parent1_d.gene_type,
                "probability":0.5},
                {"morph_name":wild_morph,
                "gene_type":wild_gene,
                "probability":0.25}
                ])
    
# [{morph_name:parent1のmorph_nameとまったく一致。
# gene_type:D
# probability:0.25}
# {morph_name:gene_typeに紐づくmorph_nameを表示。
# gene_type:-2
# probability:0.75}]

def result_pattern2(result_d,parent1_d,parent2_d_selected,wild_morph,wild_gene,morph_match, gene_match):
    result_d.append([
                {"morph_name":parent2_d_selected.morph_name,
                "gene_type":parent2_d_selected.gene_type,
                "probability":0.25},
                {"morph_name":wild_morph,
                "gene_type":wild_gene,
                "probability":0.75}
                ])
    
# 同じものがない場合。(D,-)
# list=[{morph_name:parent1のmorph_nameとまったく一致。
# gene_type:D
# probability:0.25}
# {morph_name:gene_typeに紐づくmorph_nameを表示。
# gene_type:-2
# probability:0.75}]

def result_pattern3():
    result_d.append([
                    {"morph_name":parent2_d_selected.morph_name,
                    "gene_type":parent2_d_selected.gene_type,
                    "probability":0.25},
                    {"morph_name":wild_morph,
                    "gene_type":wild_gene,
                    "probability":0.75}
                    ])
    