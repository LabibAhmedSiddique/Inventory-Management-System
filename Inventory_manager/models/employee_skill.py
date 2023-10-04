import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class BistaEmployeeSkill(models.Model):
    _name = "bista.employee.skill"
    _description = "Bista Employee Skills"
    _rec_name = 'name'

    name = fields.Char(string="Skill Name")
    #reverse relation for many2many field
    employee_ids = fields.Many2many("bista.employee","bista_employee_bista_employee_skill_rel")
    skill_type = fields.Selection(
        string="Skill Type",
        selection=[
            ('soft','Soft Skills'),
            ('technical','Technical')
        ]
    )