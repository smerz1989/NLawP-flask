import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column,row
from bokeh.embed import components
from bokeh.models import (ColumnDataSource,TableColumn, DataTable, LinearColorMapper, HoverTool,Dropdown,CDSView,Select, 
			PrintfTickFormatter, GeoJSONDataSource, CustomJS,CustomJSFilter)
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, STAMEN_TERRAIN
from bokeh.palettes import Blues9, Reds9,RdBu11
import json


CASETYPES = [('habeas corpus-US','Habeas Corpus-US'),('habeas corpus-state','Habeas Corpus-State'),
             ('criminal court motions','Criminal Court Motions'),('contempt of court','Contempt Of Court'),
             ('(non)conv-criminal case','(Non)Conv-Criminal Case'),('alien petitions','Alien Petitions'),
             ('Native American rights','Native American Rights'),('voting rights','Voting Rights'),
             ('Social Security case','Social Security Case'),('racial discrimination','Racial Discrimination'),
             ('14th amendment','14th Amendment'),('military exclusion','Military Exclusion'),
             ('free of expression','Freedom Of Expression'),('free of religion','Freedom Of Religion'),
             ('union v. company','Union V. Company'),('member v union','Member V Union'),
             ('employee v. employer','Employee V. Employer'),('commercial regulation','Commercial Regulation'),
             ('environmental protection','Environmental Protection'),('local/state economic','Local/State Economic'),
             ('labor dispute-govt v union/employer','Labor Dispute-Govt V Union/Employer'),
             ('rent control, excess profits','Rent Control, Excess Profits'),
             ('womens rights','Womens/Gender Rights'),('NLRB v employer','NLRB V Employer',),
             ('NLRB v union','NLRB V Union'),('handicapped rights','Handicapped Rights'),
             ('reverse discrim-race','Reverse Discrim-Race'),('reverse discrim-sex','Reverse Discrim-Sex'),
             ('right to privacy','Right To Privacy'),('age discrimination','Age Discrimination'),
             ('Sentencing guidelines deviation','Sentencing Guidelines Deviation')]

def create_callback(geosource,judge_source):
    js_callback = CustomJS(args=dict(stuff=geosource,otherstuff=judge_source),
                    code="""
                    otherstuff.change.emit();
                    stuff.change.emit();""")
    return js_callback

def create_filter(dropdown,geosource):
    js_filter = custom_filter = CustomJSFilter(args=dict(dropdown=dropdown,geodata=geosource),
                              code="""
				var indices = [];
				for (var i = 0; i < geodata.data.casetype.length; i++){
				  if (geodata.data['casetype'][i] == dropdown.value){
   				    indices.push(true);
				  } else {
 				    indices.push(false);
 				  }
				}
				return indices;
				""")
    return js_filter

def create_dropdown(callback,menu=CASETYPES,label="Case Type"):
    d = Select(title=label,value="habeas corpus-US",
            options=menu,max_width=130,css_classes=["form-control"])
    d.js_on_change('value',callback)
    return d

def format_plot(p):
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks

    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None 
    p.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    p.yaxis.major_label_text_font_size = '0pt'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

def create_table(judge_source,dropdown):
    custom_filter = CustomJSFilter(args=dict(dropdown=dropdown,judgedata=judge_source),
                              code="""
	var indices = [];
	// iterate through rows of data source and see if each satisfies some constraint
	for (var i = 0; i < judgedata.data.casetype.length; i++){
	 if (judgedata.data['casetype'][i] == dropdown.value){
	   console.log(source.data['casetype'][i])
	   indices.push(true);
	 } else {
	   indices.push(false);
	 }
	}
	return indices;
	""")
    view = CDSView(source =judge_source, filters = [custom_filter])
    columns = [
        TableColumn(field="statdist_formatted", title="District"),
        TableColumn(field="judge", title="Judge"),
        TableColumn(field="casetype",title="Case Type"),
        TableColumn(field="Con_Prob", title="Probability Conservative"),
    ]
    table = DataTable(source=judge_source,columns=columns,view=view)
    print(table)
    return table

def create_geoplot(geojsonfile):
    geojson = json.load(open(geojsonfile,'r'))
    geo_source = GeoJSONDataSource(geojson=json.dumps(geojson))
    judge_df = pd.read_csv('./static/data/judge_prediction_probs.csv')
    judge_source = ColumnDataSource(judge_df)

    tile_provider = get_provider(CARTODBPOSITRON)
    tooltips = [("District","@DISTRICT"),("District Number","@District_N"),
                ("Liberal Win Chance","@lib_prob"),("Conservative Win Chance","@con_prob")]
    p = figure(x_range=(-1.4e7,-7e6),y_range=(2.6e6,6.4e6),plot_height = 600 , plot_width = 950,
                       x_axis_type="mercator", y_axis_type="mercator",tooltips=tooltips)
    p.toolbar_location = None
    format_plot(p)
    dropdown = create_dropdown(create_callback(geo_source,judge_source))
    custom_filter = create_filter(dropdown,geo_source)
    view = CDSView(source=geo_source,filters=[custom_filter])
    table = create_table(judge_source,dropdown)
    p.add_tile(tile_provider)
    blues_palette = tuple(reversed(RdBu11))
    color_mapper = LinearColorMapper(palette=blues_palette,low=0,high=1)
    patches = p.patches('xs','ys',source=geo_source,fill_color={'field':'lib_prob','transform':color_mapper},
            fill_alpha=1,hover_line_color="black",hover_fill_color="white",line_color="white",line_width=0.5,view=view)
    script, div = components(column(row(column(dropdown,sizing_mode="fixed",height=250,width=150),
                                 column(p,sizing_mode="scale_width")),column(table,sizing_mode="scale_width"),css_classes=["justify-content-center"]))
    return script,div

