import base64
from io import BytesIO
import io
import os
import re
import traceback
import uuid
from django import forms
from django.http import FileResponse
from django.shortcuts import redirect, render
from docxtpl import DocxTemplate
from django.core.cache import cache

from core.forms import DocumentoForm
from core.models import Documento
from docxforms import settings



def extrair_campos(docx):
    campos = []
    for p in docx.get_docx().paragraphs:
        matches = re.findall(r"\{\{\s*(\w+)\s*\}\}", p.text)
        for match in matches:
            if match not in campos:
                campos.append(match)
    
    for tabela in docx.get_docx().tables:
        for row in tabela.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    matches = re.findall(r"\{\{\s*(\w+)\s*\}\}", p.text)
                    for match in matches:
                        if match not in campos:
                            campos.append(match)
    return campos

def serializar_arquivo(arquivo):
    bytes = arquivo.read()
    return base64.b64encode(bytes).decode('utf-8')

def guardar_em_memoria(request, dados):
    for key, value in dados.items():
        request.session[key] = value

def guardar_media(file):
    doc= file.read()
    path = os.path.join(settings.MEDIA_ROOT,'temp',file.name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(doc)
    return path
    


def inicio(request):
    if request.method == 'POST':
        try:
           
            form = DocumentoForm(request.POST, request.FILES)
            if form.is_valid():
                doc=form.save()
                doc_id = doc.id
                return redirect(f'edit/?key={doc_id}')

        except KeyError:
            return render(request, 'index.html', {'error': 'Arquivo DOCX não enviado'})
        except Exception as e:
            print(str(e))
            return render(request, 'index.html', {'error': 'Erro ao processar o arquivo'})

    return render(request, 'index.html', {'form':DocumentoForm()})

def editar_docx(request):
    #campos_recebidos = request.session.get('campos',[])
    #campos_formatados = [s.replace("_", " ") for s in campos_recebidos]
    #nome_arquivo = request.session.get('nome_arquivo','')
    #docx_path = request.session.get('docx_path')
    
    doc_id= request.GET.get('key')
    documento = Documento.objects.get(id=doc_id)

    with documento.arquivo.open('rb') as f:
        file_bytes = io.BytesIO(f.read())
        docx = DocxTemplate(file_bytes)
        campos = extrair_campos(docx)

        print(campos)
    
    if request.method == 'POST':
        path = os.path.join(settings.MEDIA_ROOT, 'temp', nome_arquivo)
        print(path)
        with open(path,'rb') as f:
            doc = DocxTemplate(f)
            doc.render({"nome":"lucas"})
            #output = BytesIO()
            #doc.save(output)
            #output.seek(0)
            #return FileResponse(output, as_attachment=True, filename="documento_editado.docx")

    return render(request, 'edit.html', {'campos':campos, 'nome_arquivo': 'nome_arquivo'})