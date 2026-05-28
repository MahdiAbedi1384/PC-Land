from django import template
import os
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

register = template.Library()

@register.filter
def concat(*args):
    return "".join(args)

@register.filter(name="kg_to_g")
def kilogram_to_gram(kilogram):
    return kilogram * 1000

@register.filter(name="ntpw")
def number_to_persian_word(number):
    numbers_in_persian_word = {
        0:"صفر",
        1:"یک",
        2:"دو",
        3:"سه",
        4:"چهار",
        5:"پنج",
        6:"شش",
        7:"هفت",
        8:"هشت",
        9:"نه",
    }
    return numbers_in_persian_word.get(number, "نامعلوم")

@register.simple_tag
def get_specs_template(product):
    product: object
    model = product.__class__.__name__.lower()

    # تلاش برای لود template مخصوص مدل
    try:
        return f"product-specs/{model}.html"
    except TemplateDoesNotExist:
        # fallback مطمئن: اگر نبود، default.html
        return "product-specs/default.html"
