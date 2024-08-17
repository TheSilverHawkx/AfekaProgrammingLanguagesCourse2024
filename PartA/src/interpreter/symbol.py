from typing import Self
from abc import ABCMeta

class Symbol(object):
    """Represents a general symbol in the symbol table.

    Symbols can represent variables, types, functions, etc. within
    the scope of a program. In the current project - it represents functions.

    Attributes:
        name (str): The name of the symbol.
        type (optional): The type of the symbol, if applicable.

    Usage:
        symbol = Symbol(name='x', type='INTEGER')
    """
    def __init__(self, name, type: Self=None) -> None:
        self.name = name
        self.type = type
    
    def __str__(self):
        return "{class_name}(name={symbol_name}{optional_type})".format(
            class_name=self.__class__.__name__,
            symbol_name= self.name,
            optional_type=f", type={self.type}" if self.type is not None else ""
        )

    def __repr__(self) -> str:
        return self.__str__()

class BuiltinTypeSymbol(Symbol):
    """Represents a built-in type symbol in the symbol table.

    Built-in types are predefined types such as INTEGER and BOOLEAN.

    Attributes:
        name (str): The name of the built-in type.

    Usage::

        int_type = BuiltinTypeSymbol(name='INTEGER')
    """
    def __init__(self, name, type=None) -> None:
        super().__init__(name)

class ParamSymbol(Symbol):
    """Represents a parameter symbol in the symbol table.

    Parameters are used within function or method declarations.

    Attributes:
        name (str): The name of the parameter.
        type (optional): The type of the parameter, if applicable.

    Usage:
        param = ParamSymbol(name='x', type='INTEGER')
    """
    def __init__(self, name: str, type=BuiltinTypeSymbol):
        super().__init__(name, type)

class CallableSymbol(Symbol):
    """Represents a function / Lambda symbol in the symbol table.

    Function symbols include information about the function, such as:
    name, its formal parameters, and the associated expression AST node.

    Attributes:
        name (str): The name of the function.
        formal_params (list[ParamSymbol]): The list of parameters for the function.
        expr_ast (AST): The AST node representing the function's body.

    Usage:
        param1 = Param(token=param_token1)
        param2 = Param(token=param_token2)
        func_symbol = FunctionSymbol(name='foo', formal_params=[param1, param2])
    """
    def __init__(self, name, formal_params: list[ParamSymbol]=None) -> None:
        super().__init__(name)

        self.formal_params = [] if formal_params is None else formal_params
        self.expr_ast = None

    def __str__(self) -> str:
        params_str = ", ".join(param.name for param in self.formal_params)
        result = f"{self.__class__.__name__}(name={self.name}, parameters=[{params_str}])"
                
        return result

class ScopedSymbolTable(object):
    """Represents a scoped symbol table for tracking symbols in various scopes.

    This symbol table supports nested scopes and allows insertion, lookup, 
    and initialization of built-in types.

    Attributes:
        scope_name (str): The name of the scope.
        scope_level (int): The level of the scope (e.g., global scope might be level 1).
        enclosing_scope (Self): The parent scope that encloses this scope. Default is None

    Usage:
        global_scope = ScopedSymbolTable(scope_name='global', scope_level=1)
        global_scope._init_builtins()
    """
    def __init__(
            self,
            scope_name: str,
            scope_level: int,
            enclosing_scope: Self = None
    ):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope

    def _init_builtins(self):
        """ Initialize built-in data types """
        self.insert(BuiltinTypeSymbol('INTEGER'))
        self.insert(BuiltinTypeSymbol('BOOLEAN'))
        self.insert(BuiltinTypeSymbol('FUNCTION'))

    def __str__(self):
        s  = [f'{"Symbols Table":=^30}']
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
             self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            s.append(f'{header_name:<15}: {header_value}')

        if len(self._symbols) > 0:
            longest_key = max(len(x) for x in self._symbols.keys())
            s.append('Symbols:')
            s.extend([f'{k:>{longest_key}}: {str(v)}' for k,v in self._symbols.items() ])
            
        s.append('-'*30)
        return '\n'.join(s)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.scope_name},level={self.scope_level}, enclosing_scope={self.enclosing_scope.scope_name})"

    def insert(self, symbol: Symbol) -> None:
        """
        Inserts a symbol into the symbol table.

        Args:
            symbol (Symbol): The symbol to be inserted into the table.

        Usage:
            int_symbol = BuiltinTypeSymbol('INTEGER'))
            symbol_table.insert(int_symbol)
        """
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str, current_scope_only: bool = False) -> Symbol | None:
        """
        Looks up a symbol by name in the symbol table.

        This method searches for the symbol in the current scope and, 
        if not found, recursively searches in enclosing scopes unless 
        `current_scope_only` is set to True.

        Args:
            name (str): The name of the symbol to look up.
            current_scope_only (bool, optional): If True, limits the lookup to the current scope only.

        Returns:
            Symbol | None: The symbol if found, otherwise None.
        """
        symbol = self._symbols.get(name, None)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)