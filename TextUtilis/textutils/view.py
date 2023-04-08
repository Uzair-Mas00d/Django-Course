from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request,'index.html')

def analyze(request):
    djtext = request.POST.get('text','default')
    removepunc = request.POST.get('removepunc','off')
    fullcap =  request.POST.get('fullcap','off')
    newlineremover = request.POST.get('newlineremover','off')
    extraspaceremover = request.POST.get('spaceremover','off')
    charcount = request.POST.get('charcount','off')

    if removepunc == "on":
        punList = '''.,:;!?()[]-<>'"{}\/@#$%^&*~_'''
        analyzed = ""
        for char in djtext:
            if char not in punList:
                analyzed = analyzed + char
        params = {"purpose":"Removed punctuation","analyzed_text":analyzed}
        djtext = analyzed
        #return render(request,"analyze.html",params)
    
    if fullcap == "on":
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()
        params = {"purpose":"Changed to UpperCase","analyzed_text":analyzed}
        djtext = analyzed
        #return render(request,"analyze.html",params)
    
    if newlineremover == "on":
        analyzed = ""
        for char in djtext:
            if char != "\n" and char != "\r":
                analyzed = analyzed + char
        params = {"purpose":"Newline Remover","analyzed_text":analyzed}
        djtext = analyzed
        #return render(request,"analyze.html",params)
    
    if extraspaceremover == "on":
        analyzed = ""
        for index,char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1] == " "):
                analyzed = analyzed + char                
        params = {"purpose":"Extra Space Remover","analyzed_text":analyzed}
        djtext = analyzed
        #return render(request,"analyze.html",params)
    
    if charcount == "on":
        punList = '''.,:;!?()[]-<>'"{}\/@#$%^&*~_\n\r" "'''
        analyzed = 0
        for char in djtext:
            if char not in punList:
                analyzed += 1
        params = {"purpose":"Char Counter","analyzed_text":f"Number of char in text {analyzed}"}
        #return render(request,"analyze.html",params)

    if removepunc != "on" and fullcap != "on" and newlineremover != "on" and extraspaceremover != "on" and charcount != "on":
        return HttpResponse("Error")

    return render(request,"analyze.html",params)
