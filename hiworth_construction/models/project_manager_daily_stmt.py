from openerp import fields, models, api
import datetime
from openerp.exceptions import Warning as UserError
from openerp.osv import osv
from openerp.tools.translate import _
from dateutil import relativedelta
from openerp.exceptions import except_orm, ValidationError
import math

class PmWork(models.Model):
    _name = 'pm.works'


    projectname_id = fields.Many2one('project.project', 'Project')
    supervisor_id = fields.Many2one('res.partner', 'Supervisor')
    # work_planned = fields.Many2one('task.line','Work Planned')
    work_planned = fields.Many2one('task.line','Work planned')
    work_planned1 = fields.Many2one('budget.planning.chart.line','Work planned')
    name_subcontractor = fields.Many2one('res.partner','Subcontractor')
    work_id = fields.Many2one('pm.daily.statement','Work Details')
    material = fields.Many2many('product.product',string='Materials')
    veh_categ_id = fields.Many2many('fleet.vehicle',
                                    string='Machinery')
    no_labours = fields.Integer()
    work_done = fields.Many2one('task.line','Work Planned')
    work_status = fields.Char('Work Status')

    delay_reason = fields.Char('Reason For Delay')
    remarks = fields.Char('Remarks')



class PmDailyStatement(models.Model):
    _name = 'pm.daily.statement'
    _rec_name = 'partner_id'

    # name = fields.Char('Name')
    partner_id = fields.Many2one('res.partner','Name')
    date = fields.Date('Date')
    project_id = fields.Many2one('project.project','Project')
    pm_work_ids = fields.One2many(
        comodel_name='pm.works',
        inverse_name='work_id',
        string='Daily Statements',
        store=True,
    )

