from odoo import models, fields

class Partes(models.Model):
    _name = 'gestion.partes'
    _description = 'Tabla de Partes'

    # === NUEVO CAMPO DE IMAGEN ===
    imagen = fields.Binary(string="Imagen Parte", attachment=True)

    name = fields.Char(string='Name', required=True)
    producto_id = fields.Many2one('gestion.productos', string='Producto Relacionado')
