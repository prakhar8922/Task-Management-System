from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection


def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)


def serve_react_app(request):
    """Serve the React application"""
    return render(request, 'index.html')
