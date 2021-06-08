This is test of listing.

{% for oneof in oneofs -%}
[ Oneof: {{ oneof.package }}::{{ oneof.msg_name }}::{{ oneof.fieldname }} ]
{%- for case in oneof.cases %}
{{ case.type_name }} - {{ case.value_name }}
 // Name converted: {{ case.value_name | camelize }}, {{ case.value_name | camelize_lower }}, {{ case.value_name | underscore }}, {{ case.value_name | underscore_upper }}
{% endfor %}
{% endfor %}

