from admin_auto_filters.filters import AutocompleteFilter


class CategoryFilter(AutocompleteFilter):
    title = 'Category Filter'
    field_name = 'category'


class ShoeFilter(AutocompleteFilter):
    title = 'Shoe Filter'
    field_name = 'shoe'


class SizeFilter(AutocompleteFilter):
    title = 'Size Filter'
    field_name = 'size'


class UserFilter(AutocompleteFilter):
    title = 'User Filter'
    field_name = 'user'
