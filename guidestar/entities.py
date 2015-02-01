from __future__ import division
import math


class Paginator(object):
    """ helper class to handles results pages

    """
    def __init__(self, per_page, total_records, current_page):
        self.current_page = current_page
        self.total_records = total_records
        self.per_page = per_page
        self.num_pages = int(math.ceil(self.total_records / self.per_page))

    def has_next(self):
        return self.current_page < self.num_pages

    def has_prev(self):
        return self.current_page > 1

    def next_page(self):
        return self.current_page + 1

    def prev_page(self):
        return self.current_page - 1

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.total_records == 0:
            return 0
        return (self.per_page * (self.current_page - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page.
        if self.current_page == self.num_pages:
            return self.total_records
        return self.current_page * self.per_page


class Items(list):
    pass


class Item(object):

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        return pickle

    def __getattr__(self, name):
        # invoken when refering to attribute that it is not valid or it was not present at json response
        return None

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into a model instance."""
        instance = cls()
        for k, v in json.items():
            if hasattr(cls, 'exclude') and k in cls.exclude:
                pass
            elif hasattr(cls, 'parsers') and k in cls.parsers:
                func = cls.parsers[k]
                setattr(instance, k, func(v))
            else:
                setattr(instance, k, v)
        return instance

    @classmethod
    def parse_list(cls, json):
        items = Items()
        if type(json) is list:
            objects = json
        else:
            objects = json.get('hits', [])

        for obj in objects:
            items.append(cls.parse(obj))
        return items


class NteeCode(Item):
    parsers = {
        'ntee_code_details': lambda v: v.get('nteecodedescription')
    }


class GeographicArea(Item):
    exclude = ('organization_id', )


class PersonType(Item):
    exclude = ('last_modified', )


class Person(Item):
    parsers = {
        'person_types': PersonType.parse_list
    }
    exclude = ('organizationid', )


class Program(Item):
    exclude = ('organizationid', )


class Organization(Item):
    parsers = {
        'geographic_areas_served': GeographicArea.parse_list,
        'organization_ntee_codes': NteeCode.parse_list,
        'people': Person.parse_list,
        'programs': Program.parse_list

    }

    @classmethod
    def parse_list(cls, json, per_page, num_page):
        items = super(Organization, cls).parse_list(json)
        items.paginator = Paginator(per_page, json.get('total_hits'), num_page)
        return items
