from django.shortcuts import render
from django.http import JsonResponse
from .task import analyze_video_comments

def analyze_video(request):
    if request.method == 'POST':
        url = request.POST.get('youtube_url', '')
        video_id = url.split('v=')[-1].split('&')[0]  
        task = analyze_video_comments.delay(video_id)
        return JsonResponse({'task_id': task.id})
    return render(request, 'analyzer/form.html')

def get_task_result(request, task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    if result.ready():
        return JsonResponse({'status': 'done', 'result': result.get()})
    return JsonResponse({'status': 'pending'})