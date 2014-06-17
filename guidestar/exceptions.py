class GuidestarError(Exception):

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)


class GuiestarNoResults(GuidestarError):
    pass


EXCEPTIONS_MAPPING = {
    404: GuiestarNoResults
}