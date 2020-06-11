from odoo import api, fields, models



class Covers(models.Model):
      _name = 'cover.benfeits'


      cover_name = fields.Char('Cover')
      ar_cover = fields.Char('Arabic Cover')
      product_id = fields.Many2one('product.covers', string="product_id",ondelete='cascade')

class ProductCovers(models.Model):
      _name = 'product.covers'
      _rec_name = 'product_name'

      product_name = fields.Char('Product Name')
      ar_product_name = fields.Char('Arabic Product Name')
      cover_ids = fields.One2many('cover.benfeits', 'product_id', string="Category Benefit")

      # @api.multi
      def price(self):
            self.env['motor.api'].get_covers(
                  {'type': 'General', 'lang': 'ar'})


class MotorRating(models.Model):
      _name = 'motor.rating.table'
      brand = fields.Selection([('all brands', 'All Brands (except Chinese & East Asia)'),
                               ('chinese cars & east asia', 'Chinese Cars & East Asia'),('all models','All Models')],
                              'Brand')
      deductible = fields.Selection([('250 EGP', '250 EGP'),
                                ('4 Per Thousand', '4 Per Thousand')],
                               'Deductible')

      sum_insured_from = fields.Float('From Sum Insured')
      sum_insure_to = fields.Float('To Sum Insured')
      product_id = fields.Many2one('product.covers',ondelete='cascade')
      # product = fields.Char(related='product_id.product_name', string='product', store=True)

      rate = fields.Float('Rate', digits=(12,4))




class MotorApi(models.Model):
      _name = 'motor.api'

      @api.model
      def get_price(self,data):
            if data.get('product') == 'Total Loss Only':
                  rate = self.env['motor.rating.table'].search(
                        [('brand', '=', 'all models'), ('product_id.product_name', '=', data.get('product')),
                         ('sum_insured_from', '<=', data.get('price')), ('sum_insure_to', '>=', data.get('price'))])
                  price = data.get('price')*rate.rate
            else:
                 price = {}
                 if data.get('brand') == 'all brands':
                        rates = self.env['motor.rating.table'].search([('brand','=',data.get('brand' )),('product_id.product_name','=',data.get('product')),
                                                          ('sum_insured_from','<=', data.get('price')),('sum_insure_to', '>=', data.get('price'))])
                        for rate in rates:
                            price.update({rate.deductible: data.get('price') * rate.rate})
                 else:
                       rate = self.env['motor.rating.table'].search(
                             [('brand', '=', data.get('brand')),
                              ('product_id.product_name', '=', data.get('product')),
                              ('sum_insured_from', '<=', data.get('price')),
                              ('sum_insure_to', '>=', data.get('price'))])
                       price = data.get('price') * rate.rate
            return price

      @api.model
      def get_covers(self,data):
            res = []
            if data.get('lang') == 'en':
                  covers = self.env['product.covers'].search(
                              [('product_name', '=', data.get('type'))]).cover_ids
                  for cover in covers:
                        res.append(cover.cover_name)
                  print(res)
                  return res
            else:
                  covers = self.env['product.covers'].search(
                        [('product_name', '=', data.get('type'))]).cover_ids
                  for cover in covers:
                        if cover.ar_cover != False:
                              res.append(cover.ar_cover)
                  print(res)
                  return res


class aropeHelpDesk(models.Model):
    _inherit = 'helpdesk_lite.ticket'

    sum_insured = fields.Float('Sum Insured')
    brand = fields.Char('Brand')
    product_id = fields.Many2one('product.covers')

class ticketApi(models.Model):
      _inherit = 'ticket.api'

      @api.model
      def create_motor_ticket(self, data):
            name = 'Motor Ticket'
            ids = self.env['product.covers'].search([('product_name','=', data.get('product'))]).id

            ticket = self.env['helpdesk_lite.ticket'].create(
                  {'name': name, 'contact_name': data.get('name'), 'phone': data.get('phone'),
                   'email_from': data.get('mail'), 'sum_insured': data.get('price'), 'brand': data.get('brand'), 'product_id': ids})
            return ticket.id
