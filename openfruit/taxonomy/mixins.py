
class UrlNameMixin:

    def url_latin_name(self):
        return self.latin_name.replace(' ', '-')

    def url_name(self):
        return self.name.replace(' ', '-')
