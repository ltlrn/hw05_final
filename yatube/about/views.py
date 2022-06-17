from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    """Отображение страницы об авторе."""
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """Отображение страницы используемых технологий."""
    template_name = 'about/tech.html'
