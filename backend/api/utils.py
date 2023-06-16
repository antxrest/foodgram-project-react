from django.shortcuts import HttpResponse


def shopping_cart_file(ingredients):

    shopping_list = 'Список покупок: \n'
    for ingredient in ingredients:
        shopping_list += (
            f'{ingredient["ingredient__name"]} - '
            f'{ingredient["amount_sum"]} '
            f'({ingredient["ingredient__measurement_unit"]}) \n'
        )
        response = HttpResponse(
            shopping_list, content_type='text/plain; charset=utf8'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.txt"'
    return response
