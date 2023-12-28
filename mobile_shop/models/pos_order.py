from odoo import api, fields, models, _
import logging
_log = logging.getLogger(__name__)
class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    product_cost = fields.Float(string="Cost",compute="_compute_product_cost",
        readonly=True,
        store=True
     )
    @api.depends('product_id')
    def _compute_product_cost(self):
        for rec in self:
            pol = rec.env['purchase.order.line']
            pol_find = pol.search([('product_id', '=', rec.product_id.id)])
            pol_count = pol.search_count([('product_id', '=', rec.product_id.id)])
            on_hand_qty = rec.product_id.qty_available
            cost_line = sum(line.price_unit for line in pol_find)
            if pol_count:
                cost = cost_line / pol_count
                rec.product_cost = cost
            else:
                rec.product_cost = rec.product_id.standard_price

    pos_categ_id = fields.Many2one(
        string="POS Category",
        comodel_name="pos.category",
        related='product_id.pos_categ_id',
        readonly=True,
        store=True
    )
    order_name = fields.Char(string="name", 
        related='order_id.name',
        readonly=True,
        store=True)
    date_orders = fields.Datetime(string="Field name", related='order_id.date_order',
        readonly=True,
        store=True )
    partner_ids = fields.Many2one(
        string="partner_id",
        comodel_name="res.partner",
        related='order_id.partner_id',
        readonly=True,
        store=True
    )
    user_ids = fields.Many2one(
        string="partner_id",
        comodel_name="res.users",
        related='order_id.user_id',
        readonly=True,
        store=True
    )
    session_ids = fields.Many2one(
        string="partner_id",
        comodel_name="pos.session",
        related='order_id.session_id',
        readonly=True,
        store=True
    )
    
    def calculate_product_cost(self):
        # return True
        posl = self.env['pos.order.line'].search([])
        for rec in posl:
            pol = rec.env['purchase.order.line']
            pol_find = pol.search([('product_id', '=', rec.product_id.id)])
            pol_count = pol.search_count([('product_id', '=', rec.product_id.id)])
            cost_line = sum(line.price_unit for line in pol_find)
            if pol_count:
                cost = cost_line / pol_count
                rec.product_cost = cost
                _log.exception("==============================calculate_product_cost")

            else:
                rec.product_cost = rec.product_id.standard_price
                _log.exception("==============================calculate_product_cost")
