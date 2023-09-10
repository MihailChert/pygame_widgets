from app.Application import Application, Builder
from app.Drawing import DrawingFactory

factories = {'drawing': DrawingFactory}
builder = Builder.build_from('code/appconfig.json')
app = Application.create_from_builder(builder)
app.run()
