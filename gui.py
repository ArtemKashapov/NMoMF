from statistics import mode
import eel


eel.init('web')

if __name__=="__main__":
    eel.start('index.html', port=8080)