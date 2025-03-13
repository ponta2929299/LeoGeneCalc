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
    
    super_mack = Morph.objects.get(morph_name="スーパーマックスノー")
    mack = Morph.objects.get(morph_name="マックスノー")
    super_lemon = Morph.objects.get(morph_name="スーパーレモンフロスト")
    lemon = Morph.objects.get(morph_name="レモンフロスト")
    
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
                    #(M2,x)
                    if parent1_c == super_mack:
                        #(M2,M2)
                        if parent2_c == parent1_c:
                            result_c.append([
                                    {"morph_name":parent1_c.morph_name,
                                    "gene_type":parent1_c.gene_type,
                                        "probability":1.0}
                                        ])
                            print(f"1{result_c}")
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
                            print(f"2{result_c}")
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
                            print(f"3{result_c}")
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
                            print(f"4{result_c}")
                            continue
                        else:
                            continue
                    
                #(x,-)
                else:
                    if parent1_c.morph_name == "end":
                        print(f"finally1{result_c}")
                        break
                    #(M2,-)
                    elif parent1_c == super_mack:
                        if mack not in parent2_c_selected and super_mack not in parent2_c_selected:
                                result_c.append([
                                    {"morph_name":mack.morph_name,
                                    "gene_type":mack.gene_type,
                                    "probability":1.0}
                                    ])
                                print(f"5{result_c}")
                                continue
                    #(M,-)
                    elif parent1_c == mack:
                        if mack not in parent2_c_selected and super_mack not in parent2_c_selected:
                                result_c.append([
                                    {"morph_name":mack.morph_name,
                                    "gene_type":mack.gene_type,
                                    "probability":0.5},
                                    {"morph_name":wild_morph,
                                    "gene_type":wild_gene,
                                    "probability":0.5}
                                    ])
                                print(f"6{result_c}")
                                continue
                    #(L2,-)
                    elif parent1_c == super_lemon:
                        if lemon not in parent2_c_selected and super_lemon not in parent2_c_selected:
                                result_c.append([
                                    {"morph_name":lemon.morph_name,
                                    "gene_type":lemon.gene_type,
                                    "probability":1.0}
                                    ])
                                print(f"7{result_c}")
                                continue
                    #(L,-)
                    elif parent1_c == lemon:
                        if lemon not in parent2_c_selected and super_lemon not in parent2_c_selected:
                                result_c.append([
                                    {"morph_name":lemon.morph_name,
                                    "gene_type":lemon.gene_type,
                                    "probability":0.5},
                                    {"morph_name":wild_morph,
                                    "gene_type":wild_gene,
                                    "probability":0.5}
                                    ])
                                print(f"8{result_c}")
                                continue
            #(-,x)
            else:
                if parent2_c.morph_name == "end":
                    print(f"finally2{result_c}")
                    break
                #(-,M2)
                if parent2_c == super_mack:
                    if mack not in parent1_c_selected and super_mack not in parent1_c_selected:
                                result_c.append([
                                {"morph_name":mack.morph_name,
                                "gene_type":mack.gene_type ,
                                "probability":1.0}
                                ])
                                print(f"9{result_c}")
                                continue
                #(-,M)
                elif parent2_c == mack:
                    if mack not in parent1_c_selected and super_mack not in parent1_c_selected:
                                result_c.append([
                                {"morph_name":mack.morph_name,
                                "gene_type":mack.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"10{result_c}")
                                continue
                #(-,L2)
                elif parent2_c == super_lemon:
                    if lemon not in parent1_c_selected and super_lemon not in parent1_c_selected:
                                result_c.append([
                                {"morph_name":lemon.morph_name,
                                "gene_type":lemon.gene_type ,
                                "probability":1.0}
                                ])
                                print(f"11{result_c}")
                                continue
                #(-,L)
                elif parent2_c == lemon:
                    if lemon not in parent1_c_selected and super_lemon not in parent1_c_selected:
                                result_c.append([
                                {"morph_name":lemon.morph_name,
                                "gene_type":lemon.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"12{result_c}")
                                continue
    return(result_c)