from odoo import models, fields

class UnidadNegocio(models.Model):
    _name = 'gestion.unidad.negocio'
    _description = 'Unidad de Negocio'

    name = fields.Char(string='Nombre de la Unidad', required=True)
    descripcion = fields.Text(string='Descripción')
