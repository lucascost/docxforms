from django.shortcuts import render
from docxtpl import DocxTemplate

def inicio(request):
    if request.method == 'POST':
        doc = DocxTemplate(request.FILES['docx_file'])
        print("arquivo recebido")


    return render(request, 'index.html')