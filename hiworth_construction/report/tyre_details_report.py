from openerp import fields, models, api, _
from datetime import datetime


class VehicleTyreReport(models.TransientModel):
    _name = "vehicle.tyre.report.wizard"

    tyre_id = fields.Many2one('vehicle.tyre')
    from_date = fields.Date()
    to_date = fields.Date()
    include_retreading = fields.Boolean()

    @api.multi
    def view_vehicle_tyre_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_construction.report_vehicle_tyre_report_template',
            'datas': datas,
            'report_type': 'qweb-html',
        }

    @api.multi
    def print_vehicle_tyre_report(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_construction.report_vehicle_tyre_report_template',
            'datas': datas,
            'report_type': 'qweb-pdf',
            #
        }

    @api.model
    def get_vehicle_tyre_details(self):
        res = self.tyre_id
        domain = []
        if not self.tyre_id:
            if self.from_date:
                domain = [('purchase_date', '>=', self.from_date)]
            if self.to_date:
                domain = [('purchase_date', '<=', self.to_date)]
            res = self.env['vehicle.tyre'].search(domain)
        return res
