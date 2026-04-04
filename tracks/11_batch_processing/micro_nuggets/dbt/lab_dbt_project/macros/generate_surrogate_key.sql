{% macro generate_surrogate_key(field_list) %}
    {#-
    Generate a surrogate key by MD5-hashing concatenated field values.

    Usage:
        {{ generate_surrogate_key(['order_id', 'customer_id']) }}
        → Generates: md5(coalesce(cast(order_id as varchar),'') || '-' || coalesce(cast(customer_id as varchar),''))

    Why surrogate keys?
        - Natural keys (order_id) may change or have duplicates across sources
        - Hashed surrogate keys are stable, cross-system compatible
        - Enables deduplication and idempotent loads

    Note: dbt-utils provides a more robust version (generate_surrogate_key)
    that handles NULL values and cross-database dialect differences.
    This is a simplified lab version for teaching the concept.

    Arguments:
        field_list: list of column names to include in the hash (list of strings)
    -#}
    md5(
        {% for field in field_list %}
            coalesce(cast({{ field }} as varchar), '')
            {% if not loop.last %} || '-' || {% endif %}
        {% endfor %}
    )
{% endmacro %}
