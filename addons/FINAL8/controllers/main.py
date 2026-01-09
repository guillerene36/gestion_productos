from odoo import http
from odoo.http import request
import json
import base64

class PruebaController(http.Controller):

    # --- RUTA DE PRUEBA (Sin Autenticacion) ---
    # Fíjate que @http y def están alineados a 4 espacios
    @http.route('/final8/ping', type='http', auth='none', csrf=False)
    def ping_final(self):
        return "<h1>¡SI VES ESTO, FUNCIONA!</h1>"

    # --- RUTA DEL REPORTE ---
    @http.route('/final8/reporte', type='http', auth='public', csrf=False)
    def reporte_final(self, **kw):
        datos = request.get_json_data()
        if not datos: 
            return "Error: Sin JSON"
            
        pdf, _ = request.env['ir.actions.report']._sudo()._render_qweb_pdf(
            'FINAL8.reporte_diccionario_template', 
            res_ids=[], 
            data={'mis_datos': datos}
        )
        return request.make_response(
            base64.b64encode(pdf),
            headers=[('Content-Type', 'text/plain')]
        )
