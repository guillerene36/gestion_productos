from odoo import models, fields

class Productos(models.Model):
    _name = 'gestion.productos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Tabla de Productos'

    # === NUEVO CAMPO DE IMAGEN ===
    imagen = fields.Binary(string="Imagen Producto", attachment=True)

    name = fields.Char(string='Nombre', required=True, tracking=True)
    tipo = fields.Selection([('bien', 'Bien'), ('servicio', 'Servicio')], string='Tipo', tracking=True)
    codigo = fields.Char(string='Codigo', required=True)
    descripcion = fields.Char(string='Descripcion')
    origen = fields.Selection([('imp', 'IMP'), ('nac', 'NAC')], string='Origen')
    cantidad_vendida = fields.Integer(string='Cantidad vendida', tracking=True)
    
    partes_ids = fields.One2many('gestion.partes', 'producto_id', string='Partes')

    unidad_negocio_ids = fields.Many2many(
        'gestion.unidad.negocio', 
        string='Unidades de Negocio',
        tracking=True
    )

    _sql_constraints = [
        ('codigo_unique', 'unique(codigo)', '¡El código del producto ya existe! Debe ser único.')
    ]
