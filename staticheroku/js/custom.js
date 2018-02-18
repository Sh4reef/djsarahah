


(function(global, $){
  var Greetr = function(firstName, lastName, language){
    return new Greetr.sn.init(firstName, lastName, language);
  }

  var supportedLangs = ['en', 'es'];

  var greetings = {
    en: 'Hello',
    es: 'Hola'
  }

  var formalGreetings = {
    en: 'Greeting',
    es: 'Saludos',
  }

  Greetr.sn = Greetr.prototype = {
    fullName: function(){
      return this.firstName + ' ' + this.lastName;
    },
    validate: function(){
      if(supportedLangs.indexOf(this.language) === -1){
        throw 'This language is not yet supported.';
      }
    },
    greeting: function(){
      return greetings[this.language] + ' ' + this.firstName;
    },
    formalGreeting: function(){
      return formalGreetings[this.language] + ', ' + this.firstName;
    },
    greet: function(formal){
      var msg;
      if(formal){
        msg = this.formalGreeting();
      }
      else{
        msg = this.greeting();
      }
      if(console){
        console.log(msg);
      }
      return this;
    },
    setLang: function(language){
      this.language = language;
      this.validate();
      return this;
    },
    htmlGreeting: function(selector, formal){
      if(!$){
        throw 'jQuery is not loaded.';
      }
      if(!selector){
        throw 'Missing jQuery selecotr.';
      }
      if(formal){
        msg = this.formalGreeting();
      }
      else{
        msg = this.greeting();
      }
      if(console){
        console.log(msg);
      }

      $(selector).html(msg);

      return this;
    }
  };

  init = Greetr.sn.init = function(firstName, lastName, language){
      var self = this;
      self.firstName = firstName || 'SetFirstNameHere';
      self.lastName = lastName || 'SetLastNameHere';
      self.language = language || 'en';
      self.validate();
  }

  init.prototype = Greetr.sn;

  global.Greetr = global.G$ = Greetr;

})(window, jQuery);
