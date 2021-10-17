from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.

def login_user(request):
    return render(request,'login.html')

def logout_user(request):
    logout (request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou Senha invalido")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    Evento = evento.objects.filter(usuario=usuario,data_evento__gt=data_atual)
    dados = {'eventos': Evento}
    return render(request,'agenda.html', dados)

@login_required(login_url='/login/')
def appointment(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = evento.objects.get(id=id_evento)
    return render(request, "appointment.html", dados)

@login_required(login_url='/login/')
def submit_appointment(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento: object = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento.objects.filter(id=id_evento).update(titulo=titulo, data_evento=data_evento,descricao=descricao)
        else:
            evento.objects.create(titulo=titulo, data_evento=data_evento,descricao=descricao,usuario=usuario)
    return redirect('/')

@login_required(login_url='/login/')
def delete_appointment(request,id_evento):
    usuario = request.user
    try:
        Evento = evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == Evento.usuario:
        Evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    Evento = evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(Evento), safe=False)





