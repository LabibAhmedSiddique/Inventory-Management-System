import re
from datetime import datetime, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError ,Warning

class SaleOrder(models.Model):
    #ihnerit the original model.
    _inherit = 'sale.order'

    customer_phone_no = fields.Char(string="Customers Phone")
    customer_secondary_contact = fields.Char(string="Secondary Phone")

    # the structure of inherited button_action need to be same as original. include api if there is any in original.
    def action_confirm(self):
        if self.validity_date == False:
            raise UserError("The Expiration field cannot be blank")

        for line in self.order_line: 
            #order_line is one2many field so we need to use loop
            if line.price_unit <=0:
                raise UserError("Please Set Unit Price for product '{}'".format(line.product_id.name))
            if line.product_uom_qty <=0:
                raise UserError("Please Set Quantity for product '{}'".format(line.product_id.name))
        res = super(SaleOrder, self).action_confirm()

        return res
    
    #onchange of customer name we will show phone number
    @api.onchange("partner_id")
    def onchange_partner_id_add_phone_no(self):
        if self and self.partner_id :
            # partner_id is a many2one field so it always refers with id. So no need to use search
            if self.partner_id.phone:
                self.customer_phone_no = self.partner_id.phone
            elif self.partner_id.mobile:
                self.customer_phone_no = self.partner_id.mobile
            else:
                #if dont use false then the field wont change if there is no number and once filled.
                self.customer_phone_no = False
            if self.partner_id.secondary_contact:
                self.customer_secondary_contact=self.partner_id.secondary_contact
            else:
                self.customer_secondary_contact=False