from django.shortcuts import render, redirect
from morph.forms import MorphSelectForm
from morph.models import Morph, ComboMorph
from morph.dominant import calculate_d
import json

def dominant_morph_view(request):
    if request.method == "POST":
        form = MorphSelectForm(request.POST)
        if form.is_valid():
            #親１
            parent1_d_selected = form.cleaned_data["parent1_d_morphs"]
            # parent1_c_selected = form.cleaned_data["parent1_c_morphs"]
            # parent1_r_selected = form.cleaned_data["parent1_r_morphs"]
            # parent1_wild_selected = form.cleaned_data["parent1_wild_morphs"]
            
            
            #親２
            parent2_d_selected = form.cleaned_data["parent2_d_morphs"]
            # parent2_c_selected = form.cleaned_data["parent2_c_morphs"]
            # parent2_r_selected = form.cleaned_data["parent2_r_morphs"]
            # parent2_wild_selected = form.cleaned_data["parent2_wild_morphs"]
            
            gene2_instance = parent2_d_selected.gene_type
            gene2_dict = gene2_instance.to_dict()
            gene2_json = json.dump(gene2_dict)
            print(gene2_json)
            
            if parent1_d_selected:
            #関数呼び出し
                dominant_result = calculate_d(parent1_d_selected,parent2_d_selected)
                if dominant_result:
                    #呼び出した結果をsessionに保存
                    request.session["result_d"] = dominant_result
                    return redirect("result")
            
            else:
                pass
            
    else:
        form = MorphSelectForm()
        
    return render(request, "morph/calculate.html", {"form":form})

def result_view(request):
    
    result_d = request.session.get("result_d","結果がありません")
    
    return render(request,"result.html",{"result_d":result_d})