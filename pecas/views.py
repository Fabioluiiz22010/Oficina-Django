from django.shortcuts import render, redirect, get_object_or_404
from .models import Peca

def listaPecas(request):
    pecas = Peca.objects.all()
    context = {'pecas': pecas}
    return render(request, 'pecas/listaPecas.html', context)

def criarPeca(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade')
        valorUN = request.POST.get('valorUN')

        try:
            Peca.objects.create(
                nome=nome, 
                quantidade=quantidade, 
                valorUN=valorUN
            )
            return redirect('listaPecas')
        except:
            pass

    return render(request, 'pecas/criarPeca.html', {})

def editarPeca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)

    if request.method == 'POST':
        peca.nome = request.POST.get('nome')
        peca.quantidade = request.POST.get('quantidade')
        peca.valorUN = request.POST.get('valorUN')
        
        peca.save()
        return redirect('listaPecas')
    
    context = {
        'peca': peca
    }
    return render(request, 'pecas/criarPeca.html', context)

def deletarPeca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    peca.delete()
    return redirect('listaPecas')