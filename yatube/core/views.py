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
    return render(
        request,
        'core/500.html',
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def permission_denied(request, exception):
    """Отображение ошибки доступа."""
    return render(
        request,
        'core/403.html',
        status=HTTPStatus.FORBIDDEN
    )


def csrf_failure(request, reason=''):
    """Отображение ошибки проверки csrf."""

    return render(request, 'core/403csrf.html')
