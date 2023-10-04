import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class ResPartner(models.Model):
    #ihnerit the original model.
    _inherit = 'res.partner'

    gender = fields.Selection([('male',"Male"),('female',"Female"),('other','Other')], string="Gender")
    secondary_contact = fields.Char(string="Secondary Contact")

    @api.model
    def create(self, values):
        if not values.get('gender'):
            raise UserError("Please put gender value")
        res = super(ResPartner, self).create(values)
        return res