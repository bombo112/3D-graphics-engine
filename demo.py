import Engine as fx


teapotmodel = "teapot.obj"

teapot_id = fx.load_model(teapotmodel)

while True:
    fx.update()