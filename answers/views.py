import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from create_form.models import Form, Questions
from results.models import Responses
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


# # Create your views here.        
# def response(request, code, response_code):
#     formInfo = Form.objects.filter(code = code)
#     #Checking if form exists
#     if formInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: formInfo = formInfo[0]
#     #Checking if form creator is user
#     if not formInfo.allow_view_score:
#         if formInfo.creator != request.user:
#             return HttpResponseRedirect(reverse("403"))
    
#     responseInfo = Responses.objects.filter(response_code = response_code)
#     if responseInfo.count() == 0:
#         return HttpResponseRedirect(reverse('404'))
#     else: responseInfo = responseInfo[0]
#     return render(request, "sub/response.html", {
#         "form": formInfo,
#         "response": responseInfo,
#     })


def response(request, code, response_code):
    # Retrieve the form or return 404 if not found
    form_info = get_object_or_404(Form, code=code)
    
    # Check if the user is allowed to view the score
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))

    # Retrieve the response or return 404 if not found
    response_info = get_object_or_404(Responses, response_code=response_code)

    # Render the response page with the retrieved data
    return render(request, "sub/response.html", {
        "form": form_info,
        "response": response_info,
    })
