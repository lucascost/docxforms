import base64
import re
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

def serializar_arquivo(arquivo):
    bytes = arquivo.read()
    return base64.b64encode(bytes).decode('utf-8')

def guardar_em_memoria(request, dados):
    for key, value in dados.items():
        request.session[key] = value


def inicio(request):
    if request.method == 'POST':
        try:
            file = request.FILES['docx_file']

            if not file.name.endswith('.docx'):
                return render(request, 'index.html', {'error': 'O arquivo enviado não é um DOCX válido'})

            docx = DocxTemplate(file)
            campos = extrair_campos(docx)
            
            docx_bytes = serializar_arquivo(file)

            guardar_em_memoria(request,{
                'docx_bytes':docx_bytes,
                'campos': campos,
                'nome_arquivo':file.name
                })

            return redirect('edit/')

        except KeyError:
            return render(request, 'index.html', {'error': 'Arquivo DOCX não enviado'})
        except Exception as e:
            return render(request, 'index.html', {'error': 'Erro ao processar o arquivo'})

    return render(request, 'index.html')

def editar_docx(request):
    campos_recebidos = request.session.get('campos',[])
    campos_formatados = [s.replace("_", " ") for s in campos_recebidos]

    nome_arquivo = request.session.get('nome_arquivo','')

    return render(request, 'edit.html', {'campos':campos_formatados, 'nome_arquivo': nome_arquivo})