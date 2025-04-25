from django.shortcuts import render

def get_homepage(request):
    context = {
        "svatek": "Libor",
        "title": "Pulp Fiction",
        "movies": [
                {
                 "title": "Django unchained"
                },
                {
                 "title": "Teletubies"
                }
            ]
    }
    return render(
        request, "main/home.html", context
    )
