from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, RadioField, SubmitField, widgets
from wtforms.validators import NumberRange, DataRequired

class GameForm(FlaskForm):
    # cry = StringField('Боевой клич: ', validators=[DataRequired()])
    direction = SelectField('Выберите направление движения: ', coerce=int,
                            choices=[(1, 'Север'), (2, 'Юг'), (3, 'Запад'), (4, 'Восток')],
                            render_kw={'class': 'game-form_p'})
    steps = IntegerField('Количество шагов: ', validators=[NumberRange(min=1, max=5), DataRequired()], default=1,
                            render_kw={'class': 'game-form_p'})
    see_pirat = RadioField('Показать предыдущее положение пиратов: ', coerce=int,
                           choices=[(0, 'Нет (координаты пиратов будут меняться через три хода)'),
                                    (1, 'Да (координаты пиратов будут меняться каждый ход)')],
                           default=0, render_kw={'class': 'game-form_li game-form_p'})
    submit = SubmitField('Вперед')

#, widget=widgets.TableWidget(with_table_tag=True)
