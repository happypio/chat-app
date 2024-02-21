from django.shortcuts import redirect, render


def chat(request):
    if request.user.is_authenticated:
        return render(request, "chats/index.html")
    else:
        return redirect("custom_auth:login")
