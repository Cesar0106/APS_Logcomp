from abc import abstractmethod
import sys

class PrePro:
    def filter(code):
        lines = code.split('\n')
        filtered_lines = []
        
        for line in lines:
            stripped_line = line.strip()

            if not stripped_line:
                continue
            
            elif stripped_line.startswith('//'):
                continue
            
            i = 0
            while i < len(line) - 1:
                if line[i] == '/' and line[i+1] == '/':
                    line = line[:i]
                i += 1
            filtered_lines.append(line)
                    
        clean_code = '\n'.join(filtered_lines) + '\n'
        return clean_code

    
class Node():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass


class IntVal(Node):
    def evaluate(self, st):
        return ("entier", self.value)

class StringVal(Node):
    def evaluate(self, st):
        return ("chaine", self.value)
    
class NoOp(Node):
    def evaluate(self, st):
        pass

class BinOp(Node):
    def evaluate(self, st):
        fils_gauche = self.children[0].evaluate(st)
        fils_droite = self.children[1].evaluate(st)
        if self.value == '+' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return ("entier", fils_gauche[1] + fils_droite[1])
        elif self.value == '-' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return ("entier", fils_gauche[1] - fils_droite[1])
        elif self.value == '*' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return ("entier", fils_gauche[1] * fils_droite[1])
        elif self.value == '/' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return ("entier", fils_gauche[1] // fils_droite[1])
        elif self.value == '==' and fils_gauche[0] == fils_droite[0]:
            return ("entier", int(fils_gauche[1] == fils_droite[1]))
        elif self.value == '>' and fils_gauche[0] == fils_droite[0]:
            return ("entier", int(fils_gauche[1] > fils_droite[1]))
        elif self.value == '<' and fils_gauche[0] == fils_droite[0]:
            return ("entier", int(fils_gauche[1] < fils_droite[1]))
        elif self.value == '&&' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return ("entier", int(fils_gauche[1] and fils_droite[1]))
        elif self.value == '||' and fils_gauche[0] == fils_droite[0] and fils_gauche[0] == "entier":
            return (int, int(fils_gauche[1] or fils_droite[1]))
        elif self.value == '.':
            return ("chaine", str(fils_gauche[1]) + str(fils_droite[1]))

class UnOp(Node):
    def evaluate(self, st):
        fils= self.children[0].evaluate(st)
        if self.value == "+" and fils[0] == "entier":
            return ("entier", fils[1])
        elif self.value == "-" and fils[0] == "entier":
            return ("entier", -fils[1])
        elif self.value == "!" and fils[0] == "entier":
            return ("entier", int(not fils[1]))
        
class Identifiant(Node):
    def evaluate(self, st):
        return st.get(self.value)
    
class Print(Node):
    def evaluate(self, st):
        print(self.children[0].evaluate(st)[1])

class For(Node):
    def evaluate(self, st):
        self.children[0].evaluate(st)
        while self.children[1].evaluate(st)[1]:
            self.children[3].evaluate(st)
            self.children[2].evaluate(st)

class If(Node):
    def evaluate(self, st):
        if self.children[0].evaluate(st):
            self.children[1].evaluate(st)
        elif len(self.children) == 3:
            self.children[2].evaluate(st)


class Bloc(Node):
    def evaluate(self, st):
        for child in self.children:
            child.evaluate(st)

class Assingnment(Node):
    def evaluate(self, st):
        children = self.children[1].evaluate(st)
        st.set(self.children[0].value, children)

class VarDec(Node):
    def evaluate(self, st):
        if len(self.children) == 2:
            st.create(self.children[0].value, self.value)
            st.set(self.children[0].value, self.children[1].evaluate(st))
        else:
            st.create(self.children[0].value, self.value)

class SymbolTable():
    
    symbol_table = {}

    def get(self, identifier):
        if identifier in self.symbol_table:
            return self.symbol_table[identifier]
        else:
            raise TypeError("Variavel")
        
    def set(self, identifier, value):
        if value[0] == self.symbol_table[identifier][0]:
            if identifier in self.symbol_table:
                self.symbol_table[identifier] = value
            else:
                raise TypeError("Variavel")
        else:
            raise TypeError("Erro de tipo")
    
    def  create(self, identifier, type):
        if identifier in self.symbol_table:
            raise TypeError("Variavel")
        else:
            self.symbol_table[identifier] = (type, None)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:

    RESERVED = ["affiche", "si", "sinon", "pour", "var", "entier", "chaine"]
    
    def __init__(self, source : str):
        self.source = source
        self.position = 0
        self.next = None
    
    def select_next(self):

            if self.position == len(self.source):
                self.next = Token("EOF", "")

            elif self.source[self.position].isdigit():
                numero = ""
                while  self.position < len(self.source) and self.source[self.position].isdigit():
                    numero += self.source[self.position]
                    self.position += 1
                self.next = Token("ENTIER", int(numero))
            
            elif self.source[self.position] == "+":
                self.next = Token("PLUS", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "-":
                self.next = Token("MINUS", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "*":
                self.next = Token("MULT", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "/":
                self.next = Token("DIV", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "(":
                self.next = Token("ABRE_PARENTESIS", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == ")":
                self.next = Token("FECHA_PARENTESIS", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "#":
                self.next = Token("HASHTAG", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "=":
                if self.source[self.position+1] == "=":
                    self.next = Token("COMPARE", "==")
                    self.position += 2
                else:
                    self.next = Token("EQUAL", self.source[self.position])
                    self.position += 1
            
            elif self.source[self.position] == "\n":
                self.next = Token("BREAKLINE", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == ";":
                self.next = Token("PONTO_VIRGULA", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == "|":
                if self.source[self.position+1] == "|":
                    self.next = Token("OU", "||")
                    self.position += 2
                else:
                    raise ValueError(f"Erro na linha {self.position}")
            
            elif self.source[self.position] == "&":
                if self.source[self.position+1] == "&":
                    self.next = Token("ET", "&&")
                    self.position += 2
                else:
                    raise ValueError(f"Erro na linha {self.position}")
                
            elif self.source[self.position] == "!":
                self.next = Token("NOT", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == ">":
                self.next = Token("MAIOR", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "<":
                self.next = Token("MENOR", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "{":
                self.next = Token("ABRE_CHAVES", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == "}":
                self.next = Token("FECHA_CHAVES", self.source[self.position])
                self.position += 1
            
            elif self.source[self.position] == ".":
                self.next = Token("CONCATENA", self.source[self.position])
                self.position += 1

            elif self.source[self.position] == '"':
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != '"':
                    string += self.source[self.position]
                    self.position += 1
                if self.source[self.position] == '"':
                    self.position += 1
                    self.next = Token("CHAINE", string)
                else:
                    raise ValueError(f"Erro na linha {self.position}")
                
            elif self.source[self.position].isalpha():
                identificador = ""
                while  self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    identificador += self.source[self.position]
                    self.position += 1
                
                if identificador in Tokenizer.RESERVED:
                    if(identificador == "affiche" ):
                        self.next = Token("AFFICHE", self.source[self.position])
                    elif(identificador == "si"):
                        self.next = Token("SI", self.source[self.position])
                    elif(identificador == "sinon"):
                        self.next = Token("SINON", self.source[self.position])
                    elif(identificador == "pour"):
                        self.next = Token("POUR", self.source[self.position])
                    elif(identificador == "var"):
                        self.next = Token("VAR", self.source[self.position])
                    elif(identificador == "entier"):
                        self.next = Token("TYPE", "entier")
                    elif(identificador == "chaine"):
                        self.next = Token("TYPE", "chaine")
                else:
                    self.next = Token("IDENTIFIANT", identificador)

            elif self.source[self.position].isspace():
                self.position += 1
                self.select_next()
            
            else:
                raise ValueError(f"Erro na linha {self.position}")


class Parser:
    
    tokenizer = None

    def parse_program():
        resultado = Bloc("Bloc", [])
        while Parser.tokenizer.next.type != "EOF":
            resultado.children.append(Parser.parse_statement())
        return resultado
    
    def parse_statement():

        resultado = None

        if Parser.tokenizer.next.type == "BREAKLINE":
            Parser.tokenizer.select_next()
            return NoOp("NoOp", [])
        
        elif Parser.tokenizer.next.type == "IDENTIFIANT":
            identificador = Identifiant(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.select_next()
                resultado = Assingnment("=", [identificador, Parser.parse_bool_expression()])
                if Parser.tokenizer.next.type == "BREAKLINE":
                    Parser.tokenizer.select_next()
                    return resultado
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro") 
        
        elif Parser.tokenizer.next.type == "AFFICHE":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "HASHTAG":
                Parser.tokenizer.select_next()
                resultado = Print("Affiche", [Parser.parse_bool_expression()])
                if Parser.tokenizer.next.type == "HASHTAG":
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.select_next()
                        return resultado
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")
        
        elif Parser.tokenizer.next.type == "SI":
            Parser.tokenizer.select_next()
            resultado = If("si", [Parser.parse_bool_expression()])
            resultado.children.append(Parser.parse_block())
            if Parser.tokenizer.next.type == "SINON":
                Parser.tokenizer.select_next()
                resultado.children.append(Parser.parse_block())
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Erro")
        
        elif Parser.tokenizer.next.type == "POUR":
            Parser.tokenizer.select_next()
            resultado = For("pour", [Parser.parse_assingnment()])
            if Parser.tokenizer.next.type == "PONTO_VIRGULA":
                Parser.tokenizer.select_next()
                resultado.children.append(Parser.parse_bool_expression())
                if Parser.tokenizer.next.type == "PONTO_VIRGULA":
                    Parser.tokenizer.select_next()
                    resultado.children.append(Parser.parse_assingnment())
                    resultado.children.append(Parser.parse_block())
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.select_next()
                        return resultado
                    else:
                        raise TypeError("Erro")
                else:
                    raise TypeError("Erro")
            else:
                raise TypeError("Erro")

        elif Parser.tokenizer.next.type == "VAR":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "IDENTIFIANT":
                identificador = Identifiant(Parser.tokenizer.next.value, [])
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "TYPE":
                    tipo = Parser.tokenizer.next.value
                    resultado = VarDec(tipo, [identificador])
                    Parser.tokenizer.select_next()
                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.select_next()
                        resultado.children.append(Parser.parse_bool_expression())
                    if Parser.tokenizer.next.type == "BREAKLINE":
                        Parser.tokenizer.select_next()
                        return resultado
                    else:
                        raise TypeError("Erro")

                else:
                    raise TypeError("Erro")

            
        else:
            raise TypeError("Erro")
        
    
    def parse_assingnment():

        if Parser.tokenizer.next.type == "IDENTIFIANT":
            identificador = Identifiant(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.select_next()
                resultado = Assingnment("=", [identificador, Parser.parse_bool_expression()])
                return resultado
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")

        
    def parse_block():
        resultado = Bloc("Bloc", [])
        if Parser.tokenizer.next.type == "ABRE_CHAVES":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "BREAKLINE":
                Parser.tokenizer.select_next()
                while Parser.tokenizer.next.type != "FECHA_CHAVES":
                    resultado.children.append(Parser.parse_statement())
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
        
    def parse_bool_expression():
        resultado = Parser.parse_bool_term()

        while Parser.tokenizer.next.type == "OU":
            Parser.tokenizer.select_next()
            resultado = BinOp("||", [resultado, Parser.parse_bool_term()])

        return resultado

    def parse_bool_term():
        resultado = Parser.parse_rel_expression()

        while Parser.tokenizer.next.type == "ET":
            Parser.tokenizer.select_next()
            resultado = BinOp("&&", [resultado, Parser.parse_rel_expression()])
        return resultado


    def parse_rel_expression():

        resultado = Parser.parse_expression()

        while Parser.tokenizer.next.type == "MAIOR" or Parser.tokenizer.next.type == "MENOR" or Parser.tokenizer.next.type == "COMPARE":
            if Parser.tokenizer.next.type == "MAIOR":
                Parser.tokenizer.select_next()
                resultado = BinOp(">", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "MENOR":
                Parser.tokenizer.select_next()
                resultado = BinOp("<", [resultado, Parser.parse_expression()])
            elif Parser.tokenizer.next.type == "COMPARE":
                Parser.tokenizer.select_next()
                resultado = BinOp("==", [resultado, Parser.parse_expression()])

        return resultado
    
    def parse_expression():

        resultado = Parser.parse_term()

        while Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "CONCATENA":
            if Parser.tokenizer.next.type == "PLUS":
                Parser.tokenizer.select_next()
                resultado = BinOp("+", [resultado, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "MINUS":
                Parser.tokenizer.select_next()
                resultado = BinOp("-", [resultado, Parser.parse_term()])
            elif Parser.tokenizer.next.type == "CONCATENA":
                Parser.tokenizer.select_next()
                resultado = BinOp(".", [resultado, Parser.parse_term()])

        return resultado
    
    def parse_term():
        resultado = Parser.parse_factor()

        while Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV":
            if Parser.tokenizer.next.type == "MULT":
                Parser.tokenizer.select_next()
                resultado = BinOp("*", [resultado, Parser.parse_factor()])
            elif Parser.tokenizer.next.type == "DIV":
                Parser.tokenizer.select_next()
                resultado = BinOp("/", [resultado, Parser.parse_factor()])

        return resultado
    
    def parse_factor():

        resultado = None

        if Parser.tokenizer.next.type == "ENTIER":
            resultado = IntVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado
        
        elif Parser.tokenizer.next.type == "IDENTIFIANT":
            resultado = Identifiant(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado
        
        elif Parser.tokenizer.next.type == "CHAINE":
            resultado = StringVal(Parser.tokenizer.next.value, [])
            Parser.tokenizer.select_next()
            return resultado

        elif Parser.tokenizer.next.type == "PLUS":
            Parser.tokenizer.select_next()
            resultado = UnOp("+", [Parser.parse_factor()])
            return resultado

        elif Parser.tokenizer.next.type == "MINUS":
            Parser.tokenizer.select_next()
            resultado = UnOp("-", [Parser.parse_factor()])
            return resultado
        
        elif Parser.tokenizer.next.type == "NOT":
            Parser.tokenizer.select_next()
            resultado = UnOp("!", [Parser.parse_factor()])
            return resultado

        elif Parser.tokenizer.next.type == "ABRE_PARENTESIS":
            Parser.tokenizer.select_next()
            resultado = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type == "FECHA_PARENTESIS":
                Parser.tokenizer.select_next()
                return resultado
            else:
                raise TypeError("Erro")
        else:
            raise TypeError("Erro")
        
            
    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.select_next()
        resultado = Parser.parse_program()

        if Parser.tokenizer.next.type == "EOF":
            return resultado
        else:
            raise TypeError("Erro")

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        code = file.read() + '\n'
        code = PrePro.filter(code)

    st = SymbolTable()
    root = Parser.run(code)
    root.evaluate(st)