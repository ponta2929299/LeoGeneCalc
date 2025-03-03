from django.shortcuts import render
from .forms import MorphSelectForm
from .models import Morph, ComboMorph
import json
# from .result_functions import result_pattern1,result_pattern2,result_pattern3,result_pattern4



#Dominantの計算
def calculate_d(parent1_d_selected,parent2_d_selected):
    #計算結果を入れるリスト
    result_d = []
    for parent1_d in parent1_d_selected:
        for parent2_d in parent2_d_selected:
            if parent1_d:
                
                gene1_instance = parent1_d.gene_type
                gene1_dict = gene1_instance.to_dict()
                gene1_json = json.dump(gene1_dict)
                print(gene1_json)
                        
                #parent1_dのmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる  
                morph_instance = Morph.objects.filter(
                morph_name__icontains = parent1_d.morph_name,#parent1_dのmorph_nameを含む
                morph_name__endswith = "２C"#かつ２Cがついてる
                ).first()
        
                morph_match = morph_instance.morph_name if morph_instance else "該当なし"
                gene_match = morph_instance.gene_type if morph_instance else "該当なし"

                # parent1のmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
                morph_exclude_instance = Morph.objects.filter(
                morph_name__icontains = parent1_d.morph_name).exclude(morph_name__endswith="２C"
                ).first()

                morph_exclude_match = morph_exclude_instance if  morph_exclude_instance else "該当なし"
                #上記に紐づくgene_type
                gene_exclude_match = morph_exclude_instance.gene_type if morph_exclude_instance else "該当なし"

                #Morphモデルの-2というgene_typeを表示する。
                wild_gene_instance = Morph.objects.filter(
                gene_type__gene_type__in = ["-2"]
                ).first()

                wild_gene = wild_gene_instance.gene_type
                #上記に紐づくmorph_name
                wild_morph = wild_gene_instance.morph_name

                #parent2_d_selectedの中にある、parent1_d_selectedに含まれていないもの
                non_match_morph = [morph_name for morph_name in parent2_d_selected if morph_name != parent1_d ]
                
                #non_match_morphのうち、2Cが含まないもの
                exclude_non_match_morph = [morph_name for morph_name in non_match_morph if not morph_name.morph_name.endswith("２C")]
                
            
                # まず、parent1がエニグマもしくはホワイト&イエローの場合。
                if parent1_d.morph_name in ["エニグマ","ホワイト&イエロー"]:

                    # parent1とまったく同じものがparent2にあったら、100%(D,D)
                    if parent1_d == parent2_d:
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

                        #parent2_d_selectedにparent1_d_selected内以外のものがあるかみる。(-,D)
                        if non_match_morph:
                                result_d.append([
                                    {"morph_name":parent2_d.morph_name,
                                    "gene_type":parent2_d.gene_type,
                                    "probability":0.25},
                                    {"morph_name":wild_morph,
                                    "gene_type":wild_gene,
                                    "probability":0.75}
                                    ])

                    #同じものがない場合(D,-)
                    else:
                        result_d.append([
                            {"morph_name":parent1_d.morph_name,
                            "gene_type":parent1_d.gene_type,
                            "probability":0.25},
                            {"morph_name":wild_morph,
                            "gene_type":wild_gene,
                            "probability":0.75}
                            ])
                
                        #parent2_d_selectedにparent1_d_selected内以外のものがあるかみる。(-,D)
                        if non_match_morph:
                            result_d.append([
                                {"morph_name":parent2_d.morph_name,
                                "gene_type":parent2_d.gene_type,
                                "probability":0.25},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.75}
                                ])
            
                # parent1がエニグマもしくはホワイト&イエロー以外の場合(else)。(つまり、ゴーストorTUGorGEM)            
                else:
                    # parent1とまったく同じものがparent2にあるか、探す。
                    if parent1_d == parent2_d:

                        # それが２ｃを含むかみる。2cの場合、(D2,D2)100% D2
                        if "２C" in parent1_d.morph_name:                     
                            result_d.append([
                                    {"morph_name":parent1_d.morph_name,
                                    "gene_type":parent1_d.gene_type,
                                    "probability":1.0}
                                    ])
    
                            # parent2_d_selectedにparent1_d_selected以外のものがあるかみる。
                            if non_match_morph:                       
                        
                                # あった場合、それが２ｃを含むかみる。(-,D2)100%D
                                if exclude_non_match_morph:
                                    result_d.append([
                                        {"morph_name":parent2_d.morph_name,
                                        "gene_type":parent2_d.gene_type,
                                        "probability":1.0}
                                        ])
                
                                # 2cを含まない場合、(-,D)
                                else:
                                    result_d.append([
                                        {"morph_name":parent2_d.morph_name,
                                        "gene_type":parent2_d.gene_type,
                                        "probability":0.25},
                                        {"morph_name":wild_morph,
                                        "gene_type":wild_gene,
                                        "probability":0.75}
                                        ])
                                                    
                        # 含まない場合(D,D)
                        else:
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
    
                            # parent2_d_selectedにparent1_d_selected以外のものがあるかみる。
                            if non_match_morph:
                            
                                # あった場合、それが２ｃを含むかみる。(-,D2)100%D
                                if exclude_non_match_morph:
                                    result_d.append([
                                    {"morph_name":parent2_d.morph_name,
                                    "gene_type":parent2_d.gene_type,
                                    "probability":1.0}
                                    ])

                                # 2cを含まない場合、(-,D)
                                else:
                                    result_d.append([
                                    {"morph_name":parent2_d.morph_name,
                                    "gene_type":parent2_d.gene_type,
                                    "probability":0.25},
                                    {"morph_name":wild_morph,
                                    "gene_type":wild_gene,
                                    "probability":0.75}
                                    ])

                    # 次に、まったく同じものがparent2になかった場合。
                    else:
                        # それが２ｃを含むかみる。
                        if "２C" in parent1_d.morph_name:
                    
                            # parent1とおなじmorph_nameを含むものがparent2にあるかみる。(D2,D)
                            if parent2_d.morph_name in parent1_d.morph_name:
                                result_d.append([
                                    {"morph_name":parent1_d.morph_name,
                                    "gene_type":parent1_d.gene_type,
                                    "probability":0.5},
                                    {"morph_name":morph_exclude_match,
                                    "gene_type":gene_exclude_match,
                                    "probability":0.5}
                                    ])
    
                                # parent2_d_selectedにparent1_d_selected以外のものがあるかみる。
                                if non_match_morph:
                    
                                    # あった場合、それが２ｃを含むかみる。(-,D2)100%D
                                    if exclude_non_match_morph:
                                        result_d.append([
                                            {"morph_name":parent2_d.morph_name,
                                            "gene_type":parent2_d.gene_type,
                                            "probability":1.0}
                                            ])

                                    # 2cを含まない場合、(-,D)
                                    else:
                                        result_d.append([
                                            {"morph_name":parent2_d.morph_name,
                                            "gene_type":parent2_d.gene_type,
                                            "probability":0.25},
                                            {"morph_name":wild_morph,
                                            "gene_type":wild_gene,
                                            "probability":0.75}
                                            ])

                            # ない場合、(D2,-)100%D    
                            else:
                                result_d.append([
                                    {"morph_name":morph_exclude_match,
                                    "gene_type":gene_exclude_match,
                                    "probability":1.0}
                                    ])
        
                                # parent2_d_selectedにparent1_d_selected以外のものがあるかみる。
                                if non_match_morph:
                        
                                    # あった場合、それが２ｃを含むかみる。(-,D2)100%D
                                    if exclude_non_match_morph:
                                        result_d.append([
                                            {"morph_name":parent2_d.morph_name,
                                            "gene_type":parent2_d.gene_type,
                                            "probability":1.0}
                                            ])

                                    # 2cを含まない場合、(-,D)
                                    else:
                                        result_d.append([
                                            {"morph_name":parent2_d.morph_name,
                                            "gene_type":parent2_d.gene_type,
                                            "probability":0.25},
                                            {"morph_name":wild_morph,
                                            "gene_type":wild_gene,
                                            "probability":0.75}
                                            ])

                        #２ｃを含まない場合(D,-)        
                        else:
                            result_d.append([
                                {"morph_name":parent1_d.morph_name,
                                "gene_type":parent1_d.gene_type,
                                "probability":0.25},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.75}
                                ])

                            # parent2_d_selectedにparent1_d_selected以外のものがあるかみる。
                            if non_match_morph:
                                
                                # あった場合、それが２ｃを含むかみる。(-,D2)100%D
                                if exclude_non_match_morph:
                                    result_d.append([
                                        {"morph_name":parent2_d.morph_name,
                                        "gene_type":parent2_d.gene_type,
                                        "probability":1.0}
                                        ])
            
                                # 2cを含まない場合、(-,D)
                                else:
                                    result_d.append([
                                        {"morph_name":parent2_d.morph_name,
                                        "gene_type":parent2_d.gene_type,
                                        "probability":0.25},
                                        {"morph_name":wild_morph,
                                        "gene_type":wild_gene,
                                        "probability":0.75}
                                        ])

            else:
                pass
            
    return result_d


"""
result_d = []
大きいリスト(遺伝子型ごと)に小さいリスト(モルフごと)を作成。さらにその中はディクショナリー(算出結果ごと)。
確率計算する際は、リストやディクショナリーのインデックス番号で指定してする。

まず、parent1がエニグマもしくはホワイト&イエローの場合。
parent1とまったく同じものがparent2にあるか、探す。
あった場合。100%(D,D)だから、
list=[{morph_name:parent1のmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる。
gene_type:D2
probability:0.25}
morph_name:parent1のmorph_nameとまったく一致。
gene_type:D
probability:0.5}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.25}]

同じものがない場合。(D,-)
list=[{morph_name:parent1のmorph_nameとまったく一致。
gene_type:D
probability:0.25}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.75}]

parent2_d_selectedにparent1_d_selected内以外のものがどうかみる。
あった場合、(-,D)
list=[{morph_name:parent2のmorph_nameとまったく一致。
gene_type:D
probability:0.25}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.75}]
            
            
次に、計算したことのない、parent1_d_selectedをみる。(ゴーストでない)
上記の作業を繰り返し、新しいリストにいれてく。
            
上記が終わったら、
parent1がエニグマもしくはホワイト&イエロー以外の場合(else)。(つまり、ゴーストorTUGorGEM)
あった場合、parent1とまったく同じものがparent2にあるか、探す。
それが２ｃを含むかみる。
2cの場合、(D2,D2)100% D2だから、
list=[{morph_name:parent1のmorph_nameとまったく一致。
gene_type:D2
probability:1.0}
含まない場合(D,D)、
list=[{morph_name:parent1のmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる。
gene_type:D2
probability:0.25}
{morph_name:parent1のmorph_nameとまったく一致。
gene_type:D
probability:0.5}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.25}]
                        
次に、まったく同じものがparent2になかった場合。
それが２ｃを含むかみる。
2cの場合、
parent1とおなじmorph_nameを含むものがparent2にあるかみる。
あった場合、(D2,D)
list=[{morph_name:parent1のmorph_nameとまったく一致。
gene_type:D2
probability:0.5}
{morph_name:parent1のmorph_nameを含み、かつ2Cを含まないmorph_name。
gene_type:D
probability:0.5}]
                        
ない場合、(D2,-)100%D
list=[{morph_name:parent1のmorph_nameを含み、かつ2Cを含まないmorph_name。
gene_type:D
probability:1.0}]
                
2cを含まない場合、(D,-)
list=[{morph_name:parent1のmorph_nameとまったく一致。
gene_type:D
probability:0.25}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.75}]
                        
parent2_d_selectedにparent1_d_selected内以外のものがあるかみる。
あった場合、それが２ｃを含むかみる。
2cの場合、(-,D2)100%Dだから、
list=[{morph_name:parent2のmorph_nameとまったく一致。
gene_type:D
probability:1.0}
                        
2cを含まない場合、(-,D)
list=[{morph_name:parent2のmorph_nameとまったく一致。
gene_type:D
probability:0.25}
{morph_name:gene_typeに紐づくmorph_nameを表示。
gene_type:-2
probability:0.75}]
"""