from django.shortcuts import render
from .forms import MorphSelectForm
from .models import Morph, ComboMorph
from itertools import chain

#Dominantの計算
def calculate_d(parent1_d_select,parent2_d_select):
    #リストの最後にマーカーをつける
    end_instance = Morph.objects.get(morph_name="end")
    parent1_d_selected = parent1_d_select.union(Morph.objects.filter(id=end_instance.id))
    parent2_d_selected = parent2_d_select.union(Morph.objects.filter(id=end_instance.id))
    
    parent1_d_selected = parent1_d_selected.order_by('id')
    parent2_d_selected = parent2_d_selected.order_by("id")

    # parent1_d_selected = chain(parent1_d_select,["end"])
    # parent2_d_selected = chain(parent2_d_select,["end"])
    #計算結果を入れるリスト
    result_d = []
    
    for parent1_d in parent1_d_selected:
        # parent2_d_selected = chain(parent2_d_select,["end"])
        for parent2_d in parent2_d_selected:
            if parent1_d.morph_name != "end":
                if parent2_d.morph_name != "end":  
                    
                    #parent1_dのmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる  
                    morph_instance = Morph.objects.filter(
                    morph_name__exact = f"{parent1_d.morph_name}2c"#parent1_dのmorph_nameを含み、かつ２Cがついてる
                    ).first()
                
                    morph_match = morph_instance.morph_name if morph_instance else None
                    gene_match = morph_instance.gene_type if morph_instance else None

                    # parent1のmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
                    morph_exclude_instance = Morph.objects.filter(
                    morph_name__icontains = parent1_d.morph_name).exclude(morph_name__endswith="2c"
                    ).first()

                    morph_exclude_match = morph_exclude_instance if  morph_exclude_instance else None
                    #上記に紐づくgene_type
                    gene_exclude_match = morph_exclude_instance.gene_type if morph_exclude_instance else None
            
                    print(type(parent1_d))  # parent2_dの型を確認
                                
                    #parent2_dのmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる  
                    morph2_instance = Morph.objects.filter(
                    morph_name__exact = f"{parent2_d.morph_name}2c"#parent1_dのmorph_nameを含み、かつ２Cがついてる
                    ).first()

                    morph2_match = morph_instance.morph_name if morph_instance else None
                    gene2_match = morph_instance.gene_type if morph_instance else None
        
                    # parent2_dのmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
                    morph2_exclude_instance = Morph.objects.filter(
                    morph_name__icontains = parent2_d.morph_name).exclude(morph_name__endswith="2c"
                    ).first()
                    morph2_exclude_match = morph2_exclude_instance.morph_name if  morph2_exclude_instance else None
                    gene2_exclude_match = morph2_exclude_instance.gene_type if morph2_exclude_instance else None
            
                    #Morphモデルの-2というgene_typeを表示する。
                    wild_gene_instance = Morph.objects.filter(
                    gene_type__gene_type__in = ["-2"]
                    ).first()

                    wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
                    #上記に紐づくmorph_name
                    wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
    
                # #parent2_d_selectedの中にある、parent1_d_selectedに含まれていないもの
                # non_match_morph = [parent2_d for parent2_d in parent2_d_selected if parent2_d.morph_name != parent1_d.morph_name ]
                # #non_match_morphのうち、2Cが含まないもの
                # exclude_non_match_morph = [morph_name for morph_name in non_match_morph if not morph_name.morph_name.endswith("2c")]
                
                # まず、parent1がエニグマもしくはホワイト&イエローの場合。
                    if parent1_d.morph_name in ["エニグマ","ホワイト&イエロー"]:    
            
                        #同じmorphなら(D,D)
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
                            continue
                        
                        #同じmorphじゃないなら、(D,x)
                        else:
                            continue

                
                #     #parent1にエニグマもしくはホワイト&イエロー以外がある場合
                #     else:
                #         #(D2,-)or(D,-)
                #         if parent2_d == "end":
                #             #(D2,-)
                #             if parent1_d == morph_match:
                #                 result_d.append([
                #                         {"morph_name":morph_exclude_match,
                #                         "gene_type":gene_exclude_match,
                #                         "probability":1.0}
                #                         ])
                #                 continue
                
                    #(D2,x)or(D,x)  
                    #parent1にエニグマもしくはホワイト&イエロー以外がある場合    
                    else:
                        #(D2,x)
                        if parent1_d == morph_match:
                            #(D2,D2)
                            if parent2_d == parent1_d:
                                result_d.append([
                                    {"morph_name":parent1_d.morph_name,
                                    "gene_type":parent1_d.gene_type,
                                        "probability":1.0}
                                        ])
                                continue
                            
                            #(D2,D)
                            elif parent2_d == morph_exclude_match:
                                    result_d.append([
                                        {"morph_name":parent1_d.morph_name,
                                        "gene_type":parent1_d.gene_type,
                                        "probability":0.5},
                                        {"morph_name":parent2_d.morph_name,
                                        "gene_type":parent2_d.gene_type,
                                        "probability":0.5}
                                        ])
                                    continue
                            else:
                                continue
        
                        #(D,x)    
                        elif parent1_d == morph_exclude_match:
                            
                            #(D,D2)
                            if parent2_d == morph_match:
                                result_d.append([
                                    {"morph_name":parent2_d.morph_name,
                                    "gene_type":parent2_d.gene_type,
                                    "probability":0.5},
                                    {"morph_name":parent1_d.morph_name,
                                    "gene_type":parent1_d.gene_type,
                                    "probability":0.5}
                                    ])
                                continue
                            #(D,D)
                            elif parent2_d == parent1_d:
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
                                continue
                            else:
                                continue

                        else:
                            continue
                # (x,-)
                else:
                    #(D,-)
                    if parent1_d.morph_name in ["エニグマ","ホワイト&イエロー"]:
                        result_d.append([
                            {"morph_name":parent1_d.morph_name,
                            "gene_type":parent1_d.gene_type,
                            "probability":0.5},
                            {"morph_name":wild_morph,
                            "gene_type":wild_gene,
                            "probability":0.5}
                            ])
                        continue
                        
                    else:
                        #(D,-)
                        if parent1_d == morph_exclude_match:
                            result_d.append([
                                {"morph_name":parent1_d.morph_name,
                                "gene_type":parent1_d.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                        #(D2,-)
                        else:
                            result_d.append([
                                {"morph_name":morph_exclude_match,
                                "gene_type":gene_exclude_match,
                                "probability":1.0}
                                ])
                            continue
                
            #(-,x)
            else:
                first_list = []
        
                #parent1_d_selecteedのなかにない、parent2_dをだす。リストa
                #この時点では、2C以外が一致しているmorph_nameも含まれている。
                
                #(-,-)
                if parent2_d == "end":
                    break
        
                elif parent2_d not in parent1_d_selected:
                    first_list.append(parent2_d)
                    
                    #もし、first_listからだしたinclude_2cが、morph_nameに２ｃを含むなら、2cをのぞいたmorph_nameがparent1_d_selectedにあるかみる。
                    #あったら、pass
                    #なっかたら、(-,D2)の計算
                    #bが２ｃを含まないなら、２ｃを足したorph_nameがparent1_d_selectedにあるかみる。
                    #あったら、pass
                    #なっかたら、(-,D)の計算
            
                    for items in first_list:
                        #もし、first_listが(parent2_d)が２ｃを含むなら、
                        #morph2_match = parent2_dのmorph_nameを含み、かつ2Cのついているmorph_name
                        if items == morph2_match:
                                #morph2_exclude_match = b(...2c)の2cがないmorph_nameがparent1_d_selectedにあるかみる。
                                #あったら、該当したmorph_nameをto_removeにいれる。
                            if morph2_exclude_match in parent1_d_selected:
                                first_list.remove(items)
        
                            #parent1_d_listにA2、parent2_dにAという状況の除外
                        if morph2_match in parent1_d_selected:
                            first_list.remove(morph2_match)
                
                        #ここからは、完全に重複のないparent2_d_selectedないのmorph_nameの計算
                    for i in first_list:
                        # (-,D2)
                        if i == morph2_match:
                            result_d.append([
                                {"morph_name":morph2_exclude_match,
                                "gene_type":gene2_exclude_match ,
                                "probability":1.0}
                                ])
                            continue
                        #(-,D)
                        else:
                            result_d.append([
                                {"morph_name":parent2_d.morph_name,
                                "gene_type":parent2_d.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                            continue
                else:
                    continue
                
                # #(-,x)のxが今まで計算されてない遺伝子であったら、
                # if non_match_morph:
                #         #(-,D)
                #         if exclude_non_match_morph:
                #             result_d.append([
                #                     {"morph_name":parent2_d.morph_name,
                #                     "gene_type":parent2_d.gene_type,
                #                     "probability":0.5},
                #                     {"morph_name":wild_morph,
                #                     "gene_type":wild_gene,
                #                     "probability":0.5}
                #                     ])
                #             continue
                #         #(-,D2)
                #         else:
                #             result_d.append([
                #                     {"morph_name":parent2_d.morph_name,
                #                     "gene_type":parent2_d.gene_type,
                #                     "probability":1.0}
                #                     ])
                #             continue
                #parent2_dにparent1_dと異なるものがなっかた場合、

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