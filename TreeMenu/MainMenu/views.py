from django.shortcuts import render

def base_pattern(request, path):
    return render(request, 'base.html')