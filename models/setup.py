from odoo import api, fields, models

class Brands(models.Model):
      _name='car.brands'
      _rec_name = 'brand'

      brand=fields.Char('Brand')

class Covers(models.Model):
      _name = 'cover.benfeits'


      cover_name = fields.Char('Cover')
      ar_cover = fields.Char('Arabic Cover')
      amount = fields.Float('Amount')
      product_id = fields.Many2one('product.covers', string="product_id",ondelete='cascade')

class ProductCovers(models.Model):
      _name = 'product.covers'
      _rec_name = 'product_name'
      
      product_name = fields.Char('Product Name')
      ar_product_name = fields.Char('Arabic Product Name')
      cover_ids = fields.One2many('cover.benfeits', 'product_id', string="Category Benefit")
      motor_rating_ids = fields.One2many('motor.rating.table', 'product_id', string="Rates")

      # @api.multi
      def price(self):
            self.env['motor.api'].get_price(
                  {'brand': 'chinese cars & east asia', 'lang': 'en','price':500000})


class MotorRating(models.Model):
      _name = 'motor.rating.table'
      brand = fields.Selection([('all brands', 'All Brands (except Chinese & East Asia)'),
                               ('chinese cars & east asia', 'Chinese Cars & East Asia'),('all models','All Models')],
                              'Brand')
      deductible = fields.Char('Deductible')
            # fields.Selection([('250 EGP', '250 EGP'),
            #                     ('4 Per Thousand', '4 Per Thousand')],
            #                    'Deductible')

      sum_insured_from = fields.Float('From Sum Insured')
      sum_insure_to = fields.Float('To Sum Insured')
      product_id = fields.Many2one('product.covers',ondelete='cascade')
      # product = fields.Char(related='product_id.product_name', string='product', store=True)

      rate = fields.Float('Rate', digits=(12,4))




class MotorApi(models.Model):
      _name = 'motor.api'

      @api.model
      def get_price(self,data):
            result = []
            price = {}
            dic = {}
            deductible ={}

            if data.get('lang') == 'en':
                  for record in self.env['product.covers'].search([('motor_rating_ids.brand', 'in', [data.get('brand'),'all models']),
                        ('motor_rating_ids.sum_insured_from', '<=', data.get('price')),('motor_rating_ids.sum_insure_to', '>=', data.get('price'))]):
                        cover_amount = 0.0
                        for cover in record.cover_ids:
                              cover_amount += cover.amount
                        for rec in record.motor_rating_ids:
                              if rec.sum_insured_from <= data.get('price') and rec.sum_insure_to >= data.get('price'):
                                    price.update({'cover': 'Price', record.product_name: 'EGP ' + str((rec.rate*data.get('price'))+cover_amount)})
                                    if rec.deductible == False:
                                          deductible_value = ''
                                    else:
                                          deductible_value = rec.deductible
                                    deductible.update({'cover': 'Deductible', record.product_name: deductible_value})

                  result.append(price)
                  result.append(deductible)
                  for cover in self.env['cover.benfeits'].search([]):
                        res = []
                        for rec in self.env['product.covers'].search([('motor_rating_ids.brand', 'in', [data.get('brand'),'all models']),
                              ('motor_rating_ids.sum_insured_from', '<=', data.get('price')),('motor_rating_ids.sum_insure_to', '>=', data.get('price'))]):
                              for record in rec.cover_ids:
                                    if record.cover_name == cover.cover_name:
                                          val = 'true'
                                          res.append({rec.product_name: val})
                        if cover.cover_name not in dic.keys():
                              dic[cover.cover_name] = res
                  d = {}
                  for key, val in dic.items():
                        for rec in val:
                              for k,v in rec.items():
                                    d['cover']=key
                                    d[k]=v
                        result.append(d)
                        d={}
                  print(result)
                  return result
            else:
                  for record in self.env['product.covers'].search([('motor_rating_ids.brand', 'in', [data.get('brand'),'all models']),
                        ('motor_rating_ids.sum_insured_from', '<=', data.get('price')),('motor_rating_ids.sum_insure_to', '>=', data.get('price'))]):
                        cover_amount = 0.0
                        for cover in record.cover_ids:
                              cover_amount += cover.amount
                        for rec in record.motor_rating_ids:
                              if rec.sum_insured_from <= data.get('price') and rec.sum_insure_to >= data.get('price'):
                                    price.update({'cover': 'السعر', record.ar_product_name: 'EGP ' + str((rec.rate*data.get('price'))+cover_amount)})
                                    if rec.deductible == False:
                                          deductible_value = ''
                                    else:
                                          deductible_value = rec.deductible
                                    deductible.update({'cover': 'التحمل', record.ar_product_name: deductible_value})

                  result.append(price)
                  result.append(deductible)
                  for cover in self.env['cover.benfeits'].search([]):
                        res = []
                        for rec in self.env['product.covers'].search([('motor_rating_ids.brand', 'in', [data.get('brand'),'all models']),
                              ('motor_rating_ids.sum_insured_from', '<=', data.get('price')),('motor_rating_ids.sum_insure_to', '>=', data.get('price'))]):
                              for record in rec.cover_ids:
                                    if record.ar_cover == cover.ar_cover:
                                          val = 'true'
                                          res.append({rec.ar_product_name: val})
                        if cover.ar_cover not in dic.keys():
                              dic[cover.ar_cover] = res
                  d = {}
                  for key, val in dic.items():
                        for rec in val:
                              for k,v in rec.items():
                                    d['cover']=key
                                    d[k]=v
                        result.append(d)
                        d={}
                  print(result)
                  return result



            # if data.get('product') == 'Total Loss Only':
            #       rate = self.env['motor.rating.table'].search(
            #             [('brand', '=', 'all models'), ('product_id.product_name', '=', data.get('product')),
            #              ('sum_insured_from', '<=', data.get('price')), ('sum_insure_to', '>=', data.get('price'))])
            #       price = data.get('price')*rate.rate
            # else:
            #      price = {}
            #      if data.get('brand') == 'all brands':
            #             rates = self.env['motor.rating.table'].search([('brand','=',data.get('brand' )),('product_id.product_name','=',data.get('product')),
            #                                               ('sum_insured_from','<=', data.get('price')),('sum_insure_to', '>=', data.get('price'))])
            #             for rate in rates:
            #                 price.update({rate.deductible: data.get('price') * rate.rate})
            #      else:
            #            rate = self.env['motor.rating.table'].search(
            #                  [('brand', '=', data.get('brand')),
            #                   ('product_id.product_name', '=', data.get('product')),
            #                   ('sum_insured_from', '<=', data.get('price')),
            #                   ('sum_insure_to', '>=', data.get('price'))])
            #            price = data.get('price') * rate.rate
            # return price

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

      @api.model
      def create_motor_ticket(self, data):
            name = 'Motor Ticket'
            type = 'motor'
            ids = self.env['product.covers'].search([('product_name', '=', data.get('product'))]).id

            ticket = self.env['quoate'].create(
                  {'name': name, 'contact_name': data.get('name'), 'phone': data.get('phone'),
                   'email_from': data.get('mail'), 'sum_insured': data.get('price'),
                   'brand': data.get('brand'), 'product_id': ids, 'ticket_type': type})
            return ticket.id

      @api.model
      def get_brands(self,data):
            print(data)
            brands = []
            for rec in self.env['car.brands'].search([]):
                  brands.append({'id': rec.id, 'title': rec.brand})
            return brands

class aropeHelpDesk(models.Model):
    _inherit = 'quoate'

    brand = fields.Char('Brand')
    product_id = fields.Many2one('product.covers')




