from django.shortcuts import render


def main(request):
    return render(request, 'main.html')


def contact(request):
    return render(request, 'contact.html')
