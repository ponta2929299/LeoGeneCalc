from django.shortcuts import render
from .forms import MorphSelectForm
from .models import Morph, ComboMorph

#Dominantの計算
def calculate_d(parent1_d_select,parent2_d_select):
    #リストの最後にマーカーをつける
    end_instance = Morph.objects.get(morph_name="end")
    parent1_d_selected = parent1_d_select.union(Morph.objects.filter(id=end_instance.id))
    parent2_d_selected = parent2_d_select.union(Morph.objects.filter(id=end_instance.id))
    
    parent1_d_selected = parent1_d_selected.order_by('id')
    parent2_d_selected = parent2_d_selected.order_by("id")
    
    enigma_2c = Morph.objects.get(id=23)
    enigma = Morph.objects.get(id=24)
    wy_2c = Morph.objects.get(id=25)
    wy = Morph.objects.get(id=26)
    gem_2c = Morph.objects.get(id=27)
    gem = Morph.objects.get(id=28)
    tug_2c = Morph.objects.get(id=29)
    tug = Morph.objects.get(id=30)
    ghost_2c = Morph.objects.get(id=31)
    ghost = Morph.objects.get(id=32)
    
    #Morphモデルの-2というgene_typeを表示する。
    wild_gene_instance = Morph.objects.filter(
    gene_type__gene_type__in = ["-2"]
    ).first()
    wild_gene = wild_gene_instance.gene_type if wild_gene_instance else None
    #上記に紐づくmorph_name
    wild_morph = wild_gene_instance.morph_name if wild_gene_instance else None
    

    result_d = []
    
    for parent1_d in parent1_d_selected:
        
        for parent2_d in parent2_d_selected:
            if parent1_d.morph_name != "end":
                if parent2_d.morph_name != "end": 
                    #(E,x)
                    if parent1_d == enigma:
                        #(E,E)
                        if parent2_d == parent1_d:
                            result_d.append([
                            {"morph_name":enigma_2c.morph_name,
                            "gene_type":enigma_2c.gene_type,
                            "probability":0.25},
                            {"morph_name":enigma.morph_name,
                            "gene_type":enigma.gene_type,
                            "probability":0.5},
                            {"morph_name":wild_morph,
                            "gene_type":wild_gene,
                            "probability":0.25}
                            ])
                            print(f"1{result_d}")
                            continue
                        #(E,other)
                        else:
                            continue
                    #(W,x)
                    elif parent1_d == wy:
                        #(W,W)
                        if parent2_d == parent1_d:
                            if parent2_d == parent1_d:
                                result_d.append([
                                {"morph_name":wy_2c.morph_name,
                                "gene_type":wy_2c.gene_type,
                                "probability":0.25},
                                {"morph_name":wy.morph_name,
                                "gene_type":wy.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.25}
                                ])
                                print(f"2{result_d}")
                                continue
                        #(W,other)
                        else:
                            continue
                    #(G2,x)
                    elif parent1_d == gem_2c:    
                        #(G2,G2)
                        if parent2_d == parent1_d:
                            result_d.append([
                                    {"morph_name":gem_2c.morph_name,
                                    "gene_type":gem_2c.gene_type,
                                        "probability":1.0}
                                        ])
                            print(f"3{result_d}")
                            continue
                        #(G2,G)
                        if parent2_d == gem:
                            result_d.append([
                                        {"morph_name":gem_2c.morph_name,
                                        "gene_type":gem_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":gem.morph_name,
                                        "gene_type":gem.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"4{result_d}")
                            continue
                        #(G2,other)
                        else:
                            continue
                    #(G,x)
                    elif parent1_d == gem:
                        #(G,G2)
                        if parent2_d == gem_2c:
                            result_d.append([
                                        {"morph_name":gem_2c.morph_name,
                                        "gene_type":gem_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":gem.morph_name,
                                        "gene_type":gem.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"5{result_d}")
                            continue
                        #(G,G)
                        elif parent2_d == parent1_d:
                                result_d.append([
                                {"morph_name":gem_2c.morph_name,
                                "gene_type":gem_2c.gene_type,
                                "probability":0.25},
                                {"morph_name":gem.morph_name,
                                "gene_type":gem.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.25}
                                ])
                                print(f"6{result_d}")
                                continue
                        #(G,other)
                        else:
                            continue
                    #(T2,x)
                    elif parent1_d == tug_2c:
                        #(T2,T2)
                        if parent2_d == parent1_d:
                            result_d.append([
                                    {"morph_name":tug_2c.morph_name,
                                    "gene_type":tug_2c.gene_type,
                                    "probability":1.0}
                                    ])
                            print(f"7{result_d}")
                            continue
                        #(T2,T)
                        if parent2_d == tug:
                            result_d.append([
                                        {"morph_name":tug_2c.morph_name,
                                        "gene_type":tug_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":tug.morph_name,
                                        "gene_type":tug.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"8{result_d}")
                            continue
                        #(T2,other)
                        else:
                            continue
                    #(T,x)    
                    elif parent1_d == tug:
                        #(T,T2)
                        if parent2_d == tug_2c:
                            result_d.append([
                                        {"morph_name":tug_2c.morph_name,
                                        "gene_type":tug_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":tug.morph_name,
                                        "gene_type":tug.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"9{result_d}")
                        #(T,T)
                        elif parent2_d == parent1_d:
                            result_d.append([
                                {"morph_name":tug_2c.morph_name,
                                "gene_type":tug_2c.gene_type,
                                "probability":0.25},
                                {"morph_name":tug.morph_name,
                                "gene_type":tug.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.25}
                                ])
                            print(f"10{result_d}")
                            continue
                        #(T,other)
                        else:
                            continue
                    #(GH2,x)
                    elif parent1_d == ghost_2c:
                        #(GH2,GH2)
                        if parent2_d == parent1_d:
                            result_d.append([
                                    {"morph_name":ghost_2c.morph_name,
                                    "gene_type":ghost_2c.gene_type,
                                    "probability":1.0}
                                    ])
                            print(f"11{result_d}")
                            continue
                        #(GH2,GH)
                        elif parent2_d == ghost:
                            result_d.append([
                                        {"morph_name":ghost_2c.morph_name,
                                        "gene_type":ghost_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":ghost.morph_name,
                                        "gene_type":ghost.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"12{result_d}")
                        #(GH2,other)
                        else:
                            continue
                    #(GH,x)
                    if parent1_d == ghost:
                        #(GH,GH2)
                        if parent2_d == ghost_2c:
                            result_d.append([
                                        {"morph_name":ghost_2c.morph_name,
                                        "gene_type":ghost_2c.gene_type,
                                        "probability":0.5},
                                        {"morph_name":ghost.morph_name,
                                        "gene_type":ghost.gene_type,
                                        "probability":0.5}
                                        ])
                            print(f"13{result_d}")
                        #(GH,GH)
                        elif parent2_d == parent1_d:
                            result_d.append([
                                {"morph_name":ghost_2c.morph_name,
                                "gene_type":ghost_2c.gene_type,
                                "probability":0.25},
                                {"morph_name":ghost.morph_name,
                                "gene_type":ghost.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.25}
                                ])
                            print(f"14{result_d}")
                        #(GH,other)
                        else:
                            continue
                #(x,-)
                else:
                    first_list = []
                    #parent2_c_selectedのなかにない、parent1_cをだす。リスト
                    
                    if parent1_d.morph_name == "end":
                        print(f"finally1{result_d}")
                        break
                    
                    # elif parent1_d not in parent2_d_selected:
                    #     first_list.append(parent1_d)
                    #     print("first{first_list}")
                        
                    #     for i in first_list:
                    #(E,-)
                    elif parent1_d == enigma:
                        if enigma not in parent2_d_selected and enigma_2c not in parent2_d_selected:
                            result_d.append([
                                {"morph_name":enigma.morph_name,
                                "gene_type":enigma.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                            print(f"15{result_d}")
                            continue
                    #(W,-)
                    elif parent1_d == wy:
                        if wy not in parent2_d_selected and wy_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":wy.morph_name,
                                "gene_type":wy.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"16{result_d}")
                                continue
                    #(G2,-)
                    elif  parent1_d == gem_2c:
                        if gem not in parent2_d_selected and gem_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":gem.morph_name,
                                "gene_type":gem.gene_type,
                                "probability":1.0}
                                ])
                                print(f"17{result_d}")
                                continue
                    #(G,-)
                    elif parent1_d == gem:
                        if gem not in parent2_d_selected and gem_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":gem.morph_name,
                                "gene_type":gem.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"18{result_d}")
                                continue
                    #(T2,-)
                    elif parent1_d == tug_2c:
                        if tug not in parent2_d_selected and tug_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":tug.morph_name,
                                "gene_type":tug.gene_type,
                                "probability":1.0}
                                ])
                                print(f"19{result_d}")
                                continue
                    #(T,-)
                    elif parent1_d == tug:
                        if tug not in parent2_d_selected and tug_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":tug.morph_name,
                                "gene_type":tug.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"20{result_d}")
                                continue
                    #(GH2,-)
                    elif parent1_d == ghost_2c:
                        if ghost not in parent2_d_selected and ghost_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":ghost.morph_name,
                                "gene_type":ghost.gene_type,
                                "probability":1.0}
                                ])
                                print(f"21{result_d}")
                                continue
                    #(GH,-)
                    elif parent1_d == ghost:
                        if ghost not in parent2_d_selected and ghost_2c not in parent2_d_selected:
                                result_d.append([
                                {"morph_name":ghost.morph_name,
                                "gene_type":ghost.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"22{result_d}")
                                continue
                    
            #(-,x)                    
            else:
                # #(-,-)
                if parent2_d.morph_name == "end":
                    print(f"finally1{result_d}")
                    break
                # #(-,x)
                # elif parent2_d not in parent1_d_selected:
                #         second_list.append(parent2_d)
                        
                #         for j in second_list:
                #(-,E)
                if parent2_d == enigma:
                    if enigma not in parent1_d_selected and enigma_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":enigma.morph_name,
                                "gene_type":enigma.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"23{result_d}")
                                continue
                #(-,W)
                elif parent2_d == wy:
                    if wy not in parent1_d_selected and wy_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":wy.morph_name,
                                "gene_type":wy.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"24{result_d}")
                                continue
                #(-,G2)
                elif parent2_d == gem_2c:
                    if gem not in parent1_d_selected and gem_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":gem.morph_name,
                                "gene_type":gem.gene_type,
                                "probability":1.0}
                                ])
                                print(f"25{result_d}")
                                continue
                #(-,G)
                elif parent2_d == gem:
                    if gem not in parent1_d_selected and gem_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":gem.morph_name,
                                "gene_type":gem.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"26{result_d}")
                                continue
                #(-,T2)
                elif parent2_d == tug_2c:
                    if tug not in parent1_d_selected and tug_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":tug.morph_name,
                                "gene_type":tug.gene_type,
                                "probability":1.0}
                                ])
                                print(f"27{result_d}")
                                continue
                #(-,T)
                elif parent2_d == tug:
                    if tug not in parent1_d_selected and tug_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":tug.morph_name,
                                "gene_type":tug.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"28{result_d}")
                                continue
                #(-,GH2)
                elif parent2_d == ghost_2c:
                    if ghost not in parent1_d_selected and ghost_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":ghost.morph_name,
                                "gene_type":ghost.gene_type,
                                "probability":1.0}
                                ])
                                print(f"29{result_d}")
                                continue
                #(-,GH)
                elif parent2_d == ghost:
                    if ghost not in parent1_d_selected and ghost_2c not in parent1_d_selected:
                                result_d.append([
                                {"morph_name":ghost.morph_name,
                                "gene_type":ghost.gene_type,
                                "probability":0.5},
                                {"morph_name":wild_morph,
                                "gene_type":wild_gene,
                                "probability":0.5}
                                ])
                                print(f"30{result_d}")
                                continue
    return(result_d)