import string

from string_with_arrows import *
#Burada classımızdaki bilgileri kullanmak için gerekli olan kısım

#Sabit değerler
#Rakamlar Digits olarak ifade ediyoruz
#Bir karakterin rakam olup olmadığını tespit edebilmek için
DIGITS = '0123456789'

#Bir karakterin harf olup olmadığını tespit edebilmek için
LETTERS = string.ascii_letters
#Bir karakterin harf + rakam olup olmadığını tespit edebilmek için
LETTERS_DIGITS = LETTERS + DIGITS

#Hatalar için kullanacağımız kodlar
#Aradığımız karakteri bulamazsak bazı hatalar vermemiz gerekiyor, bu yüzden burada yapacağım şey kendi özel hata sınıfımızı tanımlıyorum.
#Bu metotumuz "Error" ismi detaylar ve posizyon başlangıcı ve bitişi değerlerini alıyor
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

#Burada bir metot oluşturuyoruz ve bu sadece bir string oluşturacak,hata adını ve ayrıntılarını gösterecek.
    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result

#Geçersiz Karakter Hatası
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Character', details)

#Beklenen Karakter Hatası
class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

#Geçersiz Sözdizimi için yani geçersiz bir syntax hatası sınıfı
#bu hatalar ayrıştırılma işleminde bir hata olduğunda oluşturulacaktır
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Geçersiz Syntax', details)

#Çalışma zamanı hatası için kullanacağımız kisim
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context
    #göster
    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + \
            string_with_arrows(self.pos_start.ftxt,
                               self.pos_start, self.pos_end)
        return result
    #geri izleme
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result
               #geri izleme(en son arama)


#Pozisyon bilgilerinde kullanacağımız kısım yani konum
#Position,satır numarası sütun numarasını ve mevcut indeksi takip ediyor
class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    #Satır İçerisinde ilerlemek için kullanacağımız kısım,bu sadece bir sonraki indekse geçecek
    #advance(ilerleme)
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    #Sadece konumun bir kopyasını oluşturacak bir kopyalama metot
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


#Tokenlerimiz
#Farklı töken türleri için sabitleri tanımlıyoruz
#Değişken tipi,sırasıyla int ve float
TT_INT = 'TT_INT' 
TT_FLOAT = 'FLOAT'  

# Değişkenler
# Keyword,identifier 
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'

#Operatörler
TT_PLUS = 'PLUS'    #Toplama(+)
TT_MINUS = 'MINUS'  #Çıkarma(-)
TT_DIV = 'DIV'      #Bölme(/)
TT_MUL = 'MUL'      #Çarpma (*)
TT_EQ = 'EQ'        #Eşittir(=)

#Üstünü almak için kullandığımız operatör (^)  Örn: 2^4 = 16
TT_POW = 'POW'

#Özel Semboller
TT_LPAREN = 'LPAREN'  #Sol Parantez (
TT_RPAREN = 'RPAREN'  #Sağ Parantez )

#Satır Sonu (end of line)
TT_EOF = "EOF"

TT_EE = 'EE'  #Eşittir
TT_NE = 'NE'  #Eşitr Değildir
TT_LT = 'LT'  #Küçüktür
TT_GT = 'GT'  #Büyüktür
TT_LTE = 'LTE' #Küçük Eşittir
TT_GTE = 'GTE' #Büyük Eşittir

#Dilimde kullanacağım kkeywordlerim
KEYWORDS = [
    'VAR',   #Değişken
    'AND',   #Ve
    'OR',    #Veya
    'NOT',   #Değil
    'IF',    #Eğer
    'THEN',  #Öyleyse
    'ELIF',  #Değil ise
    'ELSE',  #Değil
    'FOR',   #For Döngüsü
    'TO',    #Döngü Buraya Kadar
    'STEP',  #Artış veya Azalış Miktarı
    'WHILE'  #While Döngüsü
]

#Token,bir türü ve isteğe bağlı olarak bir değeri olan basit bir nesnedir.Her token, kodun yalnızca küçük bir bölümünden gelir.
#Token class'ında token'in tipi, değeri pozisyon başlangıcı ve bitişi bulunuyor
#Pozisyon başlangıç ve bitişi bize hatanın nerede olduğunu göstermek için var
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    #Eğer ki token türümüz ve değeri eşleşirse bu işlemi gerçekleştir diyoruz
    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    #Terminal penceresine yazdırıldığında güzel görünmesi için ona bir representation methodu
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'
#Token değere sahip olduktan sonra,türü ve ardından değeri yazdırır bir değeri yoksa, yalnızca türü yazdırır

#Lexer:Programı input olarak alıp tokenlere bölecek
#Lexer, karakter karakter girdiden geçecek ve metni, süreçte tokens dediğimiz bir listeye bölecektir
class Lexer:
    #Initialize method kısmında,işleyeceğimiz metni almamız gerekecek
    #Bunu sadece self.text'e atayacağız
    #Mevcut pozisyonu ve aynı zamanda mevcut karakteri takip etmemiz gerekiyor
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
    #Line(Satır) içerisinde ilerlemek için bu fonksiyonu kullanacağız
    #Metinde sadece bir sonraki karaktere ilerleyecek bir yöntem tanımlandı
    #Pozisyonu artırıyorum ve ardından mevcut karakteri metin içinde o konumdaki karaktere ayarlanılıyor
    #Bunu ancak konum metnin uzunluğundan küçükse yapabiliriz
    #Metnin sonuna ulaştığımızda,onu none olarak ayarlanıyor
    def advance(self):
        #else durumunda satırın sonun gelmişiz demektir
        #Girilen text içerisinde,text uzunluğu kadar gezeceğiz.
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(
            self.text) else None

    #Token oluşturuyoruz
    def make_tokens(self):
        tokens = []
        #Okunan karakter boş (' ') olmadığı sürece
        #Metindeki her karaktere giden bir döngü oluşturuluyor,mevcut karakterin none'a eşit olmadığını kontrol ediliyor
        #Çünkü yukarıda metnin sonuna geldiğimizde onu none olarak ayarlandı
        while self.current_char != None:
            #Boşluk varsa bir adım ilerle
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            #Okunan karakter + ise bunu TT_PLUS tokeni olarak tutcağız
            elif self.current_char == '+':
                #+ karakterini token listemize TT_PLUS adıyla ekledik
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()  #Bir karekter ilerliyoruz
                #Toplama işlemi için yaptığımız adımları,en üstte tanımladığımız tüm sabitler içinde yapıyorız
                #Çıkarma İşlemi
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
                #Çarpma İşlemi
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
             #Bölme İşlemi
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            #Üs (Kuvvet) İşlemi
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            #eşit
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ, pos_start=self.pos))
                self.advance()
            #Sol Parantez
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            #Sağ Parantez
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            #Değil Eşit
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            #Eşit mi ?
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            #Küçüktür
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            #Büyüktür
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            #Eğer tanımlı olan karakterlerden hiç biri gelmediyse hata dönmemiz gerekiyor
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    #Sayı birden fazla karakter olabilir bu yüzden, aslında bir sayı yapan bir fonksiyon yapıyoruz
    #Bu fonksiyon ya bir integer tokeni ya da bir float tokeni yapacaktır
    def make_number(self):
        #sayımız int ya da float mı kontrol etmek için kullandığımız ifade
        #Rakamları string formunda takip etmemiz gerekiyor
        num_str = ''
        #Ayrıca nokta sayısını da takip etmemiz gerekiyor.
        dot_count = 0  #Nokta Sayısı
        pos_start = self.pos.copy()
        #Sayıda nokta yoksa bu bir integerdir, ancak sayıda nokta varsa o zaman bir floattır
        #Bu fonksiyonun içinde, mevcut karakterin none olmadığını ve mevcut karakterin bir rakam veya nokta olup olmadığını kontrol edecek başka bir döngü oluşturuluyor
        while self.current_char != None and self.current_char in DIGITS + '.':
            #Geçerli karakter bir noktaysa eğer nokta sayısını artıracağız nokta sayısının zaten bire eşit olması durumunda,döngüden çıkıyoruz çünkü tek sayıda iki nokta olamaz
            if self.current_char == '.':
                if dot_count == 1:  #Sayı içerisinde birden fazla nokta olamaz
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
                 #Eğer nokta yoksa rakam stringini bir artırıyoruz çünkü sıradaki karakter bir rakam olmak zorunda
            self.advance()

            #Sayıda hiç nokta yoksa tipi int tipindedir
            #Nokta sayısının sıfıra eşit olup olmadığını kontrol ediyoruz eğer sıfırsa sayımız bir integer değilse floattır
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        #dot_counter'ın 0'dan farklı olduğu zaman sayıda nokta var demektir
        #Tipi floattır
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    #Girilen string geçerli bir string mi ? Asci'ye uyuyor mu onu kontrol ediyoruz
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        #Token Tipi kulanılabilir bir keyword mü onu kontrol ettiğimiz kısım
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    #Eşit değil mi kontrolü (!)
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
         #Eğer eşit değildir sembolü eşittirden sonra geldiyse hata çıkarıyoruz
        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (sonra '!')")

    #Eşit mi kontrolü (=)
    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    #Küçük mü kontrolü
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    #Büyük mü kontrolü
    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

#Nodes
#Düğümler
#Parser bir ağaç oluşturacak, önce birkaç farklı düğüm türü tanımlamamız gerekiyor
class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

     # özel bir represent methodu tanımlıyorum ve bu sadece tokeni string olarak döndürecek.
    def __repr__(self):
        return f'{self.tok}'

#VAR Tipi Erişimi için
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

#VAR Tipi Atama işlemi için
class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

#If Durumu İçin
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (
            self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

#For Döngüsü İçin
class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

#While Döngüsü için kullandığımız ifade
class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

#Parser
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Beklenen '+', '-', '*', '/' or '^'"
            ))
        return res

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"IF' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'THEN' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expr())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"'THEN' Bekleniyor"
                ))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expr())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'FOR' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Tanımlayıcı Bekleniyor"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Bekleniyor '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'TO' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error:
                return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'THEN' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body))

    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'WHILE' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"'THEN' Bekleniyor"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.expr())
        if res.error:
            return res

        return res.success(WhileNode(condition, body))

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "')' Bekleniyor"
                ))

        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Beklenenler int, float, identifier, '+', '-', '('"
        ))

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    #Matematiksel işlemler için  kullanacağımız ifade
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    #Eşitlkik Kontrol İfadeleri ( ==, <=, vb.)
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(
            self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Beklenen int, float, tipidedir, '+', '-', '(' veya 'NOT'"
            ))

        return res.success(node)  #Sonucu Dön

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Tanımlayıcı Bekleniyor"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Bekleniyor'='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(
            self.comp_expr, ((TT_KEYWORD, 'AND'), (TT_KEYWORD, 'OR'))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Beklenen 'VAR', int, float, identifier, '+', '-' veya '('"
            ))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)


#Çalışma Zamanı Sonuçları için kullanacağımız kod kısmı
#Mevcut sonucu takip edecek ve varsa bir hatayı da takip edecek
class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

#Değerler için kullanacağımız kod kısmı
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    #Bölünme Durumu
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Sıfır(0) a bölme hatası',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

    #Üs(Kuvvet Alma)
    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
    #Eşitlik Durumu
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
    #Eşit Değil Durumu (Değil Eşit)
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
    #Küçüktür Durumu
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
    #Büyüktür Durumu
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
    #Küçük Eşittir Durumu
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
    #Büyük Eşittir Durumu
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
    #VE Durumu
    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
    #VEYA Durumu
    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
    #Değil Durumu (not)
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

#Context
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


#Yorumlayıcı(Interpreter) için kullanılan kod kısmı
class Interpreter:
       # Bu metot,o düğümü işleyecek ve ardından tüm alt düğümleri ziyaret edecek
    def visit(self, node, context):
       #metot ismini almak için
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    #Eğer o isimde bir metot yoksa
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')


    #Her düğüm türü için gez metodu tanımlıyorum
    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(
                context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' tanımlanmadı.",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error:
            return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error:
            return res
        if node.step_value_node:
            step_value = res.register(
                self.visit(node.step_value_node, context))
            if res.error:
                return res
        else:
            step_value = Number(1)
        i = start_value.value
        if step_value.value >= 0:
            def condition(): return i < end_value.value
        else:
            def condition(): return i > end_value.value
        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)
    
    def visit_WhileNode(self, node, context):
        res = RTResult()
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error:
                return res
            if not condition.is_true():
                break
            res.register(self.visit(node.body_node, context))
            if res.error:
                return res
        return res.success(None)
    

#Çalıştırmak için kullanacağımız kod
#Global Sembol Tablosu
global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number(0))
#Kontrol durumu 0 dönüyorsa False yazdır
global_symbol_table.set("FALSE", Number(0))
#Kontrol durumu 1 dönüyorsa True yazdır
global_symbol_table.set("TRUE", Number(1))


#Çalıştırma kısmı
#Bu metot metin alıp çalıştıracak.
def run(fn, text): #fn:filename
    #Tokenlerı Üretmek için kullanacağımız kod kısmı
    #Yeni bir lexer oluşturuyoruz
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # Soyut syntax ağacını oluşturuyoruz
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    #Programı Çalıştır
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
