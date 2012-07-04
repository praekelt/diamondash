var DEFAULT_REQUEST_INTERVAL = 2000
var DEFAULT_GRAPH_COLOUR = '#0051cc'

var graphs = []; // rickshaw objects
var requestInterval = (config.requestInterval === undefined) ? DEFAULT_REQUEST_INTERVAL : config.requestInterval;

function constructWidgets() {
	graphElements = document.querySelectorAll('.graph'); 
    for (var i = 0; i < graphElements.length; i++) {
		widgetName = $.trim(graphElements[i].id);
		widgetConfig = config.widgets[widgetName];

		graphs[i] = {
			name: widgetName,
			data: [],
			object: undefined
		};

		metricSeries = [];
		for (var metricName in widgetConfig.metrics) {
			metric = widgetConfig.metrics[metricName]

			graphs[i].data[metricName] = [{ x:0, y:0 }];
			metricColor = (metric.color === undefined) ? DEFAULT_GRAPH_COLOUR : metric.color;
			metricSeries[metricName] = {
				data: graphs[i].data[metricName],
				color: metricColor
			}
		}
		
		graphs[i].object = new Rickshaw.Graph({
			element: graphElements[i],
			renderer: 'line',
			series: metricSeries
		});

		graphs[i].object.render();
	}
}

function constructUrl(widgetName) {
	return '/render/' + config.dashboardName + '/' + widgetName;
}

function updateWidgets() {
	$.each(graphs, function(i, graph) { 
		url = constructUrl(graph.name)
		getData(url, 
		function(metricData) {
			for (var metricName in metricData)
				graph.data[metricName] = metricData[metricName];
			graph.object.update();
			metricData = null;
		});
	});
}

// retrieve the data from Graphite
function getData(currentUrl, cbDataReceived) {
	var obtainedData = [];
	$.ajax({

		/*beforeSend: function(xhr) {
		  if (auth.length > 0) {
		  var bytes = Crypto.charenc.Binary.stringToBytes(auth);
		  var base64 = Crypto.util.bytesToBase64(bytes);
		  xhr.setRequestHeader("Authorization", "Basic " + base64);
		  }
		  },*/

		dataType: 'json',
		error: function(xhr, textStatus, errorThrown) {
			console.log("Error: " + xhr + " " + textStatus + " " + errorThrown);
		},
		url: currentUrl
	}).done(function(responseData) {
		if (responseData.length > 0)
		    cbDataReceived(responseData);
	});
}

constructWidgets();
updateWidgets();

var updateId = setInterval(updateWidgets, requestInterval);
