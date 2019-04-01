from django.http import JsonResponse


class AjaxResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            data = {
                'status': 'error',
                'response': form.error
            }
            return JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'status': 'success',
            }
            return JsonResponse(data)
        return response
