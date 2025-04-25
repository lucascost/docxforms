import base64
from io import BytesIO
import re
import zipfile
from django import forms
from django.shortcuts import redirect, render
from docxtpl import DocxTemplate

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

def inicio(request):

    if request.method == 'POST':
        try:
            docx = DocxTemplate(request.FILES['docx_file'])

            if not request.FILES['docx_file'].name.endswith('.docx'):
                return render(request, 'index.html', {'error': 'O arquivo enviado não é um DOCX válido'})

            campos = extrair_campos(docx)
            

        except KeyError:
            return render(request, 'index.html', {'error': 'Arquivo DOCX não enviado'})
        except Exception as e:
            return render(request, 'index.html', {'error': 'Erro ao processar o arquivo'})
        
        docx = request.FILES['docx_file']
        docx_bytes= docx.read()
        
        docx_serializado = docx_bytes.decode('latin1')

        request.session['docx_bytes'] = docx_serializado
        request.session['campos'] = campos
        
        return redirect('edit/')

    return render(request, 'index.html')

def editar_docx(request):
    campos_recebidos = request.session.get('campos',[])
    campos_formatados = [s.replace("_", " ") for s in campos_recebidos]
    return render(request, 'edit.html', {'campos':campos_formatados})