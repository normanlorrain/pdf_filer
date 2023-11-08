import src
import dst
import layout

try:
    src.init()
    dst.init()
    layout.start()
except Exception as e:
    print(e)
    input("Press enter")
