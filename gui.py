import eel
from solver import State, Implicits, Graphics


eel.init('web')

@eel.expose
def run():
    current = State()
    solution, theta_array, time_array = Implicits(current).solve()
    plotter = Graphics(solution, theta_array, time_array)
    plotter.plot_solution()



if __name__=="__main__":
    eel.start('index.html', port=8080)