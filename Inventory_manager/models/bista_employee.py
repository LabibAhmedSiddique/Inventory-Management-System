import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class BistaEmployee(models.Model):
    _name = "bista.employee"
    _description = "Bista Employee Details"
    _rec_name = 'name'


    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    name = fields.Char(string="Employee Name")
    gender = fields.Selection(
        string="Gender", 
        selection= [
            ('male','Male'),
            ('female','Female'),
            ('other','Other')
        ]
    )
    date_of_birth = fields.Date(string="Birth-Date")
    # employee_age = fields.Integer(string="employee_age")
    # calculate age from birthdate. need to store to view the data.
    # employee_age = fields.Integer(string= 'Age',compute = "_age_calculate", store = True)
    #onchange field
    employee_age = fields.Integer(string= 'Age')
    employee_city_address_id = fields.Many2one('bista.city.information')
    present_address = fields.Text(string="Detail Address")
    employee_last_degree = fields.Char(string="Educational Status")
    employee_religion = fields.Char(string="Religion")
    employee_nationality = fields.Char(string="Nationality")

    phone_no = fields.Char(string="Phone No")
    email_address = fields.Char(string="Email Address")    

    employee_id = fields.Char(string="Employee Id")
    employee_designation = fields.Selection(
        string="Designation",
        selection=[
            ('junior_dev','Junior Developer'),
            ('senior_dev','Senior Developer'),
            ('ml_engineer','Machine learning Engr'),
            ('android_dev','Android Developer'),
            ('project_lead','Project Lead'),
        ],
        default = 'junior_dev'
    )
    # default value method
    def _get_default_joining_date(self):
        return datetime.now().date()
    @api.model
    def default_get(self,fields):
        values = super(BistaEmployee,self).default_get(fields)
        values["employee_nationality"] = "Bangladeshi"
        # print(values,"________________________________")
        return values
    joining_date = fields.Date(string="Joining Date", default=_get_default_joining_date)
    total_experience = fields.Char(string="Job Experience")
    on_leave = fields.Boolean(string= "On Leave", default = False)
    payment_ammount = fields.Float(string= "Payment Ammount", default=0.00)
    comment_about_employee = fields.Text(string="Comments")
    is_remote = fields.Boolean(string="Remote")
    employee_photos = fields.Image(string="Profile photo", max_width=150 ,max_height=150)
    employee_photos_name = fields.Char(string="Photo Name")
    nid_scan = fields.Binary(string="NID varification")
    contract_letter = fields.Binary(string="Contract Letter")
    # assigned Task, assigned on, deadline, supervisor
    assigned_task = fields.Text(string="Assigned Task")
    # Datetime fields takes both date and time.
    assigned_task_time = fields.Datetime(string="Assigned On",default=lambda self: datetime.now())
    task_deadline = fields.Datetime(string="Deadline")
    task_time = fields.Char(string="Remaining Time", compute="_task_remaining_time_computed")
    task_time_given = fields.Char(string="Time Given For Task", compute="_get_task_time_given_computed", store = True)
    assigned_supervisor = fields.Char(string="Supervisor Name")
    #For many2one set the name as [{name}_id]
    job_position_id = fields.Many2one('bista.job.position', string="Job Position")
    #For many2many set the name as [{name}_ids]
    job_position_ids = fields.Many2many('bista.job.position', string="Job Position")

    employee_skill_ids = fields.Many2many('bista.employee.skill', string="Employee Skills")
    employee_education_ids = fields.Many2many('bista.employee.education', string="Educational Degree(s)") #TO_DO: Create XML file

    #computed
    @api.depends('task_deadline')
    def _task_remaining_time_computed(self):
        if self and self.task_deadline:
            self.task_time = str(self.task_deadline - datetime.now())
        else: #if computed field is not stored then use else condition
            self.task_time = None
    
    @api.depends('assigned_task_time','task_deadline')
    def _get_task_time_given_computed(self):
        if self and self.task_deadline and self.assigned_task_time:
            self.task_time_given = str(self.task_deadline - self.assigned_task_time)



    #api.onchange change the value of fields depanding on other fields
    @api.onchange('date_of_birth')
    def onchange_date_of_birth(self):
        # print("=============== onchange date of birth")
        if self and self.date_of_birth:
            age = (datetime.today().date() - datetime.strptime(str(self.date_of_birth), '%Y-%m-%d').date()) // timedelta(days=365)
            self.employee_age = age

    @api.onchange('employee_designation','total_experience')
    def onchange_calculate_payment(self):
        if self and self.employee_designation and self.total_experience:
            if str(self.employee_designation)=='junior_dev':
                base_salary = 30000
                experience_bonus=(int(self.total_experience)*10000)
            elif str(self.employee_designation)=='senior_dev':
                base_salary = 50000
                experience_bonus=(int(self.total_experience)*20000)
            elif str(self.employee_designation)=='ml_engineer':
                base_salary = 45000
                experience_bonus=(int(self.total_experience)*15000)
            elif str(self.employee_designation)=='android_dev':
                base_salary = 45000
                experience_bonus=(int(self.total_experience)*15000)
            elif str(self.employee_designation)=='project_lead':
                base_salary = 90000
                experience_bonus=(int(self.total_experience)*25000) 
            self.payment_ammount = base_salary + experience_bonus

    #inherit create method
    @api.model
    def create(self, vals_list):
        if vals_list.get("first_name") and vals_list.get("last_name"):
            vals_list['name'] = str(vals_list.get("first_name") +" "+ vals_list.get("last_name"))
        elif vals_list.get("first_name") and not vals_list.get("last_name"):
            vals_list['name'] = str(vals_list.get("first_name"))
        elif vals_list.get("last_name") and not vals_list.get("first_name"):
            vals_list['name'] = str(vals_list.get("last_name"))
        else:
            raise ValidationError("Please provide First Name or Last Name or Both.")
        #print(vals_list,"++++++++++++++++++++++++++")    
        if vals_list['phone_no']!= False:
            if len(vals_list['phone_no'])>14 or len(vals_list['phone_no'])<11:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals_list['phone_no'])==11:
                if vals_list['phone_no'][0:3]!='+88':
                    vals_list['phone_no']='+88'+vals_list['phone_no']
                else:
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals_list['phone_no'])==14:
                if vals_list['phone_no'][0:3]!='+88':
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            else:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")


        # print(self.name,'1111111111111111111111')
        result = super(BistaEmployee,self).create(vals_list) #in 'result' we will get the object that is created.
        print(result.first_name) #shows the first name of the object
        print(result.last_name) #shows the last name of the object
        # print(result) #shows the object using id
        # print(self) #shows only the class name/defination
        # result.first_name = "Ajke amar mon valo nai" #change the first name of the object. odoo call a 'write' method with-in 'create'
                                                        ## to edit the 'first name' of 'result' object. 
        return result

    #inherit write function_____________________________________________________________________
    # @api.model
    def write(self, vals):
        if 'phone_no' in vals:
            if len(vals['phone_no'])>14 or len(vals['phone_no'])<11:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals['phone_no'])==11:
                if vals['phone_no'][0:3]!='+88':
                    vals['phone_no']='+88'+vals['phone_no']
                else:
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            elif len(vals['phone_no'])==14:
                if vals['phone_no'][0:3]!='+88':
                    raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            else:
                raise ValidationError("Wrong Phone number!! : please insert correct phone number.")
            
        if "first_name" in vals or "last_name" in vals:
            # print("____________________________________________")
            if vals.get("first_name") and vals.get("last_name"):
                vals['name'] = vals.get("first_name") +" "+ vals.get("last_name")
            elif vals.get("first_name") and not vals.get("last_name"):
                vals['name'] = vals.get("first_name")+" "+self.last_name
            elif vals.get("last_name") and not vals.get("first_name"):
                vals['name'] = self.first_name+" "+vals.get("last_name")


        print(vals)
        result = super(BistaEmployee,self).write(vals)
        return result

    #this function will 
    def write_my_value(self):
        # self.first_name = "Ajke amar mon valo nai"
        ## search spesific recorde using odoo ORM. search with '|' means or relation for next two tuples, for more tuples relation add '|'
        ## for 'and' relation use no '|' ore place the tuple before '|'.
        ## example: and with or= search([('first_name','=','Kotha'),'|',('last_name','=','Kotha'),('employee_id','=','123')])
        ## more then one or : search('|','|',[('first_name','=','Kotha'),('last_name','=','Kotha'),('employee_id','=','123')])
        # object = self.env['bista.employee'].search(['|',('last_name','=','Kotha'),('employee_id','=','123')])
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # for i in object:  #for multiple objects wo run aloop
            # print(object)
            # i.last_name = "Kno Kotha nai"
        #search >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        object_2 = self.env['bista.employee'].search([('email_address','=','mahadi@gmail.com')])
        #search returen the object.
        #Browse use directly int id and return the object.
        job_position_object = self.env['bista.job.position'].browse(object_2.job_position_id.id)

        print(job_position_object,">>>>>>>>>>>>>>>>>")
        #both upperline and lowerline returns same object.
        raise UserError(object_2.job_position_id)
 
    #print name of searched object>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def find_senior_dev(self):
        objs = self.env['bista.employee'].search([('job_position_id', '=','Senior Developer')])
        for obj in objs:
            print(obj.name)

    #popup, wizard view >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def view_job_psition_detail(self):
        form_view_id = self.env.ref('bista_first_addons.view_bista_employee_job_position_form_simple')
        return {
            'type': 'ir.actions.act_window',
            'name': _('Job Position'),
            'res_model': 'bista.job.position',
            'view_mode': 'form',
            'res_id': self.job_position_id.id, #shows spesific job positions view
            'view_id': form_view_id.id, 
            'target':'new' # current / main | new: show as popup screen, current: breadcrambs, main: remove all breadcrambs
        }



    #Extras email validation>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    @api.onchange('email_address')
    def onchange_email_validaation_check(self):
        if self and self.email_address:
            if not re.match("^[a-z0-9]+@[a-z0-9]+[.][a-z]+.*",self.email_address):
                raise UserError(str(self.email_address)+" isn't valid email. provide a valid email id")


        
    # @api.multi is by default in every function
    # Function for buttons
    def compute_total_salary_in_employee_form(self):
        # relativedelta cself.date_of_birthonsider 31/30 months to calculate difference between datetime and 
        # return as datetime object. [object.]months return the month value of relativedelta object. 
        # By adding 12 month multipling years gives the result of total months.
        relative_duration = relativedelta.relativedelta(datetime.today(),datetime.strptime(str(self.joining_date),'%Y-%m-%d'))
        employee_working_duration = relative_duration.months+(relative_duration.years*12)
        if int(employee_working_duration)>=12 :
            raise UserError("Total salary is: "+str(self.payment_ammount+20000.00))
        elif int(employee_working_duration)>=6:
            raise UserError("Total salary is: "+str(self.payment_ammount+10000.00))
        else:
            raise UserError("Total salary is: "+str(self.payment_ammount))
        raise UserError(str(employee_working_duration))

    def see_info_of_employee_assingment(self):
        if self.assigned_task:
            raise UserError(
                "Assigned Task: "+str(self.assigned_task)+
                "\nAssigned On: "+str(self.assigned_task_time)+
                "\nDeadline: "+str(self.task_deadline)+
                "\nSupervisor Name: "+str(self.assigned_supervisor)
            )
        raise UserError("No assingment is assinged for this employee")

    # #computed field method for employee_age
    # @api.depends('date_of_birth')
    # def _age_calculate(self):
    #     if self.date_of_birth :
    #         self.employee_age = (datetime.today().date() - datetime.strptime(str(self.date_of_birth), '%Y-%m-%d').date()) // timedelta(days=365)

    