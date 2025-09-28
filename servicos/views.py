from django.shortcuts import render, redirect, get_object_or_404
from .models import Servico
from datetime import timedelta # Necessário para DurationField

def listaServicos(request):
    servicos = Servico.objects.all()
    context = {'servicos': servicos}
    return render(request, 'servicos/lista.html', context)

def criarServico(request):
    if request.method == 'POST':
        print("Requisição POST recebida para criarServico.")
        
        # Novos nomes dos campos
        descricao = request.POST.get('descricao')
        tempo_str = request.POST.get('tempo') # Virá como string, ex: "01:30:00"
        preco = request.POST.get('preco')
        
        print(f"Dados do formulário: Descricao={descricao}, Tempo={tempo_str}, Preco={preco}")

        if descricao and tempo_str and preco:
            print("Todos os campos obrigatórios preenchidos. Tentando criar Serviço...")
            try:
                # Converter tempo_str para timedelta
                # Assumindo formato HH:MM:SS ou similar para DurationField
                # Pode precisar de tratamento de erro mais robusto aqui
                hours, minutes, seconds = map(int, tempo_str.split(':'))
                tempo_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

                Servico.objects.create(
                    descricao=descricao,
                    tempo=tempo_delta,
                    preco=preco
                )
                print("Serviço criado com sucesso!")
                return redirect('listaServicos')
            except ValueError:
                error_message = 'Formato de tempo inválido. Use HH:MM:SS.'
                print(f"!!!! ERRO EXCEPCIONAL ao criar serviço: {error_message}")
                context = {'error_message': error_message, 'servico': {'descricao': descricao, 'tempo': tempo_str, 'preco': preco}}
                return render(request, 'servicos/criarServico.html', context)
            except Exception as e:
                print(f"!!!! ERRO EXCEPCIONAL ao criar serviço: {e}")
                context = {'error_message': f'Erro ao cadastrar serviço: {e}. Verifique os dados.'}
                return render(request, 'servicos/criarServico.html', context)
        else:
            print("AVISO: Campos obrigatórios faltando. Renderizando formulário novamente.")
            context = {'error_message': 'Por favor, preencha todos os campos obrigatórios.'}
            return render(request, 'servicos/criarServico.html', context)
    
    print("Renderizando formulário de criação de Serviço (GET ou POST falhou na validação inicial).")
    return render(request, 'servicos/criarServico.html')

def editarServico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        servico.descricao = request.POST.get('descricao')
        tempo_str = request.POST.get('tempo')
        servico.preco = request.POST.get('preco')
        
        if servico.descricao and tempo_str and servico.preco:
            try:
                hours, minutes, seconds = map(int, tempo_str.split(':'))
                servico.tempo = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                servico.save()
                print(f"Serviço PK={pk} editado com sucesso!")
                return redirect('listaServicos')
            except ValueError:
                error_message = 'Formato de tempo inválido. Use HH:MM:SS.'
                context = {'error_message': error_message, 'servico': servico}
                return render(request, 'servicos/criarServico.html', context)
            except Exception as e:
                print(f"!!!! ERRO EXCEPCIONAL ao editar serviço: {e}")
                context = {'error_message': f'Erro ao editar serviço: {e}. Verifique os dados.', 'servico': servico}
                return render(request, 'servicos/criarServico.html', context)
        else:
            context = {'error_message': 'Por favor, preencha todos os campos obrigatórios.', 'servico': servico}
            return render(request, 'servicos/criarServico.html', context)
    
    # Formata timedelta para HH:MM:SS para exibição no input type="time"
    tempo_formatado = None
    if servico.tempo:
        total_seconds = int(servico.tempo.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        tempo_formatado = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    context = {'servico': servico, 'tempo_formatado': tempo_formatado}
    return render(request, 'servicos/criarServico.html', context)

def deletarServico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    servico.delete()
    return redirect('listaServicos')