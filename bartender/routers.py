from rest_framework_extensions.routers import ExtendedDefaultRouter


class ExtendableRouter(ExtendedDefaultRouter):
    """
    ExtendableRouter to extend the registry from others routers
    """

    def extend(self, router):
        """
        Extend the router"s registry with another router
        :param router: router"s routes to add to this router
        """
        self.registry.extend(router.registry)
