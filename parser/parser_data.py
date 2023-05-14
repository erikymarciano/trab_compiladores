bnf_rules = [['<Type>', 'identifier', '(', '<ArgList>', ')', '<CompoundStmt>'],
             ['<Arg>', '<ArgList->'],
             [',', '<Arg>', '<ArgList~>'],
             ['ε'],
             ['<Type>', 'identifier'],
             ['<Type>', '<IdentList>'],
             ['int'],
             ['float'],
             ['identifier', '<IdentList~>'],
             [',', '<IdentList>'],
             ['ε'],
             ['<ForStmt>'],
             ['<WhileStmt>'],
             ['<Expr>', ';'],
             ['<IfStmt>'],
             ['<CompoundStmt>'],
             ['<Declaration>'],
             [';'],
             ['for', '(', '<Expr>', ';', '<OptExpr>', ';', '<OptExpr>', ')', '<Stmt>'],
             ['<Expr>'],
             ['ε'],
             ['while', '(', '<Expr>', ')', '<Stmt>'],
             ['if', '<Expr>', '<Stmt>', '<ElsePart>'],
             ['else', '<Stmt>'],
             ['ε'],
             ['{', '<StmtList>', '}'],
             ['<Stmt>', '<StmtList>'],
             ['ε'],
             ['identifier', '=', '<Expr>'],
             ['<Rvalue>'],
             ['<Mag>', '<Rvalue~>'],
             ['<Compare>', '<Mag>', '<Rvalue~>'],
             ['ε'],
             ['=='],
             ['<'],
             ['>'],
             ['<='],
             ['>='],
             ['!='],
             ['<Term>', '<Mag~>'],
             ['+', '<Term>', '<Mag~>'],
             ['-', '<Term>', '<Mag~>'],
             ['ε'],
             ['<Factor>', '<Term~>'],
             ['*', '<Factor>', '<Term~>'],
             ['/', '<Factor>', '<Term~>'],
             ['ε'],
             ['(', '<Expr>', ')'],
             ['-', '<Factor>'],
             ['+', '<Factor>'],
             ['identifier'],
             ['number']]

first = {
    '<Function>': ['int', 'float'],
    '<ArgList>': ['int', 'float'],
    '<ArgList~>': [','],
    '<Arg>': ['int', 'float'],
    '<Declaration>': ['int', 'float'],
    '<Type>': ['int', 'float'],
    '<IdentList>': ['identifier'],
    '<IdentList~>': [','],
    '<Stmt>': [';', 'int', 'float', '{', 'if', '(', '-', '+', 'identifier', 'number', 'while', 'for'],
    '<ForStmt>': ['for'],
    '<OptExpr>': ['(', '-', '+', 'identifier', 'number'],
    '<WhileStmt>': ['while'],
    '<IfStmt>': ['if'],
    '<ElsePart>': ['else'],
    '<CompoundStmt>': ['{'],
    '<StmtList>': [';', 'int', 'float', '{', 'if', '(', '-', '+', 'identifier', 'number', 'while', 'for'],
    '<Expr>': ['(', '-', '+', 'identifier', 'number'],
    '<Rvalue>': ['(', '-', '+', 'identifier', 'number'],
    '<Rvalue~>': ['==', '<', '>', '<=', '>=', '!='],
    '<Compare>': ['==', '<', '>', '<=', '>=', '!='],
    '<Mag>': ['(', '-', '+', 'identifier', 'number'],
    '<Mag~>': ['-', '+'],
    '<Term>': ['(', '-', '+', 'identifier', 'number'],
    '<Term~>': ['/', '*'],
    '<Factor>': ['(', '-', '+', 'identifier', 'number']
}

table = {
    '<Function>': {
        'int': [1],
        'float': [1]
    },
    '<ArgList>': {
        'int': [2],
        'float': [2]
    },
    '<ArgList~>': {
        ',': [3],
        ')': [4]
    },
    '<Arg>': {
        'int': [5],
        'float': [5]
    },
    '<Declaration>': {
        'int': [6],
        'float': [6]
    },
    '<Type>': {
        'int': [7],
        'float': [8]
    },
    '<IdentList>': {
        'identifier': [9]
    },
    '<IdentList~>': {
        ',': [10],
        ';': [11]
    },
    '<Stmt>': {
        'for': [12],
        'while': [13],
        'number': [14],
        'identifier': [14],
        '(': [14],
        '+': [14],
        '-': [14],
        'if': [15],
        '{': [16],
        'int': [17],
        'float': [17],
        ';': [18]        
    },
    '<ForStmt>': {
        'for': [19]
    },
    '<OptExpr>': {
        'number': [20],
        'identifier': [20],
        '(': [20],
        '+': [20],
        '-': [20],
        ';': [21],
        ')': [21]
    },
    '<WhileStmt>': {
        'while': [22]
    },
    '<IfStmt>': {
        'if': [23]
    },
    '<ElsePart>': {
        'else': [24,25],
        'int': [25],
        'float': [25],
        'number': [25],
        'identifier': [25],
        'if': [25],        
        'for': [25],
        'while': [25],
        ';': [25],
        '{': [25],
        '(': [25],
        '+': [25],
        '-': [25]
    },
    '<CompoundStmt>': {
        '{': [26]
    },
    '<StmtList>': {
        'int': [27],
        'float': [27],
        'number': [27],
        'identifier': [27],
        'if': [27],
        'for': [27],
        'while': [27],
        ';': [27],
        '{': [27],
        '(': [27],
        '+': [27],
        '-': [27]
    },
    '<Expr>': {
        'identifier': [29,30],
        'number': [30],        
        '(': [30],
        '+': [30],
        '-': [30]
    },
    '<Rvalue>': {
        'number': [31],
        'identifier': [31],
        '(': [31],
        '+': [31],
        '-': [31]
    },
    '<Rvalue~>': {        
        '==': [32],
        '!=': [32],
        '<': [32],
        '>': [32],
        '<=': [32],
        '>=': [32],
        ';': [33],
        ')': [33],
    },
    '<Compare>': {
        '==': [34],
        '<': [35],
        '>': [36],
        '<=': [37],
        '>=': [38],
        '!=': [39]        
    },
    '<Mag>': {
        'number': [40],
        'identifier': [40],
        '(': [40],
        '+': [40],
        '-': [40]
    },
    '<Mag~>': {        
        '+': [41],
        '-': [42],
        ';': [43],
        '==': [43],
        '!=': [43],
        '<': [43],
        '>': [43],
        '<=': [43],
        '>=': [43],
        ')': [43]
    },
    '<Term>': {
        'number': [44],
        'identifier': [44],
        '(': [44],
        '+': [44],
        '-': [44]
    },
    '<Term~>': {
        '*': [45],
        '/': [46],
        ',': [47],
        '+': [47],
        '-': [47],
        '==': [47],
        '!=': [47],
        '<': [47],
        '>': [47],
        '<=': [47],
        '>=': [47],
        ')': [47]
    },
    '<Factor>': {
        '(': [48],
        '-': [49],
        '+': [50],
        'identifier': [51],
        'number': [52]
    },
}

terminals = [
    'int',
    'float',
    'number',
    'identifier',
    'if',
    'else',
    'for',
    'while',
    ',',
    ';'
    '{',
    '(',
    '+',
    '-',
    '/',
    '*',
    '==',
    '!=',
    '<',
    '>',
    '<=',
    '>=',
    ')',
    '}'
]