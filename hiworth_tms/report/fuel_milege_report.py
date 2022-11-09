from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta



class VehicleMileAgeReport(models.TransientModel):
    _name = 'vehicle.mileage.wizard1'

    project = fields.Many2one('project.project', 'Project')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    @api.multi
    def action_vehicle_mileage_open_window(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }

        return {
            'name': 'Vehicle Mileage Report',
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_tms.report_fleet_vehicle_mileage_template_new',
            'datas': datas,
            'report_type': 'qweb-pdf'
        }

    @api.multi
    def get_details(self):
        d1 = self.date_from
        d2 = self.date_to
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        lst = []
        if self.vehicle_id:
            if self.project:
                driver_stmts = self.env['driver.daily.statement'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                     ('vehicle_no', '=', self.vehicle_id.id), ('project_id', '=', self.project.id)])
                print("vehicle and project exist..................")
            else:
                driver_stmts = self.env['driver.daily.statement'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                     ('vehicle_no', '=', self.vehicle_id.id)])
                print("vehicle and project not  exist..................")

        else:
            if self.project:
                driver_stmts = self.env['driver.daily.statement'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                     ('project_id', '=', self.project.id)])
                print("vehicle and project exist..................")
            else:
                driver_stmts = self.env['driver.daily.statement'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        date_list = []
        curr_date = d1
        end_date = d2
        while curr_date <= end_date:
            date_list.append(curr_date)
            curr_date += timedelta(days=1)
        for rec in driver_stmts:
                if rec.vehicle_no.is_a_mach:
                    if rec.driver_stmt_line:
                        if rec.diesel_pump_line:
                            for line in rec.diesel_pump_line:
                                litre = line.litre
                            for line in rec.driver_stmt_line:
                                if line.total_km == 0:
                                    pass
                                else:
                                    mileage = round((litre / line.total_km),2)
                                    vals = {
                                        'date': rec.date,
                                        'reg_no': rec.vehicle_no.name,
                                        'veh_id': rec.vehicle_no.id,
                                        'owner': rec.vehicle_no.vehicle_under.name,
                                        'type': rec.vehicle_no.model_id.name,
                                        'project': rec.project_id.name,
                                        'mileage': mileage,
                                        'unit': " Lt/Hr"

                                    }
                                    lst.append(vals)


                else:
                    if rec.diesel_pump_line:
                        for line in rec.diesel_pump_line:
                            if line.litre == 0:
                                pass
                            else:
                                mileage = round((line.total_odometer/line.litre),2)
                                vals = {
                                    'date': rec.date,
                                    'reg_no': rec.vehicle_no.name,
                                    'veh_id': rec.vehicle_no.id,
                                    'owner': rec.vehicle_no.vehicle_under.name,
                                    'type': rec.vehicle_no.model_id.name,
                                    'project': rec.project_id.name,
                                    'mileage': mileage,
                                    'unit': " Km/Lt"
                                }
                                lst.append(vals)
        return lst
