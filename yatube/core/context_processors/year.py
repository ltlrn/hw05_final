from datetime import datetime


def year(request):
    """Процессор контекста для вывода актуального года."""
    return {
        'year': datetime.today().year
    }
