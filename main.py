from flask import Flask, render_template, request, redirect
from game_t_i import GameTI
from config import Config
from project.forms import GameForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    GameTI(10)
    return render_template("index.html", title=' - главная')

@app.route('/new-game')
def new():
    GameTI(10)
    return redirect('/game')

@app.route('/game', methods=['get', 'post'])
@app.route('/game/<varr>/', methods=['get', 'post'])
def game_new(varr=None):
    if varr == 'new':
        GameTI(10)
        return redirect('/game')

    direction = 0
    steps = 0
    see_pirat = 0
    res = []

    game = GameTI()
    form = GameForm()

    if form.validate_on_submit():
        # cry = form.cry.data
        direction = form.direction.data
        steps = form.steps.data
        see_pirat = form.see_pirat.data

    if game.count == 3 or see_pirat == 1:
        game.karta_del_pirat()
        game.karta_ins_pirat()
        game.count = 0


    if game.it_is_pirat(game.koord_hero[0], game.koord_hero[1]):
        # Если при смене позиции пиратов их координаты совпали с координатами героя
        res = [4, 'Вам не повезло, Вас нашли пираты. Мы уверены, что в следующий раз удача будет на Вашей стороне.']
    else:
        if direction != 0 and steps != 0:
            # ИДЁМ НА СЕВЕР, ЮГ, ЗАПАД, ВОСТОК
            res = game.go_hero_go(direction, steps)


    game.count += 1
    return render_template("new-game.html", title=' - новая игра', game=game, res=res, form=form)

@app.route('/rules')
def rules():
    return render_template("rules.html", title=' - правила игры')

@app.route('/view-map')
def viewmap():
    game = GameTI()
    butn = 0

    def sravni(a, b, c):
        if a == b or a == c or b == c:
            return True
        else:
            return False

    if sravni(game.koord_klad[0], game.koord_hero[0], game.koord_pirat[0]) and \
            sravni(game.koord_klad[1], game.koord_hero[1], game.koord_pirat[1]):
        butn = 1

    return render_template("view-map.html", title=' - подглядеть карту', game=game, butn=butn)

@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
