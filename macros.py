commands = [
	{
		'cmd': 'nat',
		'code': '',
		'params': 1
	},
	{	
		'cmd': 'set',
		'code': '[-]',
		'params': 1
	},
	{
		'cmd': 'str',
		'code': '[-]',
		'params': 1
	},
	{
		'cmd': 'mov',
		'code': '*[-]*[-*+*]',
		'params': 2
	},
	{
		'cmd': 'copy',
		'code': '*[-]>[-]<*[-*+>+<*]*>[-<*+>*]',
		'params': 2
	},
	{	
		'cmd': 'add',
		'code': '[->+<]'
	},
	{	
		'cmd': 'sub',
		'code': '[->-<]'
	},
	{
		'cmd': 'mul',
		'code': '[->[->+>+<<]>>[-<<+>>]<<<]'
	},
	{
		'cmd': 'left',
		'code': '',
		'params': 1
	},
	{
		'cmd': 'right',
		'code': '',
		'params': 1
	},
	{	
		'cmd': 'leftN',
		'code': '[<]'
	},
	{
		'cmd': 'rightN',
		'code': '[>]'
	},
	{	
		'cmd': 'cpr',
		'code': '>[-]<[->+<]'
	},
	{
		'cmd': 'toDigit',
		'code': '++++++++++++++++++++++++++++++++++++++++++++++++'
	},
	{
		'cmd': 'fromDigit',
		'code': '------------------------------------------------'
	},
	{
		'cmd': 'out',
		'code': '.'
	},
	{	
		'cmd': 'print',
		'code': '[.>]'
	},
	{
		'cmd': 'if',
		'code': ''
	},
	{
		'cmd': 'endif',
		'code': '[-]]'
	}
]