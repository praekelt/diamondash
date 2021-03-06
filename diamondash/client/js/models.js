diamondash.models = function() {
  var DiamondashConfigModel = Backbone.RelationalModel.extend({
    relations: [{
      type: Backbone.HasOne,
      key: 'auth',
      relatedModel: 'diamondash.models.AuthModel',
      includeInJSON: false
    }],

    defaults: {
      auth: {}
    }
  });

  var AuthModel = Backbone.RelationalModel.extend({
    defaults: {
      all: false
    },

    stringify: function() {
      return diamondash.utils.basicAuth(
        this.get('username'),
        this.get('password'));
    }
  });

  var Model = Backbone.RelationalModel.extend({
    sync: function(method, model, options) {
      options = options || {};

      if (options.auth || diamondash.config.get('auth').get('all')) {
        options.beforeSend = function(xhr) {
          xhr.setRequestHeader(
            'Authorization',
            diamondash.config.get('auth').stringify());
        };
      }

      return Backbone.sync.call(this, method, model, options);
    }
  });

  return {
    Model: Model,
    AuthModel: AuthModel,
    DiamondashConfigModel: DiamondashConfigModel
  };
}.call(this);
