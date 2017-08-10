from math import ceil


class Pagination:

    def __init__(self, page, per_page, total_count, slug):
        self.page = page
        self.slug = slug
        self.per_page = per_page
        self.total_count = total_count
        self.pages = int(ceil(self.total_count / float(self.per_page)))

    def prev(self):
        if self.page > 1:
            return self.slug + '?page=' + str(self.page - 1)

    def next(self):
        if self.page < self.pages:
            return self.slug + '?page=' + str(self.page + 1)
