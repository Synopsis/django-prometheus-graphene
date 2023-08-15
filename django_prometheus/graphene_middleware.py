from django_prometheus import middleware


""" This will hold arbtrary graphql resolvers by their resolver name while also grabbing existing metrics for Django."""
class GrapheneMetrics(middleware.Metrics):

    def __init__(self, *args, **kwargs):

        self.graphene_resolvers = { }  

        super.__init__()

    def register_graphene_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
    	graphene_metric = metric_cls(name, documentation, labelnames=labelnames, **kwargs)
    	self.graphene_resolvers[name] = graphene_metric


    def get_graphene_metric(self, name):
    	return self.graphene_resolvers[name]

''' Overload the metrics class our middleware uses'''
class GraphenePrometheusBeforeMiddleware(middleware.PrometheusBeforeMiddleware):
	metrics_cls = GrapheneMetrics


''' Overload the metrics class our middleware uses'''
class GraphenePrometheusAfterMiddleware(middleware.PrometheusAfterMiddleware):
	metrics_cls = GrapheneMetrics