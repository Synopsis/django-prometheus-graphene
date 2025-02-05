from django_prometheus import middleware
from django_prometheus.conf import NAMESPACE
from graphene_django.filter import DjangoFilterConnectionField
from prometheus_client import Counter, Histogram

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

class GrapheneMetricDjangoFilterConnectionField(DjangoFilterConnectionField):

	@classmethod
	def metric_name(cls, filterset_class, metric_suffix):
		print("filterset_class", filterset_class)

		metric_name = filterset_class.__name__.split(".")[-1]  + metric_suffix

		print("Metric Name:", metric_name)

		return metric_name


	def __init__(
			self,
			type_,
			fields=None,
			order_by=None,
			extra_filter_meta=None,
			filterset_class=None,
			*args,
			**kwargs
		):
		 
		super().__init__(
			type_, 
			fields=fields,
			order_by=order_by,
			extra_filter_meta=extra_filter_meta,
			filterset_class=filterset_class, 
			*args,
			**kwargs)

		metric_name = GrapheneMetricDjangoFilterConnectionField.metric_name( self.filterset_class, "_histogram")

		GrapheneMetrics.get_instance().register_graphene_metric(Histogram, metric_name, f"Total count of { metric_name } Resolved", namespace=NAMESPACE)

	def get_queryset_resolver(self):
		metric_name = GrapheneMetricDjangoFilterConnectionField.metric_name(self.filterset_class, "_histogram")

		result = super().get_queryset_resolver()
		
		GrapheneMetrics.get_instance().get_graphene_metric( metric_name ).observe( len(result) )
		print("length of result:", len(result) )

		return result

	# @classmethod
	# def resolve_queryset(cls, connection, iterable, info, args, filtering_args, filterset_class):

	# 	metric_name = GrapheneMetricDjangoFilterConnectionField.metric_name(filterset_class, "_histogram")

	# 	result = super().resolve_queryset(connection, iterable, info, args, filtering_args, filterset_class)
	# 	print(filterset_class)


	# 	GrapheneMetrics.get_instance().get_graphene_metric( metric_name ).observe( len(result) )

	# 	return result
