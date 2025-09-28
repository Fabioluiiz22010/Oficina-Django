from django.shortcuts import render, redirect, get_object_or_404
from .models import Servico
from datetime import timedelta 

def format_timedelta_to_time_string(td):
    if td is None:
        return '00:00:00'
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def listaServicos(request):
    servicos = Servico.objects.all()
    context = {'servicos': servicos}
    # Template name corrigido
    return render(request, 'servicos/listaServicos.html', context) 

def criarServico(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        tempo_str = request.POST.get('tempo')
        preco = request.POST.get('preco')
        
        if descricao and tempo_str and preco:
            try:
                # 1. Tratar o tempo (assumindo HH:MM ou HH:MM:SS)
                parts = tempo_str.split(':')
                if len(parts) == 2: # Formato HH:MM
                    hours, minutes = map(int, parts)
                    seconds = 0
                elif len(parts) == 3: # Formato HH:MM:SS
                    hours, minutes, seconds = map(int, parts)
                else:
                    raise ValueError("Formato de tempo inválido.")

                tempo_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

                Servico.objects.create(
                    descricao=descricao,
                    tempo=tempo_delta,
                    preco=preco
                )
                return redirect('listaServicos')
            
            except ValueError:
                # Captura erro de formato de tempo
                error_message = 'Formato de tempo inválido. Use o formato HH:MM:SS.'
                context = {'error_message': error_message, 'servico': {'descricao': descricao, 'tempo': tempo_str, 'preco': preco}}
                return render(request, 'servicos/criarServico.html', context)
            
            except Exception as e:
                # Captura IntegrityError (NOT NULL) ou outros erros de banco
                error_message = f'Erro ao cadastrar: Verifique se todos os campos obrigatórios foram preenchidos. Detalhe: {e}'
                context = {'error_message': error_message, 'servico': {'descricao': descricao, 'tempo': tempo_str, 'preco': preco}}
                return render(request, 'servicos/criarServico.html', context)
        
        else:
            # Caso a validação inicial do POST falhe (campos vazios)
            context = {'error_message': 'Por favor, preencha todos os campos obrigatórios.'}
            return render(request, 'servicos/criarServico.html', context)
    
    return render(request, 'servicos/criarServico.html')

def editarServico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        servico.descricao = request.POST.get('descricao')
        tempo_str = request.POST.get('tempo')
        servico.preco = request.POST.get('preco')
        
        if servico.descricao and tempo_str and servico.preco:
            try:
                # Tratar o tempo
                parts = tempo_str.split(':')
                if len(parts) == 2:
                    hours, minutes = map(int, parts)
                    seconds = 0
                elif len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                else:
                    raise ValueError("Formato de tempo inválido.")

                servico.tempo = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                servico.save()
                return redirect('listaServicos')
            
            except Exception as e:
                error_message = f'Erro ao editar: {e}'
                tempo_formatado = format_timedelta_to_time_string(servico.tempo)
                context = {'error_message': error_message, 'servico': servico, 'tempo_formatado': tempo_formatado}
                return render(request, 'servicos/criarServico.html', context)
        else:
            context = {'error_message': 'Por favor, preencha todos os campos obrigatórios.', 'servico': servico}
            return render(request, 'servicos/criarServico.html', context)
    
    # Formata timedelta para HH:MM:SS para exibição
    tempo_formatado = format_timedelta_to_time_string(servico.tempo)

    context = {'servico': servico, 'tempo_formatado': tempo_formatado}
    return render(request, 'servicos/criarServico.html', context)

def deletarServico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    servico.delete()
    return redirect('listaServicos')