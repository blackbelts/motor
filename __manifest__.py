# -*- coding: utf-8 -*-
{
    'name': "Arope Motor",
    'summary': """Arope Motor""",
    'description': """Motor """,
    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'plat',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','helpdesk_inherit'],

    # always loaded
    'data': [
        # 'security/security.xml',
        
        'views/setup.xml',
        'views/arope_helpdesk.xml',
        'views/menu_item.xml',
	'security/ir.model.access.csv',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
