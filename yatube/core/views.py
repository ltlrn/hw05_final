from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    """Отображение отсутствующей страницы."""

    return render(
        request,
        'core/404.html',
        {'path': request.path},
        status=HTTPStatus.NOT_FOUND,
    )


def server_error(request):
    """Отображение ошибки сервера."""
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    return render(request, 'core/403.html', status=403)


def csrf_failure(request, reason=''):
    """Отображение ошибки проверки csrf."""

    return render(request, 'core/403csrf.html')
