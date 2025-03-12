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
    
    super_mack = Morph.object.get(morph_name="スーパーマックスノー")
    mack = Morph.object.get(morph_name="マックスノー")
    super_lemon = Morph.object.get(morph_name="スーパーレモンフロスト")
    lemon = Morph.object.get(morph_name="レモンフロスト")
    
    #Morphモデルの-2というgene_typeを表示する。
    wild_gene_instance = Morph.objects.filter(
    gene_type__gene_type__in = ["-2"]
    ).first()
    wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
    #上記に紐づくmorph_name
    wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
    
    result_c = []
    
    for parent1_c in parent1_c_selected:
        print(result_c)
        for parent2_c in parent2_c_selected:
            if parent1_c.morph_name != "end":
                if parent2_c.morph_name != "end":
                    #Morphモデルの-2というgene_typeを表示する。
                    wild_gene_instance = Morph.objects.filter(
                    gene_type__gene_type__in = ["-2"]
                    ).first()

                    wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
                    #上記に紐づくmorph_name
                    wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
                    
                    #(M2,x)
                    if parent1_c == super_mack:
                        #(M2,M2)
                        if parent2_c == parent1_c:
                            result_c.append([
                                    {"morph_name":parent1_c.morph_name,
                                    "gene_type":parent1_c.gene_type,
                                        "probability":1.0}
                                        ])
                            continue
                        #(M2,M)
                        elif parent2_c == mack:
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
                        
                    #(M,x)
                    if parent1_c == mack:
                        #(M,M)
                        if parent2_c == parent1_c:
                            result_c.append([
                                {"morph_name":super_mack.morph_name,
                                "gene_type":super_mack.gene_type,
                                "probability":0.25},
                                {"morph_name":parent1_c.morph_name,
                                "gene_type":parent1_c.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.25}
                                ])         
                            continue
                        #(M,M2)
                        elif parent2_c == super_mack:
                            result_c.append([
                                        {"morph_name":parent2_c.morph_name,
                                        "gene_type":parent2_c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":parent1_c.morph_name,
                                        "gene_type":parent1_c.gene_type,
                                        "probability":0.5}
                                        ])
                            continue
                        else:
                            continue
                    
                #(x,-)
                else:
                    first_list = []
                    #parent2_c_selectedのなかにない、parent1_cをだす。リスト
                    #この時点では、2C以外が一致しているmorph_nameも含まれている
                    
                    if parent1_c.morph_name == "end":
                        break
                    
                    elif parent1_c not in parent2_d_selected:
                        first_list.append(parent1_d)
                        
                        # for items in first_list:
                        # #もし、first_listが(parent1_d)が２ｃを含むなら、
                        # #morph_match = parent1_dのmorph_nameを含み、かつ2Cのついているmorph_name
                        #     if items == morph_match:
                        #         #morph_exclude_match = b(...2c)の2cがないmorph_nameがparent1_d_selectedにあるかみる。
                        #         #あったら、該当したmorph_nameをto_removeにいれる。
                        #         if morph_exclude_match in parent1_d_selected:
                        #             first_list.remove(items)
        
                        #     #parent2_d_listにA2、parent2_dにAという状況の除外
                        #     if morph_match in parent2_d_selected:
                        #         first_list.remove(morph_match)
                    
                    
                    
                    
                    #(M2,-)
                    if parent1_c == super_mack:
                        result_c.append([
                                {"morph_name":mack.morph_name,
                                "gene_type":mack.gene_type ,
                                "probability":1.0}
                                ])
                        continue
                    #(M,-)
                    elif parent1_c == mack:
                        result_c.append([
                                {"morph_name":mack.morph_name,
                                "gene_type":mack.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                        continue
                    #(L2,-)
                    elif parent1_c == super_lemon:
                        result_c.append([
                                {"morph_name":lemon.morph_name,
                                "gene_type":lemon.gene_type ,
                                "probability":1.0}
                                ])
                        continue
                    #(L,-)
                    elif parent1_c == lemon:
                        result_c.append([
                                {"morph_name":lemon.morph_name,
                                "gene_type":lemon.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                        continue
                        
                    else:
                        break
            #(-,x)
            else:
                #(-,M2)
                if parent2_c == super_mack:
                    result_c.append([
                            {"morph_name":mack.morph_name,
                            "gene_type":mack.gene_type ,
                            "probability":1.0}
                            ])
                    continue
                #(-,M)
                elif parent2_c == mack:
                    result_c.append([
                            {"morph_name":mack.morph_name,
                            "gene_type":mack.gene_type,
                            "probability":0.5},
                            {"morph_name":wild_morph,
                            "gene_type":wild_gene,
                            "probability":0.5}
                            ])
                    continue
                #(-,L2)
                elif parent2_c == super_lemon:
                    result_c.append([
                            {"morph_name":lemon.morph_name,
                            "gene_type":lemon.gene_type ,
                            "probability":1.0}
                            ])
                    continue
                #(-,L)
                elif parent2_c == lemon:
                    result_c.append([
                            {"morph_name":lemon.morph_name,
                            "gene_type":lemon.gene_type,
                            "probability":0.5},
                            {"morph_name":wild_morph,
                            "gene_type":wild_gene,
                            "probability":0.5}
                            ])
                    continue
                        
                else:
                    break