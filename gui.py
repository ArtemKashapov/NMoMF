import eel
from solver import State, Implicits, Explicits, Graphics


eel.init('web')

@eel.expose
def run():
    current = State()
    print(eel.getScheme())
    if eel.getScheme():
        scheme = Implicits(current)
    else:
        scheme = Explicits(current)

    solution, theta_array, time_array = scheme.solve()
    plotter = Graphics(solution, theta_array, time_array)
    plotter.plot_solution()
    # plotter.plot_image() # пространственно-временной рисунок



if __name__=="__main__":
    eel.start('index.html', port=8080)