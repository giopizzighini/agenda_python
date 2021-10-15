from django.shortcuts import render
from core.models import evento

# Create your views here.

def lista_eventos(request):
    Evento = evento.objects.all()
    dados = {'eventos': Evento}
    return render(request,'agenda.html', dados)


