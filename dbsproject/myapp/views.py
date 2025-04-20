import yaml
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
import json
import ollama

# -*- coding: utf-8 -*-
import os

from embedchain import App
app = None


def get_model_config(llm_name, embedder_name):
    global app
    db_folder = f"./db/{embedder_name}"
    os.makedirs(db_folder, exist_ok=True)
    llm_model = {
        "provider": "ollama",
        "config": {
            "model": llm_name,
            "temperature": 0.5,
            "top_p": 1,
            "stream": True,
            "base_url": "http://localhost:11434",
            "system_prompt": "你是資料庫系統這堂課的AI課程助教，請針對資料庫系統這門課程的內容或上課綱要，依據上下文用繁體中文回答問題，並且確保回答詳細且準確。"
        }

    }

    if embedder_name == "gpt4all_embedder":
        embedding_model = {
            "provider": "gpt4all"
        }
    else:
        embedding_model = {
            "provider": "huggingface",
            "config": {
                "model": "sentence-transformers/"+embedder_name,
                "model_kwargs": {
                    "trust_remote_code": True
                }
            }
        }

    # print(embedding_model)
    config = {
        "llm": llm_model,
        "embedder": embedding_model,
        "vectordb": {
            'provider': 'chroma',
            'config': {
                'collection_name': 'full-stack-app',
                'dir': db_folder,
                'allow_reset': True
            }
        }
    }
    print(config)
    app = App.from_config(config=config)
    return app


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@csrf_exempt
def upload_pdf(request):
    if request.method == "POST":
        if "pdf_files" not in request.FILES:
            return JsonResponse({"error": "沒有選擇任何檔案"}, status=400)

        files = request.FILES.getlist("pdf_files")
        uploaded_files = []

        for file in files:
            file_path = os.path.join(UPLOAD_FOLDER, file.name)

            # 儲存文件到伺服器
            path = default_storage.save(file_path, ContentFile(file.read()))
            uploaded_files.append(file.name)

            # **自動加入 app**
            app.add(path, data_type="pdf_file")

        return JsonResponse({"message": "PDF 上傳成功", "files": uploaded_files}, status=200)

    return JsonResponse({"error": "只接受 POST 請求"}, status=405)


def homepage(request):

    return render(request, 'home.html')


@csrf_exempt
def dbschatbot(request):
    global app
    model_name = request.GET.get('llm', '')  # 從URL中取得模型名稱
    embedder_name = request.GET.get('embedder', '')
    # print(model_name)
    if model_name and embedder_name:  # 如果有選擇模型
        try:
            get_model_config(model_name, embedder_name)  # 初始化選定的模型配置
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'POST':
        user_question = request.POST.get('user_question', '')
        response = app.query(user_question)  # 使用選定的模型處理問題
        return JsonResponse({'response': response})
    return render(request, 'chatbot2.html', {'response': ''})
