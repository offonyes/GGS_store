from admin_auto_filters.filters import AutocompleteFilter


class OrderFilter(AutocompleteFilter):
    title = 'Order Filter'
    field_name = 'order'


class CartFilter(AutocompleteFilter):
    title = 'Cart Filter'
    field_name = 'cart'
