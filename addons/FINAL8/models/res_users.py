from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    unidad_negocio_ids = fields.Many2many(
        'gestion.unidad.negocio',
        'res_users_unidad_negocio_rel_v2',  # <--- CAMBIAMOS ESTO (agregamos _v2)
        'user_id',
        'unidad_id',
        string='Unidades de Negocio Permitidas',
        help='El usuario solo podrá ver productos asociados a estas unidades.'
    )
