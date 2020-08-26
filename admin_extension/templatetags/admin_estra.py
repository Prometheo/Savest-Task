from django import template
from django.contrib.auth.models import User
from datetime import date

register = template.Library()

@register.simple_tag
def get_stamp():
    em_list = list()
    tem_dict = {'this_month':0, 'this_week':0, 'this_day':0}
    all_users = User.objects.all()
    for us in all_users:
        em_list.append(us.date_joined.date())
    pres = date.today()
    for var in em_list:
        days_count = pres - var
        if days_count.days <= 1:
            tem_dict['this_day'] += 1
            tem_dict['this_week'] += 1
            tem_dict['this_month'] += 1
        elif days_count.days <= 7:
            tem_dict['this_week'] += 1
            tem_dict['this_month'] += 1
        elif days_count.days <= 31:
            tem_dict['this_month'] += 1
    return tem_dict

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)