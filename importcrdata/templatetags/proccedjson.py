from django import template
from django.utils.safestring import SafeText

register = template.Library()

@register.simple_tag(takes_context=True)
def callJs(context):
    """Removes all values of arg from the given string"""
    print(context)
    action = '''<script>
        $(document).ready(function () {
            $.getJSON('/es/generatejson/1090', function (data) {

                for (let e of data) {
                    $('#display').append('<p>' + e.codele + ' ' + e.cedula + ' ' + e.nombre_completo + '</p>')
                }
            })
        });
    </script>'''
    return SafeText(action)