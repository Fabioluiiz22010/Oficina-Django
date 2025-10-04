from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import OrdemServico, PecaUsada
from veiculos.models import Veiculo
from servicos.models import Servico
from pecas.models import Peca

def listaOrdens(request):
    ordem_servicos = OrdemServico.objects.all()
    context = {'ordens': ordem_servicos}
    return render(request, 'ordemServicos/listaOrdens.html', context)

def criarOrdem(request):
    veiculos = Veiculo.objects.all()
    servicos_disponiveis = Servico.objects.all()
    pecas_disponiveis = Peca.objects.all()
    context = {
        'veiculos': veiculos,
        'servicos_disponiveis': servicos_disponiveis,
        'pecas_disponiveis': pecas_disponiveis
    }
    
    if request.method == 'POST':
        veiculo_pk = request.POST.get('veiculo')
        servico_id = request.POST.get('servico_principal')
        kilometragem = request.POST.get('Kilometragem')
        dataSaida = request.POST.get('dataSaida')
        feito = request.POST.get('feito') == 'on'
        valorTotal = request.POST.get('valorTotal')

        pecaIds = request.POST.getlist('pecaId')
        quantidades = request.POST.getlist('quantidadeUsada')

        if veiculo_pk and servico_id and kilometragem:
            try:
                with transaction.atomic():
                    veiculo = get_object_or_404(Veiculo, pk=veiculo_pk)
                    servico = get_object_or_404(Servico, pk=servico_id)
                    
                    ordem_servico = OrdemServico.objects.create(
                        veiculo=veiculo,
                        servico=servico,
                        Kilometragem=kilometragem,
                        dataSaida=dataSaida if dataSaida else None,
                        feito=feito,
                        valorTotal=valorTotal if valorTotal else 0.00
                    )

                    for pecaId, quantidade in zip(pecaIds, quantidades):
                        if pecaId and quantidade and int(quantidade) > 0:
                            peca = Peca.objects.get(pk=pecaId)
                            quantidadeInt = int(quantidade)
                            
                            PecaUsada.objects.create(
                                ordemServico=ordem_servico,
                                peca=peca,
                                quantidadeUsada=quantidadeInt
                            )

                return redirect('listaOrdens')
                
            except ValidationError as e:
                context['error_message'] = f'Erro de Estoque: {e.message}'
                return render(request, 'ordemServicos/criarOrdem.html', context)
                
            except Exception as e:
                context['error_message'] = f'Erro ao cadastrar Ordem de Serviço: {e}. Verifique os dados.'
                return render(request, 'ordemServicos/criarOrdem.html', context)
        else:
            context['error_message'] = 'Por favor, preencha todos os campos obrigatórios.'
            return render(request, 'ordemServicos/criarOrdem.html', context)
    
    return render(request, 'ordemServicos/criarOrdem.html', context)

def editarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    veiculos = Veiculo.objects.all()
    servicos_disponiveis = Servico.objects.all()
    pecas_disponiveis = Peca.objects.all()

    pecas_selecionadas_pk = [p.pk for p in ordem.pecas.all()]
    context = {
        'ordem': ordem,
        'veiculos': veiculos,
        'servicos_disponiveis': servicos_disponiveis,
        'pecas_disponiveis': pecas_disponiveis,
        'pecas_selecionadas_pk': pecas_selecionadas_pk
    }

    if request.method == 'POST':
        try:
            with transaction.atomic():
                ordem.veiculo = get_object_or_404(Veiculo, pk=request.POST.get('veiculo'))
                ordem.servico = get_object_or_404(Servico, pk=request.POST.get('servico_principal'))
                ordem.Kilometragem = request.POST.get('Kilometragem')
                ordem.dataSaida = request.POST.get('dataSaida') if request.POST.get('dataSaida') else None
                ordem.feito = request.POST.get('feito') == 'on'
                ordem.valorTotal = request.POST.get('valorTotal') if request.POST.get('valorTotal') else 0.00
                ordem.save()
                
                pecaIds = request.POST.getlist('pecaId')
                quantidades = request.POST.getlist('quantidadeUsada')

                ordem.pecaUsada_set.all().delete()
                
                for pecaId, quantidade in zip(pecaIds, quantidades):
                    if pecaId and quantidade and int(quantidade) > 0:
                        peca = Peca.objects.get(pk=pecaId)
                        quantidadeInt = int(quantidade)
                        
                        PecaUsada.objects.create(
                            ordemServico=ordem,
                            peca=peca,
                            quantidadeUsada=quantidadeInt
                        )

            return redirect('listaOrdens')
            
        except ValidationError as e:
            context['error_message'] = f'Erro de Estoque: {e.message}'
            return render(request, 'ordemServicos/criarOrdem.html', context)
        
        except Exception as e:
            context['error_message'] = f'Erro inesperado: {e}'
            return render(request, 'ordemServicos/criarOrdem.html', context)


    return render(request, 'ordemServicos/criarOrdem.html', context)

def deletarOrdem(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)
    ordem.delete()
    return redirect('listaOrdens')