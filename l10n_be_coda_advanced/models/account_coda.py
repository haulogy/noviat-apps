# Copyright 2009-2023 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountCoda(models.Model):
    _name = "account.coda"
    _description = "Object to store CODA Data Files"
    _order = "coda_creation_date desc"

    name = fields.Char(string="CODA Filename", readonly=True)
    coda_data = fields.Binary(string="CODA File", readonly=True)
    bank_statement_ids = fields.One2many(
        comodel_name="account.bank.statement",
        inverse_name="coda_id",
        string="Generated Bank Statements",
        readonly=True,
    )
    bank_statement_count = fields.Integer(
        compute="_compute_bank_statement_count", string="# of Bank Statements"
    )
    note = fields.Text(string="Import Log", readonly=True)
    coda_creation_date = fields.Date(string="CODA Creation Date", readonly=True)
    date = fields.Date(
        string="Import Date",
        default=lambda self: fields.Date.context_today(self),
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        default=lambda self: self.env.user,
        readonly=True,
    )
    state = fields.Selection(
        selection=[("draft", "Draft"), ("done", "Done")],
        default="done",
        required=True,
        readonly=True,
    )
    company_ids = fields.Many2many(
        comodel_name="res.company",
        string="Companies",
        readonly=True,
        help="A single CODA File can contain statements from multiple "
        "companies. This field shows all companies for which statements "
        "have been created.",
    )

    _sql_constraints = [
        (
            "coda_uniq",
            "unique (name, coda_creation_date)",
            "This CODA has already been imported !",
        )
    ]

    def _compute_bank_statement_count(self):
        for coda in self:
            coda.bank_statement_count = len(coda.bank_statement_ids)

    def unlink(self):
        for coda in self:
            if coda.state != "draft":
                raise UserError(
                    _("Only CODA File objects in state" " 'draft' can be deleted !")
                )
            coda.bank_statement_ids.unlink()
        return super().unlink()

    def set_to_draft(self):
        for rec in self:
            rec.state = "draft"
            if not rec.bank_statement_ids:
                rec.note = False

    def process(self):
        self.ensure_one()
        wiz_vals = {"coda_data": self.coda_data, "coda_fname": self.name}
        wizard = self.env["account.coda.import"].create(wiz_vals)
        module = __name__.split("addons.")[1].split(".")[0]
        wiz_view = self.env.ref("%s.account_coda_import_view_form_process" % module)
        return {
            "name": _("Process CODA File"),
            "res_id": wizard.id,
            "view_type": "form",
            "view_mode": "form",
            "res_model": wizard._name,
            "view_id": wiz_view.id,
            "target": "new",
            "context": dict(self.env.context, coda_id=self.id),
            "type": "ir.actions.act_window",
        }
