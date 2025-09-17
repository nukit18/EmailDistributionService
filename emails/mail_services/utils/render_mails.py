from django.template import Template, Context

def render_html_template(template_str: str, context_dict: dict) -> str:
    """
    Заполняет HTML-шаблон переменными.

    :param template_str: строка с HTML шаблоном, например "<h1>Hello, {{ name }}</h1>"
    :param context_dict: словарь переменных, например {"name": "Nikita"}
    :return: HTML-строка с подставленными значениями
    """
    template = Template(template_str)
    context = Context(context_dict)
    return template.render(context)
