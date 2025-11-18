from django.shortcuts import render

def home_view(request):
    return render(request, 'home/index.html')

# def about_view(request):
#     return render(request, 'home/about.html')


# def contact_view(request):
#     return render(request, 'home/contact.html')

# def investment_view(request):
#     return render(request, 'home/investment.html')
