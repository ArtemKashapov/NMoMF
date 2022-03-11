import eel
from solver import State, Implicits, Explicits, GFTool


eel.init('web')
scheme_flag = False

@eel.expose
def run():
    current = State()
    if int(eel.getScheme()()):
        scheme = Implicits(current)
    else:
        scheme = Explicits(current)

    solution, theta_array, time_array = scheme.solve()
    plotter = GFTool(solution, theta_array, time_array)
    plotter.plot_solution()
    plotter.plot_image() # пространственно-временной рисунок


if __name__=="__main__":
    eel.start('index.html', port=8080)