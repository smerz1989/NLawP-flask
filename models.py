from flask_wtf import FlaskForm
from wtforms.fields import SelectField, SubmitField 
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, Email, Required

CASETYPES = [('01','Habeas Corpus-US'),('02','Habeas Corpus-State'),
             ('03','Criminal Court Motions'),('04','Contempt Of Court'),
             ('05','(Non)Conv-Criminal Case'),('06','Alien Petitions'),
             ('07','Native American Rights'),('08','Voting Rights'),
             ('09','Social Security Case'),('10','Racial Discrimination'),
             ('11','14th Amendment'),('12','Military Exclusion'),
             ('13','Free Of Expression'),('14','Free Of Religion'),
             ('15','Union V. Company'),('16','Member V Union'),
             ('17','Employee V. Employer'),('18','Commercial Regulation'),
             ('19','Environmental Protection'),('20','Local/State Economic'),
             ('21','Labor Dispute-Govt V Union/Employer'),('22','Rent Control, Excess Profits'),
             ('23','Womens/Gender Rights'),('24','NLRB V Employer'),
             ('25','NLRB V Union'),('26','Handicapped Rights'),
             ('27','Reverse Discrim-Race'),('28','Reverse Discrim-Sex'),
             ('29','Right To Privacy'),('30','Age Discrimination'),
             ('31','Sentencing Guidelines Deviation')]

class OutcomeForm(FlaskForm):
    case_type = SelectField('Case Type',default='01',choices=CASETYPES)
    desired_outcome =  SelectField('Desired Outcome',default="con",choices=[('con','Conservative'),('lib','Liberal')])
    #stock_ticker=TextField('Stock Symbol',validators=[Required()])
    #month = DateField('Month',render_kw={'data-provide':'datepicker'})
    submit = SubmitField('Submit')
