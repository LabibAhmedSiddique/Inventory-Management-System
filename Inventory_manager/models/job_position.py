import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class BistaJobPosition(models.Model):
    _name = "bista.job.position"
    _description = "Bista Job Position"
    _rec_name = 'name'

    name = fields.Char(string="Job Position")

    employee_ids = fields.One2many('bista.employee', 'job_position_id', string="Employees")