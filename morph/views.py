from django.shortcuts import render, redirect
from morph.forms import MorphSelectForm
from morph.models import Morph, ComboMorph
from morph.dominant import calculate_d
import json
from django.contrib import messages

def dominant_morph_view(request):
    if request.method == "POST":
        form = MorphSelectForm(request.POST)
        if form.is_valid():
            
            #親１
            parent1_d_select = form.cleaned_data["parent1_d_morphs"]
            # parent1_c_selected = form.cleaned_data["parent1_c_morphs"]
            # parent1_r_selected = form.cleaned_data["parent1_r_morphs"]
            # parent1_wild_selected = form.cleaned_data["parent1_wild_morphs"]
            
            
        #同じmorphのhomoとhetが重複した場合、エラーをだす。
            grouped_1 = {}
            
            for morph1_exclude2c in parent1_d_select:
                #2cを除去したmorph_nameを変数にいれる。
                if morph1_exclude2c.morph_name.endswith("2c"):
                    base_name = morph1_exclude2c.morph_name[:-2]
                else:
                    base_name = morph1_exclude2c.morph_name
                
                #base_nameをキーとした空のリスト作成。（重複なし）
                if base_name not in grouped_1:
                    grouped_1[base_name] = [] 
                
                #上記のリストにユーザーの選択したmorphを入れてく
                grouped_1[base_name].append(morph1_exclude2c)
                
                #base_nameというキーと、groupという変数にいれた値のペア。groupが重複したら、エラー表示。
                for base_name, group in grouped_1.items():
                    if len(group) > 1:
                        messages.error(request, f"親１のモルフ「{base_name}が重複しています。」")
                        return redirect("calculate")
            
            
            #親２
            parent2_d_select = form.cleaned_data["parent2_d_morphs"]
            # parent2_c_selected = form.cleaned_data["parent2_c_morphs"]
            # parent2_r_selected = form.cleaned_data["parent2_r_morphs"]
            # parent2_wild_selected = form.cleaned_data["parent2_wild_morphs"]
            
            
        #同じmorphのhomoとhetが重複した場合、エラーをだす。    
            grouped_2 = {}
            
            for morph2_exclude2c in parent2_d_select:
                base_name = morph2_exclude2c.morph_name.rstrip('2c')
                
                if base_name not in grouped_2:
                    grouped_2[base_name] = []
                    
                grouped_2[base_name].append(morph2_exclude2c)
                
                for base_name, group in grouped_2.items():
                    if len(group) > 1:
                        messages.error(request, f"親２のモルフ「{base_name}が重複しています。」")
                        return redirect("calculate")
            
            if parent1_d_select:
            #関数呼び出し
                dominant_result = calculate_d(parent1_d_select,parent2_d_select)
                if dominant_result:
                    #呼び出した結果をsessionに保存(sessionにはJSON形式で入るため、str型になおす)
                    request.session["result_d"] = json.dumps(dominant_result, default=str)
                    return redirect("result")
            
            else:
                pass
            
    else:
        form = MorphSelectForm()
        
    return render(request, "morph/calculate.html", {"form":form})

def result_view(request):
    
    result_d_json = request.session.get("result_d","結果がありません")
    result_d = json.loads(result_d_json)
    
    return render(request,"morph/result.html",{"result_d":result_d})