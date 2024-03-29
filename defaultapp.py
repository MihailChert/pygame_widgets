from app.Application import Application, Builder


builder = Builder.build_from('code/appconfig.json')
app = Application.create_from_builder(builder)
app.run()
