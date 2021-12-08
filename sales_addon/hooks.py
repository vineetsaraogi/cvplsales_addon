from . import __version__ as app_version

app_name = "sales_addon"
app_title = "Sales Addon"
app_publisher = "Raj Tailor"
app_description = "Customize feature of sales module in erpnext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "raaj@akhilaminc.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sales_addon/css/sales_addon.css"
# app_include_js = "/assets/sales_addon/js/sales_addon.js"

# include js, css files in header of web template
# web_include_css = "/assets/sales_addon/css/sales_addon.css"
# web_include_js = "/assets/sales_addon/js/sales_addon.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sales_addon/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Sales Order": ["sales_addon/custom_doctype/sales_order/sales_order.js"],
	"Item": ["custom_script/item.js"],
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sales_addon.install.before_install"
# after_install = "sales_addon.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sales_addon.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Order" :{
		"validate": "sales_addon.sales_addon.custom_doctype.sales_order.sales_order.validate"	
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sales_addon.tasks.all"
# 	],
# 	"daily": [
# 		"sales_addon.tasks.daily"
# 	],
# 	"hourly": [
# 		"sales_addon.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sales_addon.tasks.weekly"
# 	]
# 	"monthly": [
# 		"sales_addon.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "sales_addon.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sales_addon.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sales_addon.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sales_addon.auth.validate"
# ]

