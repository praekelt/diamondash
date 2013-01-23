from mock import Mock, patch, call
from twisted.trial import unittest

from diamondash import utils
from diamondash.widgets.graphite import GraphiteWidgetMetric
from diamondash.widgets.graph import GraphWidget, GraphWidgetMetric
from diamondash.exceptions import ConfigError


class StubbedGraphWidget(GraphWidget):
    DEFAULTS = {'some_config_option': 'some-config-option'}


class GraphWidgetTestCase(unittest.TestCase):

    @patch.object(utils, 'set_key_defaults')
    @patch.object(utils, 'parse_interval')
    @patch.object(GraphWidgetMetric, 'from_config')
    def test_parse_config(self, mock_GraphWidgetMetric_from_config,
                          mock_parse_interval, mock_set_key_defaults):
        config = {
            'name': 'test-graph-widget',
            'graphite_url': 'fake_graphite_url',
            'metrics': [
                {'name': 'random sum', 'target':'vumi.random.count.sum'},
                {'name': 'random avg', 'target':'vumi.random.timer.avg'}],
            'time_range': '1d',
            'bucket_size': '1h',
            'metric_defaults': {
                'some_metric_config_option': 'some-metric-config-option'
            }
        }
        defaults = {'SomeWidgetType': "some widget's defaults"}

        mock_parse_interval.side_effect = [86400, 3600]
        mock_set_key_defaults.side_effect = lambda k, original, d: original

        metric1, metric2 = Mock(), Mock()
        metric1.client_config = 'metric1-fake-client-config'
        metric2.client_config = 'metric2-fake-client-config'
        mock_GraphWidgetMetric_from_config.side_effect = [metric1, metric2]

        parsed_config = StubbedGraphWidget.parse_config(config, defaults)

        mock_set_key_defaults.assert_called()

        self.assertEqual(
            mock_parse_interval.call_args_list, [call('1d'), call('1h')])

        metric1_from_config_call = call({
                'name': 'random sum',
                'target': 'vumi.random.count.sum',
                'bucket_size': 3600
            }, {'some_metric_config_option': 'some-metric-config-option'})
        metric2_from_config_call = call({
                 'name': 'random avg',
                 'target': 'vumi.random.timer.avg',
                 'bucket_size': 3600
            }, {'some_metric_config_option': 'some-metric-config-option'})
        self.assertEqual(
            mock_GraphWidgetMetric_from_config.call_args_list,
            [metric1_from_config_call, metric2_from_config_call])

        self.assertEqual(parsed_config['from_time'], 86400)
        self.assertEqual(parsed_config['bucket_size'], 3600)
        self.assertEqual(parsed_config['metrics'], [metric1, metric2])
        self.assertEqual(
            parsed_config['client_config']['metrics'],
            ['metric1-fake-client-config', 'metric2-fake-client-config'])


class StubbedGraphWidgetMetric(GraphWidgetMetric):
    DEFAULTS = {'some_config_option': 'some-config-option'}

    def __init__(self, name=None, title=None, client_config=None):
        self.name = name
        self.title = title
        self.client_config = client_config


class GraphWidgetMetricTestCase(unittest.TestCase):

    @patch.object(utils, 'slugify')
    def test_parse_config(self, mock_slugify):
        config = {
            'name': 'some metric',
            'title': 'Some Metric',
            'target': 'some.random.metric',
        }
        mock_slugify.return_value = 'some-metric'

        parsed_config = GraphWidgetMetric.parse_config(config, {})

        mock_slugify.assert_called_with('some metric')
        self.assertEqual(parsed_config['name'], 'some-metric')
        self.assertEqual(parsed_config['title'], 'Some Metric')
        self.assertEqual(parsed_config['client_config'],
                         {'name': 'some-metric', 'title': 'Some Metric'})

    def test_parse_config_for_no_name(self):
        self.assertRaises(
            ConfigError, GraphWidgetMetric.parse_config,
            {'target': 'some.random.metric'}, {})

    def test_parse_config_for_no_title(self):
        config = {
            'name': 'some metric',
            'target': 'some.random.metric',
        }
        parsed_config = GraphWidgetMetric.parse_config(config, {})
        self.assertEqual(parsed_config['title'], 'some metric')

    @patch.object(GraphiteWidgetMetric, 'process_datapoints')
    def test_process_datapoints(self, mock_super_process_datapoints):
        mock_super_process_datapoints.side_effect = lambda x: x
        metric = StubbedGraphWidgetMetric()
        self.assertEqual(
            metric.process_datapoints([[0, 1], [1, 2], [3, 5]]),
            [{'x': 1, 'y': 0}, {'x': 2, 'y': 1}, {'x': 5, 'y': 3}])