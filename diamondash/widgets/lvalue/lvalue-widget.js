(function() {
  var widgets = diamondash.widgets;

  widgets.LValueWidgetModel = widgets.WidgetModel.extend({
    isStatic: false
  });

  var ValueView = Backbone.View.extend({
    fadeDuration: 200,

    initialize: function(options) {
      this.widget = options.widget;
    },

    format: {
      short: d3.format(".2s"),
      long: d3.format(",f")
    },

    blink: function(fn) {
      this.$el.fadeOut(this.fadeDuration, function() {
        fn.call(this);
        this.$el.fadeIn(this.fadeDuration);
      }.bind(this));
    },

    render: function(longMode) {
      this.blink(function() {
        if (longMode) {
          this.$el
            .addClass('long')
            .removeClass('short')
            .text(this.format.long(this.model.get('lvalue')));
        } else {
          this.$el
            .addClass('short')
            .removeClass('long')
            .text(this.format.short(this.model.get('lvalue')));
        }
      });
    }
  });

  widgets.LValueWidgetView = widgets.WidgetView.extend({
    jst: _.template([
      '<h1 class="value"></h1>',
      '<div class="<%= change %> change">',
        '<div class="diff"><%= diff %></div>',
        '<div class="percentage"><%= percentage %></div>',
      '</div>',
      '<div class="time">',
        '<div class="from">from <%= from %></div>',
        '<div class="to">to <%= to %><div>',
      '</div>'
    ].join('')),
   
    initialize: function(options) {
      this.listenTo(this.model, 'change', this.render);

      this.value = new ValueView({
        widget: this,
        model: this.model
      });
    },

    format: {
      diff: d3.format("+.3s"),
      percentage: d3.format(".2%"),

      _time: d3.time.format.utc("%d-%m-%Y %H:%M"),
      time: function(t) { return this._time(new Date(t)); },
    },

    render: function() {
      var model = this.model;

      var diff = model.get('diff');
      var change;
      if (diff > 0) { change = 'good'; }
      else if (diff < 0) { change = 'bad'; }
      else { change = 'no'; }

      this.$('.widget-container').html(this.jst({
        from: this.format.time(model.get('from')),
        to: this.format.time(model.get('to')),
        diff: this.format.diff(diff),
        percentage: this.format.percentage(model.get('percentage')),
        change: change,
      }));

      this.value
        .setElement(this.$('.value'))
        .render(this.$el.is(':hover'));
    },

    events: {
      'mouseenter': function() {
        var self = this;
        this.value.render(true);
      },

      'mouseleave': function() {
        this.value.render(false);
      }
    }
  });
}).call(this);
