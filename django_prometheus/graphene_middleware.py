from . import Metrics, PrometheusBeforeMiddleware, PrometheusAfterMiddleware


""" This will hold arbtrary graphql resolvers by their resolver name while also grabbing existing metrics for Django."""
class GrapheneMetrics(Metrics):

    def __init__(self, *args, **kwargs):

        self.graphene_resolvers = { }  

        super.__init__()

    def register_graphene_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
    	graphene_metric = metric_cls(name, documentation, labelnames=labelnames, **kwargs)
    	self.graphene_resolvers[name] = graphene_metric


    def get_graphene_metric(self, name):
    	return self.graphene_resolvers[name]

''' Overload the metrics class our middleware uses'''
class GraphenePrometheusBeforeMiddleware(PrometheusBeforeMiddleware):
	metrics_cls = GrapheneMetrics


''' Overload the metrics class our middleware uses'''
class GraphenePrometheusAfterMiddleware(PrometheusAfterMiddleware):
	metrics_cls = GrapheneMetrics