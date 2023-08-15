from django_prometheus import middleware


""" This will hold arbtrary graphql resolvers by their resolver name while also grabbing existing metrics for Django."""
class GrapheneMetrics(middleware.Metrics):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graphene_resolvers = { }  


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


# class GrapheneMetricDjangoFilterConnectionField(DjangoFilterConnectionField):

# 	__init__

# 		for field in self.fields
# 			# make new metrics for each field
# 	 			 GrapheneMetrics.get_instance().register_graphene_metric(Histogram, fieldname, "Total count of VideoSegmentNode Resolved", namespace=NAMESPACE)


# 	 def resolve_queryset(
#         cls, connection, iterable, info, args, filtering_args, filterset_class
#     ):

# 	 	result = super.resolve_queryset(con)

# 	 	for field in self.fields:
#             GrapheneMetrics.get_instance().get_graphene_metric("resolve_all_video_segments_count").observe( len(scoped_queryset) )
