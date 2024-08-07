from typing import Self

class Symbol(object):
    def __init__(self, name, type=None) -> None:
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    def __init__(self, name, type=None) -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    __repr__ = __str__

class ParamSymbol(Symbol):
    def __init__(self, name, type=None):
        super().__init__(name, type)

    def __str__(self):
        return "<{class_name}(name='{name}', type='{type}')>".format(
            class_name=self.__class__.__name__,
            name=self.name,
            type=self.type,
        )

    __repr__ = __str__

class FunctionSymbol(Symbol):
    def __init__(self, name, formal_params: list[ParamSymbol]=[]) -> None:
        super(FunctionSymbol,self).__init__(name)

        self.formal_params = formal_params
        self.expr_ast = None

    def __str__(self) -> str:
        return '<{class_name}(name={name}, parameters={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.formal_params,
        )

    __repr__ = __str__

class LambdaSymbol(Symbol):
    def __init__(self, name: str, param: ParamSymbol = None) -> None:
        super(LambdaSymbol,self).__init__(name)

        self.param = param
        self.expr_ast = None

    def __str__(self) -> str:
        return '<{class_name}(name={name}, parameter={params})>'.format(
            class_name=self.__class__.__name__,
            name=self.name,
            params=self.param,
        )

    __repr__ = __str__

class ScopedSymbolTable(object):
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

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
            ('Scope name', self.scope_name),
            ('Scope level', self.scope_level),
            ('Enclosing scope',
             self.enclosing_scope.scope_name if self.enclosing_scope else None
            )
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s
    
    __repr__ = __str__

    def insert(self, symbol: Symbol) -> None:
        """ Insert a symbol into the symbol table."""
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str, current_scope_only: bool = False) -> Symbol | None:
        """
        Look up a symbol by name in the symbol table recursively.

        :param name: name of the symbol to look up.
        :type name: str
        :param current_scope_only: limit the lookup to the current symbol table only.
        :type current_scope_only: bool
        :return: Symbol from the symbol table or None
        :rtype: Symbol | None
        """
        symbol = self._symbols.get(name, None)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)