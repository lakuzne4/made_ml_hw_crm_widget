import pandas as pd
import numpy as np
import pickle
from IPython.display import clear_output, display, HTML
import ipywidgets as widgets
from zipfile import ZipFile

STEP_NUMBER = 100

# client_base_to_show = pd.read_csv("scored_client_base.csv", encoding='cp1251', decimal=',', sep=';')

client_base_1 =pd.read_csv ("scored_client_base_part1.zip", encoding='cp1251', decimal=',', sep=';')
client_base_2 =pd.read_csv ("scored_client_base_part2.zip", encoding='cp1251', decimal=',', sep=';')
client_base_to_show = pd.concat([client_base_1, client_base_2], axis=0, ignore_index=True)


# список скоров моделей для продукта и канала
model_collecton = {('Плюшевые мишки', 'Голубиная почта'): 0,
                     ('Бентли', 'Голубиная почта'): 0,
                     ('Бентли', 'ОМОН'): 0,
                     ('Памперсы', 'ОМОН'): 0,
                     ('Плюшевые мишки', 'ОМОН'): 0,
                     ('Ёлочные игрушки', 'ОМОН'): 0,
                     ('Бентли', 'Санта-Клаус'): 0,
                     ('Памперсы', 'Голубиная почта'): 0,
                     ('Ёлочные игрушки', 'Голубиная почта'): 0,
                     ('Алкоголь', 'Голубиная почта'): 0,
                     ('Алкоголь', 'Санта-Клаус'): 0,
                     ('Алкоголь', 'ОМОН'): 0,
                     ('Алкоголь', 'Сигнальные костры'): 0,
                     ('Памперсы', 'Санта-Клаус'): 0,
                     ('Ёлочные игрушки', 'Санта-Клаус'): 0,
                     ('Ёлочные игрушки', 'Сигнальные костры'): 0,
                     ('Плюшевые мишки', 'Санта-Клаус'): 0,
                     ('Памперсы', 'Сигнальные костры'): 0,
                     ('Плюшевые мишки', 'Сигнальные костры'): 0,
                     ('Бентли', 'Сигнальные костры'): 0}



class Main_parameters:
    df_to_filter = client_base_to_show
    conds = dict()
    result_output = widgets.Output(layout=widgets.Layout(border='solid 1px'))
    model_collection = model_collecton
    score_name = 'Плюшевые мишки_Голубиная почта_score'
    field_names = {'is_female': 'Пол=женщина',
                     'buy_frequency': 'частота покупок',
                     'is_new_client': 'новый клиент',
                     'spent_total': 'всего потратил',
                     'buyed_items_total_cnt': 'всего купил шт.',
                     'spent_on_teddy_bear': 'потратил на плюшевых мишек',
                     'spent_on_сhristmas_decorations': 'потратил на ёлочные игрушки',
                     'spent_on_alco': 'потратил на алкоголь',
                     'spent_on_bently': 'потратил на бентли',
                     'spent_on_diapers': 'потратил на подгузники',
                     'buyed_of_teddy_bear': 'купил плюшевых мишек',
                     'buyed_of_сhristmas_decorations': 'купил елочных игрушек',
                     'buyed_of_alco': 'купил алкоголя',
                     'buyed_of_bently': 'купил бентли',
                     'buyed_of_diapers': 'купил подгузники',
                     'client_lifetime': 'как долго был клиентом',
                     'region':"регион проживания",
                     'came_from': "как стал клиентом",
                     'first_product':"первый продукт"
                    }
    
def show_html(text):
    style = """<style>
                .style1 {
                    font-size:22px;
                    font-weight:normal;
                    font-family:Verdana;

                }   
                .remark {
                    font-size:16px;
                    font-weight:normal;
                    font-family:Verdana;
                    color:rgba(128,128,128, 0.8);
                }

                h1 {
                    font-weight:normal;
                    font-size:22px;
                    color:rgb(33, 150, 243);
                } 
                 h3 {
                    font-weight:normal;
                }
                 h2 {
                    font-weight:normal;
                }

                </style>"""
    return display(HTML(style + text))
    
class Widget_creator:
    """все Handlers в виджетах изменяют объекты из Main_parameters"""
    @staticmethod
    def range_slider_and_handler_create(field_name):
        """conds - storage for filter conditions on df"""
        # min_, max_ = df_to_filter[field_name].agg(['min','max']).tolist()
        min_ = Main_parameters.df_to_filter[field_name].min()
        max_ = Main_parameters.df_to_filter[field_name].quantile(0.9)


        rng_slider = widgets.FloatRangeSlider(
                                value=[min_, max_],
                                min= min_ ,
                                max= max_,
                                step= (max_ - min_) / STEP_NUMBER,
                                description=Main_parameters.field_names[field_name],
                                disabled=False,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                readout_format='.1f',
                                layout = widgets.Layout(width="90%"),
                                style = {"description_width":"40%", "range_width":"20%"}
                            )

        @rng_slider.observe
        def show_response(rng):
            if rng['type'] == 'change' and rng['name'] == 'value':
                from_, to_ = rng['new']

                Main_parameters.conds[field_name] = \
                            [(Main_parameters.df_to_filter[field_name] >= from_),
                             (Main_parameters.df_to_filter[field_name] < to_)]

                change_output()
        return rng_slider
    
    @staticmethod
    def checkbox_and_handler_create(field_name, **kwargs):
        default_dict = dict(value=False,
                            description=Main_parameters.field_names[field_name],
                            disabled=False,
                            indent=False)
        
        if kwargs:
            default_dict.update(kwargs)
            
        checkbox = widgets.Checkbox(**default_dict)
        
        @checkbox.observe
        def show_response(checkbox):
            Main_parameters.conds[field_name] = \
                [Main_parameters.df_to_filter[field_name] == int(checkbox['owner'].value)]
            
            change_output()
        
        return checkbox
    
    @staticmethod
    def multiple_choice_create(field_name, **kwargs):
        options_list = Main_parameters.df_to_filter[field_name].unique().tolist()
        
        default_dict=dict(options=options_list,
                    description=Main_parameters.field_names[field_name],
                    disabled=False,
                    style={'description_width':"200px"})
        if kwargs:
            default_dict.update(kwargs)
        
        selector = widgets.SelectMultiple(**default_dict)
        
        @selector.observe
        def show_response(selector):
                if selector['type'] == 'change' and selector['name'] == 'value':
                    options_list_to_choose = selector['new']
                    Main_parameters.conds[field_name] = \
                            [Main_parameters.df_to_filter[field_name].isin(options_list_to_choose)] 
                    change_output()
        return selector
        
def create_widgets():
    widget_collection = []
    for col in ['spent_on_teddy_bear',
                    'spent_on_сhristmas_decorations',
                    'spent_on_alco',
                    'spent_on_bently',
                    'spent_on_diapers',
                    'buyed_of_teddy_bear',
                    'buyed_of_сhristmas_decorations',
                    'buyed_of_alco',
                    'buyed_of_bently',
                    'buyed_of_diapers',
                    'spent_total']:
        widget_collection.append(Widget_creator.range_slider_and_handler_create(col))

    for col in ["is_female", "is_new_client"]:
        widget_collection.append(Widget_creator.multiple_choice_create(col, 
                                                                       layout=widgets.Layout(height='40px')))

    for col in ["region", "came_from","first_product"]:
        widget_collection.append(Widget_creator.multiple_choice_create(col))
    return widget_collection

def create_model_choosing_widget(model_collection):
    choose_product_widget = widgets.Dropdown(options=list(set([i[0] for i in list(model_collection.keys())])),
                     value=list(set([i[0] for i in list(model_collection.keys())]))[0],
                     description="Какой продукт продвигать:",
                     layout=widgets.Layout(width="50%"), style={"description_width":"50%"})

    choose_channel_widget = widgets.Dropdown(options=list(set([i[1] for i in list(model_collection.keys())])),
                     value=list(set([i[1] for i in list(model_collection.keys())]))[0],
                     description="Через какой канал:",
                     layout=widgets.Layout(width="50%"), style={"description_width":"50%"})

    @choose_product_widget.observe
    def some_func(w):
        if w['type'] == 'change' and w['name'] == 'value':
            # model = np.random.choice(list(model_collection.values()))
            by_product = w['new']
            by_channel = choose_channel_widget.value
            
            Main_parameters.score_name = by_product + "_" + by_channel +"_score"
            change_output()

    @choose_channel_widget.observe
    def some_func(w):
        if w['type'] == 'change' and w['name'] == 'value':
            by_product = choose_product_widget.value
            by_channel = w['new']

            Main_parameters.score_name = by_product + "_" + by_channel +"_score"
            change_output()
            

    return choose_product_widget, choose_channel_widget
    




def change_output() -> None:
    """обрабатывает объекты из Main_parameters"""
    with Main_parameters.result_output:
        clear_output(wait=True)
        
        conds_to_filter = []
        for cond_pair in Main_parameters.conds.values():
            conds_to_filter.extend(cond_pair)
        
        score_name = Main_parameters.score_name
        
        format_func = lambda x: "{:,.0f}".format(x).replace(",", " ")
        
        if len(conds_to_filter):
            to_dict = Main_parameters.df_to_filter[np.logical_and.reduce(conds_to_filter)][score_name]\
                    .agg(['mean','count']).to_dict()
        else:
            to_dict = Main_parameters.df_to_filter[score_name]\
                    .agg(['mean','count']).to_dict()
            
        show_html("""<div class="style1"> Расчитанные параметры будущей маркетинговой кампании :""") 
        show_html("""<div class="remark">(на основе введённого таргетинга и модели склонности к отклику)""")
        show_html("""<div class="style2"> Число клиентов с полученными предложениями: <h2>""" \
                      + format_func(int(to_dict['count'])) + "</h2></h3>")
        show_html("""<div class="style2"> Число откликнувшихся: <h2>""" \
                          + format_func(int(to_dict['count'] * to_dict['mean'])) + "</h2></h3>")
        show_html("""<div class="style2"> Средний отклик: <h2>""" \
                          + str(round(to_dict['mean']*100, 2)) +" %" + "</h2></h3>")
        
        resps_cnt_by_model = int(Main_parameters.df_to_filter[score_name]\
                                .sort_values(ascending=False)[:int(to_dict['count'])].sum())
        print()
        show_html("""<div class="style1"> 
                В случае выбора такого же количества клиентов по скору модели:""")
        show_html("""<div class="remark">(без введённого таргетинга, но на том же числе клиентов)</div>""")
        show_html("""<div class="style2"> откликов: <h2>""" + format_func(resps_cnt_by_model) + "</h2> " + "</h4>")
        
        show_html("""<div class="style2"> % отклика: <h2>""" + \
                  "{:,.2%}".format(resps_cnt_by_model/to_dict['count']) + "</h2> " + "</h4>")
        
def useful_tool(bt=None):
    Main_parameters.conds = dict()
    choose_product_widget, choose_channel_widget = create_model_choosing_widget(Main_parameters.model_collection)
    widget_collection = create_widgets()
    
    button = widgets.Button(description="Сбросить фильтры", layout=widgets.Layout(width="50%"))
    
    button.on_click(useful_tool)

    main_interface = widgets.HBox([widgets.VBox(widget_collection, layout=widgets.Layout(width="600px",
                                                                               border='solid 1px')), 
                                   Main_parameters.result_output])
    
    control_interface = widgets.HBox([widgets.VBox([choose_product_widget, choose_channel_widget],
                                                  layout=widgets.Layout(width="100%")),
                                     button])
    clear_output(wait=True)
    show_html("""<h1>
                Калькулятор откликов маркетинговых кампаний по заданному таргетингу:</h1>""")
    display(widgets.VBox([control_interface, main_interface]))
    change_output()
    
useful_tool()