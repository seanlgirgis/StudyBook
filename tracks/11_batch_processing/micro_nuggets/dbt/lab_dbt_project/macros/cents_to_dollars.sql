{% macro cents_to_dollars(column_name, decimal_places=2) %}
    {#-
    Convert integer cents to decimal dollars.

    Usage in any model:
        {{ cents_to_dollars('amount_cents') }}
        → Generates: round(amount_cents / 100.0, 2)

        {{ cents_to_dollars('price_cents', 4) }}
        → Generates: round(price_cents / 100.0, 4)

    Why a macro vs inline SQL?
        - Single source of truth: change the formula in ONE place
        - Cross-database compatible: can be adapted per dialect
        - Readable: cents_to_dollars('col') vs round(col / 100.0, 2)

    Arguments:
        column_name:    SQL expression or column name (string)
        decimal_places: number of decimal places to round to (default: 2)
    -#}
    round({{ column_name }} / 100.0, {{ decimal_places }})
{% endmacro %}
