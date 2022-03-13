import eel
from solver import State, Implicits, Explicits, GFTool


eel.init('web')
scheme_flag = False

@eel.expose
def run(params):
    I = int(params['I'])
    K = int(params['K'])
    l = float(params['l'])
    T = float(params['T'])
    c = float(params['c'])
    k = float(params['k'])
    R = float(params['R'])
    alpha = float(params['alpha'])
    current = State(c=c, k=k, R=R, l=l, alpha=alpha, T=T, I=I, K=K)
    if int(eel.getScheme()()):
        scheme = Implicits(current)
    else:
        scheme = Explicits(current)

    solution, theta_array, time_array = scheme.solve()
    plotter = GFTool(solution, theta_array, time_array)
    plotter.plot_solution()
    plotter.plot_image() # пространственно-временной рисунок
    plotter.plot_evol()

if __name__=="__main__":
    eel.start('index.html', port=8080)