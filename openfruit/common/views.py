from dal import autocomplete


class BaseAutocompleteQuerysetView(autocomplete.Select2QuerySetView):
    model_type = None

    def filter(self, qs):
        """
        This must be implemented
        :param qs:
        :return:
        """
        raise NotImplemented()

    def get_queryset(self):
        qs = self.model_type.objects.all()
        if not self.request.user.is_authenticated():
            return qs
        if self.q:
            qs = self.model_type.objects.all()
            qs = self.filter(qs)
        return qs


class NameAutocomplete(BaseAutocompleteQuerysetView):
    is_contains = False

    def filter(self, qs):
        if self.is_contains:
            qs = qs.filter(name__contains=self.q)
        else:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class GeneratedNameAutocomplete(BaseAutocompleteQuerysetView):
    is_contains = False

    def filter(self, qs):
        if self.is_contains:
            qs = qs.filter(generated_name__contains=self.q)
        else:
            qs = qs.filter(generated_name__istartswith=self.q)
        return qs



