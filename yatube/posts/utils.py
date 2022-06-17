from django.core.paginator import Paginator


def paging(request, post_list, posts_per_page):
    """Набор публикаций для страницы с запрошенным номером."""
    paginator = Paginator(post_list, posts_per_page)
    page_number = request.GET.get('page')

    return paginator.get_page(page_number)
