import re
import zipfile
from django.shortcuts import render
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
            print(campos)

        except KeyError:
            return render(request, 'index.html', {'error': 'Arquivo DOCX não enviado'})
        except Exception as e:
            return render(request, 'index.html', {'error': 'Erro ao processar o arquivo'})
            

    return render(request, 'index.html')

def editar_docx(request, campos, docx):
    pass