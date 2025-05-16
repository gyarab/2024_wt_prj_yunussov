from django.shortcuts import render

def get_homepage(request):
    context = {
        "h1_title": "Main matches",
        "movies": [
                { "title": "Arsenal vs Manchester United" },
                { "title": "Chelsea vs Liverpool" },
                { "title": "Manchester City vs Arsenal" },
                { "title": "Barcelona vs Real Madrid (El Clásico)" },
                { "title": "Liverpool vs Manchester United" },
            ]
    }
    return render(
        request, "main/home.html", context
    )
