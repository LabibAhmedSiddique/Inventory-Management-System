import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class BistaEmployeeEducation(models.Model):
    _name = "bista.employee.education"
    _description = "Bista Employee Educations"
    _rec_name = 'degree_name'

    degree_name = fields.Char(string="Degree Name")
    full_name = fields.Char(string="Full Name of the Degree")