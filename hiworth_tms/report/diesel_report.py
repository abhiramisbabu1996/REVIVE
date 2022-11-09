from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta


class VehicleSparePartsWizard(models.TransientModel):
    _name = 'vehicle.diesel.wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    vehicle_id = fields.Many2one('fleet.vehicle','Vehicle')

    @api.multi
    def action_vehicle_diesel_open_window(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }

        return {
            'name': 'All Vehicle Diesel Infomation-Expense Report',
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_tms.report_fleet_vehicle_diesel_template',
            'datas': datas,
            'report_type': 'qweb-pdf'
        }

    @api.multi
    def get_details(self):
        if self.vehicle_id:
            vehicle_obj = self.env['driver.daily.statement'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to),('vehicle_no', '=', self.vehicle_id.id)])

        else:
            vehicle_obj = self.env['driver.daily.statement'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to)])

        vehicle_det = []
        vehicle_lst = []
        for vehicles in vehicle_obj:
            item = vehicles.vehicle_no

            if item not in vehicle_lst:
                if item:
                    vehicle_vals = ({
                        # 'date': vehicles.date,
                        'vehicle_id': vehicles.vehicle_no.name,
                        'vehicle_model': vehicles.vehicle_no.model_id.name,
                        'diesel_ltr': vehicles.diesel_pump_line.litre,
                        'diesel_price': vehicles.diesel_pump_line.total_litre_amount,
                        'total_km': vehicles.diesel_pump_line.total_odometer,
                    })
                    vehicle_det.append(vehicle_vals)
                    vehicle_lst.append(vehicles.vehicle_no)
            else:
                item_copy = vehicles.vehicle_no.name
                for dicts in vehicle_det:
                    if item_copy== dicts['vehicle_id']:
                        old_ltr = dicts['diesel_ltr']
                        new_ltr = old_ltr + vehicles.diesel_pump_line.litre
                        dicts['diesel_ltr'] = new_ltr

                        old_price = dicts['diesel_price']
                        new_price = old_price + vehicles.diesel_pump_line.total_litre_amount
                        dicts['diesel_price'] = new_price

                        old_km = dicts['total_km']
                        new_km = old_km + vehicles.diesel_pump_line.total_odometer
                        dicts['total_km'] = new_km
        return vehicle_det