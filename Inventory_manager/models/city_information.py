import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class BistaJobPosition(models.Model):
    _name = "bista.city.information"
    _description = "Employee City Address"
    _rec_name = 'city_name'

    city_name = fields.Char(string="City Name")

    employee_ids = fields.One2many('bista.employee','employee_city_address_id',string="Employees")

    # employee_ids = fields.One2many('bista.employee', 'job_position_id', string="Employees")