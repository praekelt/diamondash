diamondash.DashboardController = (function() {
    function DashboardController(args) {
      this.name = args.name;
      this.widgets = args.widgets;
      this.widgetViews = args.widgetViews;
      this.requestInterval = args.requestInterval;
    }

    DashboardController.DEFAULT_REQUEST_INTERVAL = 10000;

    DashboardController.fromConfig = function(config) {
      var diamondashWidgets = diamondash.widgets,
          dashboardName,
          requestInterval,
          widgets,
          widgetViews;

      dashboardName = config.name;

      requestInterval = (config.requestInterval ||
                         DashboardController.DEFAULT_REQUEST_INTERVAL);

      widgets = new diamondashWidgets.WidgetCollection();
      widgetViews = [];

      config.widgets.forEach(function(widgetConfig) {
        var Model, View, name, model, view, widgetModelConfig;

        Model = diamondashWidgets[widgetConfig.modelClass];
        widgetModelConfig = widgetConfig.model;
        widgetModelConfig.dashboardName = dashboardName;
        model = new Model(widgetModelConfig);

        View = diamondashWidgets[widgetConfig.viewClass];
        view = new View({el: $("#" + model.get('name')), model: model});

        widgetViews.push(view);
        widgets.add(model);
      });

      return new DashboardController({
        name: dashboardName,
        widgets: widgets, 
        widgetViews: widgetViews,
        requestInterval: requestInterval
      });
    };

    DashboardController.prototype = {
      start: function() {
        var self = this;
        var fetch = function(model) { return model.fetch(); };
        setInterval(function() { self.widgets.forEach(fetch); },
                    this.requestInterval);
      }
    };

    return DashboardController;
})();