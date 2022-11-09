from openerp import models, fields, api, _
from openerp import tools, _
from datetime import datetime, date, timedelta


class VehicleSparePartsWizard(models.TransientModel):
    _name = 'vehicle.spare.wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    @api.multi
    def action_vehicle_spare_open_window(self):
        datas = {
            'ids': self._ids,
            'model': self._name,
            'form': self.read(),
            'context': self._context,
        }

        return {
            'name': 'All Vehicle Spare Parts Expense Report',
            'type': 'ir.actions.report.xml',
            'report_name': 'hiworth_tms.report_fleet_vehicle_spare_template',
            'datas': datas,
            'report_type': 'qweb-pdf'
        }

    @api.multi
    def get_details(self):
        lst = []
        vehicles = self.env['fleet.vehicle.log.services'].search([])
        if vehicles:
            print("found........................................")
        else :
            print("not found..............................")
        for vid in vehicles:
            for lines in vid.cost_ids:
                total = 0

                print("date in record",lines.date1)
                print("date from",self.date_from)
                print("date to",self.date_to)
                if (vid.date_repair >= self.date_from):
                    if(vid.date_repair <= self.date_to):
                        x = datetime.strptime(vid.date_repair, '%Y-%m-%d')
                        y=x.strftime('%d-%m-%Y').upper()
                        p=datetime.strptime(lines.date_of_repair, '%Y-%m-%d')
                        q=p.strftime('%d-%m-%Y').upper()


                        vals = {
                            'date':y,
                            'date_invoice':q,
                            'vehicle_no':lines.vehicle_id.name,
                            'vehicle_model' :lines.vehicle_id.vehicle_categ_id.name,
                            'invoice':vid.inv_ref,
                            'vendor':vid.vendor_id.name,
                            'parts_change':lines.new_parts_name,
                            'total_amt':lines.total_amount,
                            'sub_total':0,

                        }
                        lst.append(vals)
                for vals in lst:
                    total = total + vals['total_amt']
                for vals in lst:
                    vals['sub_total'] = total

        return lst
