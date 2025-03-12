from django.shortcuts import render
from .forms import MorphSelectForm
from .models import Morph, ComboMorph

#Co_Dominantの計算
def calculate_c(parent1_c_select,parent2_c_select):
    #リストの最後にマーカーをつける
    end_instance = Morph.objects.get(morph_name="end")
    parent1_c_selected = parent1_c_select.union(Morph.objects.filter(id=end_instance.id))
    parent2_c_selected = parent2_c_select.union(Morph.objects.filter(id=end_instance.id))
    
    parent1_c_selected = parent1_c_selected.order_by('id')
    parent2_c_selected = parent2_c_selected.order_by("id")
    
    result_c = []
    
    for parent1_c in parent1_c_selected:
        print(result_c)
        for parent2_c in parent2_c_selected:
            if parent1_c.morph_name != "end":
                if parent2_c.morph_name != "end":  
                    
                    # #parent1_cのmorph_nameを含み、かつhetのついているmorph_nameをMorphモデルからさがしいれる  
                    # morph_instance = Morph.objects.filter(
                    # morph_name__exact = f"het {parent1_c.morph_name}"#parent1_cのmorph_nameを含み、かつhetがついてる
                    # ).first()
                
                    # morph_match = morph_instance.morph_name if morph_instance else None
                    # gene_match = morph_instance.gene_type if morph_instance else None

                    # # parent1のmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
                    # morph_exclude_instance = Morph.objects.filter(
                    # morph_name__icontains = parent1_c.morph_name).exclude(morph_name__endswith="2c"
                    # ).first()

                    # morph_exclude_match = morph_exclude_instance if  morph_exclude_instance else None
                    # #上記に紐づくgene_type
                    # gene_exclude_match = morph_exclude_instance.gene_type if morph_exclude_instance else None
                                
                    # #parent2_cのmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる  
                    # morph2_instance = Morph.objects.filter(
                    # morph_name__exact = f"{parent2_c.morph_name}2c"#parent1_dのmorph_nameを含み、かつ２Cがついてる
                    # ).first()

                    # morph2_match = morph_instance.morph_name if morph_instance else None
                    # gene2_match = morph_instance.gene_type if morph_instance else None
        
                    # # parent2_cのmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
                    # morph2_exclude_instance = Morph.objects.filter(
                    # morph_name__icontains = parent2_c.morph_name).exclude(morph_name__endswith="2c"
                    # ).first()
                    # morph2_exclude_match = morph2_exclude_instance.morph_name if  morph2_exclude_instance else None
                    # gene2_exclude_match = morph2_exclude_instance.gene_type if morph2_exclude_instance else None
            
                    #Morphモデルの-2というgene_typeを表示する。
                    wild_gene_instance = Morph.objects.filter(
                    gene_type__gene_type__in = ["-2"]
                    ).first()

                    wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
                    #上記に紐づくmorph_name
                    wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
    
                # #parent2_c_selectedの中にある、parent1_c_selectedに含まれていないもの
                # non_match_morph = [parent2_c for parent2_d in parent2_c_selected if parent2_c.morph_name != parent1_c.morph_name ]
                # #non_match_morphのうち、2Cが含まないもの
                # exclude_non_match_morph = [morph_name for morph_name in non_match_morph if not morph_name.morph_name.endswith("2c")]
                
                # まず、parent1がエニグマもしくはホワイト&イエローの場合。
                    if parent1_c.morph_name in ["エニグマ","ホワイト&イエロー"]:    
            
                        #同じmorphなら(D,D)
                        if parent1_c == parent2_c:
                            result_c.append([
                            {"morph_name":morph_match,
                            "gene_type":gene_match,
                            "probability":0.25},
                            {"morph_name":parent1_c.morph_name,
                            "gene_type":parent1_c.gene_type,
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
                #         #(C2,-)or(C,-)
                #         if parent2_d == "end":
                #             #(C2,-)
                #             if parent1_d == morph_match:
                #                 result_d.append([
                #                         {"morph_name":morph_exclude_match,
                #                         "gene_type":gene_exclude_match,
                #                         "probability":1.0}
                #                         ])
                #                 continue
                
                    #(C2,x)or(C,x)  
                    #parent1にエニグマもしくはホワイト&イエロー以外がある場合    
                    else:
                        #(C2,x)
                        if parent1_c== morph_match:
                            #(D2,D2)
                            if parent2_c == parent1_c:
                                result_c.append([
                                    {"morph_name":parent1_c.morph_name,
                                    "gene_type":parent1_c.gene_type,
                                        "probability":1.0}
                                        ])
                                continue
                            
                            #(D2,D)
                            elif parent2_c == morph_exclude_match:
                                    result_c.append([
                                        {"morph_name":parent1_c.morph_name,
                                        "gene_type":parent1_c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":parent2_c.morph_name,
                                        "gene_type":parent2_c.gene_type,
                                        "probability":0.5}
                                        ])
                                    continue
                            else:
                                continue
        
                        #(D,x)    
                        elif parent1_c == morph_exclude_match:
                            
                            #(D,D2)
                            if parent2_c == morph_match:
                                result_c.append([
                                    {"morph_name":parent2_c.morph_name,
                                    "gene_type":parent2_c.gene_type,
                                    "probability":0.5},
                                    {"morph_name":parent1_c.morph_name,
                                    "gene_type":parent1_c.gene_type,
                                    "probability":0.5}
                                    ])
                                continue
                            #(C,C)
                            elif parent2_c == parent1_c:
                                result_c.append([
                                {"morph_name":morph_match,
                                "gene_type":gene_match,
                                "probability":0.25},
                                {"morph_name":parent1_c.morph_name,
                                "gene_type":parent1_c.gene_type,
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
                    first_list = []
                    #parent2_c_selecteedのなかにない、parent1_cをだす。リストa
                    #この時点では、2C以外が一致しているmorph_nameも含まれている
                    
                    if parent1_c == "end":
                        break
                    
                    elif parent1_c not in parent2_c_selected:
                        first_list.append(parent1_c)
                        
                        for items in first_list:
                        #もし、first_listが(parent1_c)が２ｃを含むなら、
                        #morph_match = parent1_cのmorph_nameを含み、かつ2Cのついているmorph_name
                            if items == morph_match:
                                #morph_exclude_match = b(...2c)の2cがないmorph_nameがparent1_c_selectedにあるかみる。
                                #あったら、該当したmorph_nameをto_removeにいれる。
                                if morph_exclude_match in parent1_c_selected:
                                    first_list.remove(items)
        
                            #parent2_d_listにA2、parent2_dにAという状況の除外
                            if morph_match in parent2_c_selected:
                                first_list.remove(morph_match)
                                
                        #ここからは、完全に重複のないparent2_c_selectedないのmorph_nameの計算
                        for j in first_list:
                            # (C2,-)
                            if j == morph_match:
                                result_c.append([
                                {"morph_name":morph_exclude_match,
                                "gene_type":gene_exclude_match ,
                                "probability":1.0}
                                ])
                                continue
                            #(C,-)
                            else:
                                result_c.append([
                                {"morph_name":parent1_c.morph_name,
                                "gene_type":parent1_c.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                continue
                                            
                    else:
                        continue
                
            #(-,x)
            else:
                second_list = []
        
                #parent1_c_selecteedのなかにない、parent2_cをだす。リストa
                #この時点では、2C以外が一致しているmorph_nameも含まれている。
                
                #(-,-)
                if parent2_c == "end":
                    break
        
                elif parent2_c not in parent1_c_selected:
                    second_list.append(parent2_c)
                    
                    #もし、first_listからだしたinclude_2cが、morph_nameに２ｃを含むなら、2cをのぞいたmorph_nameがparent1_c_selectedにあるかみる。
                    #あったら、pass
                    #なっかたら、(-,C2)の計算
                    #bが２ｃを含まないなら、２ｃを足したorph_nameがparent1_c_selectedにあるかみる。
                    #あったら、pass
                    #なっかたら、(-,C)の計算
            
                    for items in second_list:
                        #もし、first_listが(parent2_c)が２ｃを含むなら、
                        #morph2_match = parent2_cのmorph_nameを含み、かつ2Cのついているmorph_name
                        if items == morph2_match:
                                #morph2_exclude_match = b(...2c)の2cがないmorph_nameがparent1_c_selectedにあるかみる。
                                #あったら、該当したmorph_nameをto_removeにいれる。
                            if morph2_exclude_match in parent1_c_selected:
                                second_list.remove(items)
        
                            #parent1_c_listにA2、parent2_dにAという状況の除外
                        if morph2_match in parent1_c_selected:
                            second_list.remove(morph2_match)
                
                        #ここからは、完全に重複のないparent2_c_selectedないのmorph_nameの計算
                    for i in second_list:
                        # (-,C2)
                        if i == morph2_match:
                            result_c.append([
                                {"morph_name":morph2_exclude_match,
                                "gene_type":gene2_exclude_match ,
                                "probability":1.0}
                                ])
                            continue
                        #(-,D)
                        else:
                            result_c.append([
                                {"morph_name":parent2_c.morph_name,
                                "gene_type":parent2_c.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                            continue
                else:
                    continue
    
    return(result_c)


# #parent1_cのmorph_nameを含み、かつhetのついているmorph_nameをMorphモデルからさがしいれる  
#  morph_instance = Morph.objects.filter(
#  morph_name__exact = f"het {parent1_c.morph_name}"#parent1_cのmorph_nameを含み、かつhetがついてる
#  ).first()
                
#  morph_het_match = morph_instance.morph_name if morph_instance else None
#  gene_match = morph_instance.gene_type if morph_instance else None

#                     # parent1のmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
#                     morph_exclude_instance = Morph.objects.filter(
#                     morph_name__icontains = parent1_c.morph_name).exclude(morph_name__endswith="2c"
#                     ).first()

#                     morph_exclude_match = morph_exclude_instance if  morph_exclude_instance else None
#                     #上記に紐づくgene_type
#                     gene_exclude_match = morph_exclude_instance.gene_type if morph_exclude_instance else None
                                
#                     #parent2_cのmorph_nameを含み、かつ2Cのついているmorph_nameをMorphモデルからさがしいれる  
#                     morph2_instance = Morph.objects.filter(
#                     morph_name__exact = f"{parent2_c.morph_name}2c"#parent1_dのmorph_nameを含み、かつ２Cがついてる
#                     ).first()

#                     morph2_match = morph_instance.morph_name if morph_instance else None
#                     gene2_match = morph_instance.gene_type if morph_instance else None
        
#                     # parent2_cのmorph_nameを含み、かつ2Cを含まないmorph_nameをMorphモデルからさがしいれる
#                     morph2_exclude_instance = Morph.objects.filter(
#                     morph_name__icontains = parent2_c.morph_name).exclude(morph_name__endswith="2c"
#                     ).first()
#                     morph2_exclude_match = morph2_exclude_instance.morph_name if  morph2_exclude_instance else None
#                     gene2_exclude_match = morph2_exclude_instance.gene_type if morph2_exclude_instance else None
            
#                     #Morphモデルの-2というgene_typeを表示する。
#                     wild_gene_instance = Morph.objects.filter(
#                     gene_type__gene_type__in = ["-2"]
#                     ).first()

#                     wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
#                     #上記に紐づくmorph_name
#                     wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
    