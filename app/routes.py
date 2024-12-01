def register_routes(app):
    from app.controllers.eligibility import eligibility_blueprint
    from app.controllers.ml import ml_blueprint
    from app.controllers.integration import integration_blueprint

    app.register_blueprint(eligibility_blueprint, url_prefix='/eligibility')
    app.register_blueprint(ml_blueprint, url_prefix='/ml')
    app.register_blueprint(integration_blueprint, url_prefix='/integration')
